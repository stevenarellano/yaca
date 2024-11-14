from openai import OpenAI
import json
import os
import json
from tqdm import tqdm
import copy
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
from dotenv import load_dotenv
import argparse

load_dotenv()

with open("../prompts/prompt.txt", "r") as f:
    text = f.read()


def fetch_completion(openai: OpenAI, data_entry: dict, model: str):
    """
    Fetches a completion from the OpenAI API based on a task description and test case.

    Parameters:
        openai (OpenAI): An instance of OpenAI's API client.
        data_entry (dict): Dictionary containing the test case data and task description.
        model (str): Model name to be used for the completion.
        text (str): Context or additional instructions for the completion.

    Returns:
        dict: The updated data_entry dictionary with the completion text.
    """
    global text
    test_case = data_entry.get("small_test_cases")
    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            completions = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a code developer."},
                    {
                        "role": "user",
                        "content": (
                            f"{text}\n"
                            f"# Task description:\n```python\n{data_entry.get('markdown_description', '')}\n```\n"
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

    return data_entry if data_entry["completion"] else {"error": "Failed to fetch completion after retries"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run OpenAI model completions.')
    parser.add_argument('--model', type=str, default='babbage-002',
                        help='Model name to be used for the completion')
    args = parser.parse_args()
    model = args.model

    with open("../data/dataset.json", "r") as f:
        dataset = json.load(f)

    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_entry = {
            executor.submit(fetch_completion, openai, copy.deepcopy(entry), model): entry
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

    with open(f"./results/{model}.json", "w") as f:
        json.dump(dataset, f, indent=4)
