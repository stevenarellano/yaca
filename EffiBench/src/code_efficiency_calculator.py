import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from tqdm import tqdm
import argparse


def calculate_code_execution_efficiency(data, evaluation_code=False, path="./tmp/", max_execution_time=5):
    problem_idx = data["problem_idx"]
    completion_file, _ = add_string_to_py_file(
        data, evaluation_code=evaluation_code, path=path)
    # print("Completion file", completion_file)
    script_path = '../scripts/run_code.sh'
    completion_dat_file = f'./{path}/{problem_idx}.dat'
    # print("Dat file:" + completion_dat_file)
    try:
        result = subprocess.run([script_path, completion_file, completion_dat_file, str(max_execution_time)],
                                check=True, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        if result.returncode != 0:
            print("[Error running script]" + result.stderr[0:10] + "...")
    except Exception as e:
        print("Error running script: ", str(e)[:10] + "...")
    finally:
        return data


def fetch_completion(dataset, model_path):
    with ThreadPoolExecutor() as executor:
        future_to_entry = {executor.submit(calculate_code_execution_efficiency, entry,
                                           False, path=model_path, max_execution_time=5): entry for entry in tqdm(dataset)}
        for future in tqdm(concurrent.futures.as_completed(future_to_entry)):
            entry = future_to_entry[future]
            try:
                updated_entry = future.result()
                idx = dataset.index(entry)
                dataset[idx] = updated_entry
            except Exception as e:
                pass
    return dataset


def add_string_to_py_file(data, evaluation_code=False, path="./tmp/"):
    os.makedirs(path, exist_ok=True)
    if not evaluation_code:
        test_case = data["test_case"]
    else:
        test_case = data["small_test_cases"]
    problem_idx = data["problem_idx"]
    return_path, full_code = "", ""
    try:
        if "class Solution" in data["completion"]:
            code = data["completion"]
            if "```python" in code:
                start_idx = code.find("```python") + len("```python")
                code = code[start_idx:]
                if "```" in code:
                    end_idx = code.find("```")
                    code = code[:end_idx]
            full_code = code + "\nsolution=Solution()\n" + test_case
            with open(f"./{path}/{problem_idx}.py", "w") as f:
                f.write(full_code)
            return_path = f"./{path}/{problem_idx}.py"
    except Exception as e:
        pass
    return return_path, full_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process code executions for given models.')
    parser.add_argument('--models', nargs='+', required=True,
                        help='List of model names')
    args = parser.parse_args()
    models = args.models

    for model in models:
        if "/" in model:
            model_name = model.split("/")[1]
        else:
            model_name = model
        try:
            with open(f"./results/{model_name}.json", "r") as f:
                dataset = json.load(f)
        except Exception as e:
            print(f"Error loading dataset for model {model_name}: {e}")
            continue

        dat_path = f"./dat_results/{model_name}"
        os.makedirs(dat_path, exist_ok=True)

        fetch_completion(dataset, dat_path)
