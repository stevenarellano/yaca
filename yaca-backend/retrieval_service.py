from typing import Any, List, Optional
import chromadb
import logging
import json
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


class RetrievalService:
    def __init__(
            self,
            json_data_path: str = "../../model/data/training_data.json",
            collection_name: str = "default",
            chromadb_path: str = "chromadb",
            base_model: Any = None,
            adapter: Optional[Any] = None
    ):
        self.base_model = base_model
        self.adapter = adapter
        self.collection = self.setup_and_add_chunks_to_chromadb(
            json_data_path=json_data_path, chromadb_path=chromadb_path, collection_name=collection_name)

    @staticmethod
    def load_data(file_path: str) -> List[dict]:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def setup_and_add_chunks_to_chromadb(
            self,
            json_data_path,
            chromadb_path,
            collection_name
    ) -> chromadb.Collection:
        logging.getLogger("chromadb").setLevel(logging.WARNING)

        training_data = self.load_data(json_data_path)
        train_data, val_data = train_test_split(
            training_data, test_size=0.3, random_state=42
        )
        embedding_corpus = train_data + val_data

        client = chromadb.PersistentClient(path=chromadb_path)
        collection_list = client.list_collections()
        collection_names = [col.name for col in collection_list]

        if collection_name in collection_names:
            collection = client.get_collection(collection_name)
        else:
            collection = client.create_collection(
                collection_name, metadata={"hnsw:space": "cosine"}
            )

            def add_chunk(chunk, index) -> None:
                collection.add(documents=[chunk], ids=[f"chunk_{index}"])

            with ThreadPoolExecutor(max_workers=25) as executor, tqdm(
                    total=len(embedding_corpus), desc="Adding chunks") as pbar:
                futures = [
                    executor.submit(add_chunk, chunk['solution'], i)
                    for i, chunk in enumerate(embedding_corpus)
                ]
                for future in futures:
                    future.result()
                    pbar.update(1)

        return collection

    def retrieve_context(
        self,
        problem_description: str,
        k: int,
    ) -> List[str]:
        """
        Retrieve the top-k most relevant examples from the collection for a given problem description.

        Parameters:
            problem_description (str): The problem statement for which we want to retrieve context.
            base_model: The base embedding model used for encoding the problem description.
            k (int): Number of top relevant examples to retrieve.
            adapter (optional): An optional adapter model to apply to the query embeddings.

        Returns:
            List[str]: List of top-k relevant examples retrieved from the collection.
        """
        query_embedding = self.base_model.encode(
            problem_description, convert_to_tensor=True)

        if self.adapter is not None:
            device = next(self.adapter.parameters()).device
            query_embedding = self.adapter(
                query_embedding.to(device)).cpu().detach().numpy()
        else:
            query_embedding = query_embedding.numpy()

        retrieved_documents = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=k
        )

        top_k_documents = retrieved_documents['documents'][0]
        return top_k_documents
