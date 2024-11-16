from torch import nn
from typing import Any, List, Optional
import chromadb
import logging
import json
import openai
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
import torch
from tqdm import tqdm
import copy
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
import argparse
import os
from dotenv import load_dotenv

RAG_CONTEXT_COUNT = 3
ADAPTER_FOLDER_PATH = '../../model/adapters/'
CORPUS_DATA_PATH = '../../model/data/cpp_python/corpus_data.json'
COLLECTION_NAME = "cpp_python"

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

with open("../prompts/prompt.txt", "r") as f:
    text = f.read()


def retrieve_context(
    problem_description: str,
    base_model: Any,
    collection: Any,
    k: int,
    adapter: Optional[Any] = None
) -> List[str]:
    """
    Retrieve the top-k most relevant examples from a ChromaDB collection for a given problem description.

    Parameters:
        problem_description (str): The problem statement for which we want to retrieve context.
        base_model: The base embedding model used for encoding the problem description.
        collection: The ChromaDB collection containing code snippet embeddings.
        k (int): Number of top relevant examples to retrieve.
        adapter (optional): An optional adapter model to apply to the query embeddings for RAG.

    Returns:
        list: List of top-k relevant examples retrieved from the collection.
    """
    query_embedding = base_model.encode(
        problem_description, convert_to_tensor=True)

    if adapter is not None:
        device = next(adapter.parameters()).device
        query_embedding = adapter(
            query_embedding.to(device)).cpu().detach().numpy()
    else:
        query_embedding = query_embedding.numpy()

    retrieved_documents = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )

    top_k_documents = retrieved_documents['documents'][0]
    return top_k_documents


def fetch_completion(data_entry, model, base_model=None, collection=None, adapter=None):
    global text
    test_case = data_entry["small_test_cases"]
    rag_context = retrieve_context(
        data_entry['markdown_description'], base_model, collection, k=RAG_CONTEXT_COUNT, adapter=adapter)
    rag_as_string = "\n".join(rag_context)
    while True:
        try:
            completions = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a code developer."},
                    {
                        "role": "user",
                        "content": (
                            f"{text}\n"
                            f"# Here's some examples of high performant code:\n{rag_as_string}\n"
                            f"# Task description:\n```python\n{data_entry['markdown_description']}\n```\n"
                            f"# Test case:\n```python\n{test_case}\n```"
                        )
                    },
                ],
            )
            data_entry["completion"] = completions.choices[0].message.content
            if data_entry["completion"]:
                break
        except Exception as e:
            print(f"[ERROR] fetch_completion attempt {retries + 1}: {repr(e)}")
            time.sleep(10)
            retries += 1
            data_entry["completion"] = ""
    return data_entry


def setup_and_add_chunks_to_chromadb(embedding_corpus, path="chromadb"):
    logging.getLogger("chromadb").setLevel(logging.WARNING)

    client = chromadb.PersistentClient(path=path)

    collection_list = client.list_collections()
    collection_names = [col.name for col in collection_list]

    if COLLECTION_NAME in collection_names:
        collection = client.get_collection(COLLECTION_NAME)
        print(
            f"Collection '{COLLECTION_NAME}' already exists. Skipping chunk addition.")
    else:
        collection = client.create_collection(
            COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

        def add_chunk(chunk, index):
            collection.add(documents=[chunk], ids=[f"chunk_{index}"])

        with ThreadPoolExecutor(max_workers=25) as executor, tqdm(total=len(embedding_corpus), desc="Adding chunks") as pbar:
            futures = [
                executor.submit(add_chunk, chunk['solution'], i)
                for i, chunk in enumerate(embedding_corpus)
            ]
            for future in futures:
                future.result()
                pbar.update(1)

        print("All chunks have been added to the collection.")

    return collection


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


class LinearAdapter(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, input_dim)

    def forward(self, x):
        return self.linear(x)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Fetch completions using OpenAI API.')
    parser.add_argument('--model', type=str, default='gpt-4o-mini',
                        help='Model name to use for completion')  # any openai model
    parser.add_argument('--embeddings_adapter', type=str,
                        default='cpp_adapter_10_lr0.01_no_negatives',)  # adapters can be found in <ROOT>/model/adapters/
    args = parser.parse_args()
    model = args.model
    adapter_name = args.embeddings_adapter

    with open("../data/dataset.json", "r") as f:
        dataset = json.load(f)

    base_model = SentenceTransformer('all-MiniLM-L6-v2')

    training_data = load_data(CORPUS_DATA_PATH)
    train_data, val_data = train_test_split(
        training_data, test_size=0.3, random_state=42)

    print("Adding data chunks to a ChromaDB collection...")
    collection = setup_and_add_chunks_to_chromadb(train_data + val_data)

    adapter = LinearAdapter(base_model.get_sentence_embedding_dimension())

    adapter.load_state_dict(torch.load(
        ADAPTER_FOLDER_PATH + adapter_name + '.pth')['adapter'])

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_entry = {
            executor.submit(fetch_completion, copy.deepcopy(entry), model, base_model, collection, adapter): entry
            for entry in tqdm(dataset)
        }
        for future in tqdm(concurrent.futures.as_completed(future_to_entry)):
            entry = future_to_entry[future]
            try:
                updated_entry = future.result()
                idx = dataset.index(entry)
                dataset[idx] = updated_entry
            except Exception as e:
                print(repr(e))

    os.makedirs("./results/", exist_ok=True)
    with open(f"./results/rag{RAG_CONTEXT_COUNT}_{adapter_name}_{model}.json", "w") as f:
        json.dump(dataset, f, indent=4)
