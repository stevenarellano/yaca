import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from tqdm import tqdm


def write_canonical_solution(data, path="./dat_results/canonical_solution"):
    """
    Writes the canonical solution from the data to a Python file in the specified path.
    """
    problem_idx = data["problem_idx"]
    os.makedirs(path, exist_ok=True)

    try:
        if "canonical_solution" in data and data["canonical_solution"]:
            solution_code = data["canonical_solution"]
            if "```python" in solution_code:
                start_idx = solution_code.find("```python")
                solution_code = solution_code[start_idx + 9:]
                if "```" in solution_code:
                    end_idx = solution_code.find("```")
                    solution_code = solution_code[:end_idx]

            # Write solution code to file
            file_path = os.path.join(path, f"{problem_idx}.py")
            with open(file_path, "w") as file:
                file.write(solution_code)
            return file_path
    except Exception as e:
        print(
            f"Error writing canonical solution for problem {problem_idx}: {e}")
    return None


def process_canonical_solutions(dataset):
    """
    Iterates over the dataset and writes canonical solutions concurrently.
    """
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(
            write_canonical_solution, entry): entry for entry in tqdm(dataset)}
        for future in tqdm(concurrent.futures.as_completed(futures)):
            entry = futures[future]
            try:
                future.result()  # Check if the future completed without exceptions
            except Exception as e:
                print(
                    f"Exception processing entry {entry['problem_idx']}: {e}")
    return dataset


def calculate_code_execution_efficiency(data, path="./tmp/", max_execution_time=5):
    """
    Runs the specified canonical solution and generates a .dat file with profiling information.
    """
    problem_idx = data["problem_idx"]
    script_path = '../scripts/run_code.sh'
    completion_file = f'./{path}/{problem_idx}.py'
    completion_dat_file = f'./{path}/{problem_idx}.dat'
    os.makedirs(path, exist_ok=True)
    try:
        result = subprocess.run(
            [script_path, completion_file,
                completion_dat_file, str(max_execution_time)],
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:
        print(
            f"Error running script for problem {problem_idx}: {str(e.stderr)[:20]}")
    except Exception as e:
        print(f"Unexpected error for problem {problem_idx}: {str(e)[:20]}")

    finally:
        return data


def run_all_solutions(dataset, path="./dat_results/canonical_solution", max_execution_time=5):
    """
    Runs all canonical solution files and generates .dat files with profiling information.
    """
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(calculate_code_execution_efficiency, entry, path, max_execution_time): entry
            for entry in tqdm(dataset)
        }
        for future in tqdm(concurrent.futures.as_completed(futures)):
            entry = futures[future]
            try:
                future.result()
            except Exception as e:
                print(
                    f"Exception running solution for problem {entry['problem_idx']}: {e}")


if __name__ == "__main__":
    try:
        with open(f"../data/dataset.json", "r") as file:
            dataset = json.load(file)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        dataset = []

    canonical_path = f"./dat_results/canonical_solution"
    os.makedirs(canonical_path, exist_ok=True)

    dataset = process_canonical_solutions(dataset)
    run_all_solutions(dataset, path=canonical_path, max_execution_time=5)
