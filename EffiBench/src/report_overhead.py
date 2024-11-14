import os
import glob
import argparse


def calculate_memory_usage(dat_file_path):
    with open(dat_file_path, 'r') as file:
        prev_time = 0
        prev_mem_mb = 0
        mem_time_mb_s = 0
        next(file)
        for line in file:
            if "__main__." in line:
                continue
            parts = line.split()
            mem_in_mb = float(parts[1])
            timestamp = float(parts[2])
            if prev_time > 0:
                time_interval_s = timestamp - prev_time
                mem_time_mb_s += (prev_mem_mb + mem_in_mb) / \
                    2 * time_interval_s
            prev_time = timestamp
            prev_mem_mb = mem_in_mb
        return mem_time_mb_s


def calculate_runtime(dat_file_path):
    with open(dat_file_path, 'r') as file:
        start_time = float("inf")
        end_time = float("-inf")
        next(file)
        for line in file:
            if "__main__." in line:
                continue
            parts = line.split()
            timestamp = float(parts[2])
            start_time = min(start_time, timestamp)
            end_time = max(end_time, timestamp)
        return max(end_time - start_time, 0)


def report_max_memory_usage(dat_file_path):
    max_memory_usage = 0
    with open(dat_file_path, 'r') as file:
        next(file)
        for line in file:
            if "__main__." in line:
                continue
            parts = line.split()
            mem_in_mb = float(parts[1])
            max_memory_usage = max(max_memory_usage, mem_in_mb)
        return max_memory_usage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process model data and calculate metrics.')
    parser.add_argument('--models', nargs='+',
                        default=["gpt-3.5-turbo-0125"], help='List of model names')
    args = parser.parse_args()
    model_list = args.models

    canonical_solution_directory = "./dat_results/canonical_solution"
    canonical_solution_memory_usage = {}
    canonical_solution_execution_time = {}
    canonical_solution_max_memory_usage = {}
    for dat_file in glob.glob(os.path.join(canonical_solution_directory, "*.dat")):
        try:
            problem_idx = os.path.basename(dat_file).split('.')[0]
            canonical_solution_memory_usage[int(
                problem_idx)] = calculate_memory_usage(dat_file)
            canonical_solution_execution_time[int(
                problem_idx)] = calculate_runtime(dat_file)
            canonical_solution_max_memory_usage[int(
                problem_idx)] = report_max_memory_usage(dat_file)
        except:
            # print('Error processing canonical solution')
            pass

    global_result = {}

    for model in model_list:
        if "/" in model:
            model_name = model.split("/")[1]
        else:
            model_name = model
        completion_memory_usage = {}
        execution_time = {}
        max_memory_usage = {}
        task_idx = {}
        dat_directory = f"./dat_results/{model_name}"
        for dat_file in glob.glob(os.path.join(dat_directory, "*.dat")):
            try:
                problem_idx = os.path.basename(dat_file).split('.')[0]
                completion_memory_usage[int(
                    problem_idx)] = calculate_memory_usage(dat_file)
                execution_time[int(problem_idx)] = calculate_runtime(dat_file)
                max_memory_usage[int(problem_idx)
                                 ] = report_max_memory_usage(dat_file)
                task_idx[int(problem_idx)] = dat_file
            except Exception as e:
                pass
                # print('Error processing completion: ', e)
        global_result[model_name] = {
            "completion_memory_usage": completion_memory_usage,
            "execution_time": execution_time,
            "max_memory_usage": max_memory_usage,
            "task_idx": task_idx
        }

    for model_name in global_result.keys():
        completion_memory_usage = global_result[model_name]["completion_memory_usage"]
        execution_time = global_result[model_name]["execution_time"]
        max_memory_usage = global_result[model_name]["max_memory_usage"]

        total_execution_time = 0
        normalized_execution_time = 0
        total_max_memory_usage = 0
        normalized_max_memory_usage = 0
        total_memory_usage = 0
        total_canonical_solution_max_memory_usage = 0
        total_canonical_solution_execution_time = 0
        total_canonical_solution_memory_usage = 0
        normalized_memory_usage = 0
        total_codes = 0
        normalized_execution_time_list = []
        normalized_max_memory_usage_list = []
        normalized_memory_usage_list = []
        max_NET = 0
        max_NMU = 0
        max_TMU = 0
        NET_greater_5 = 0
        NMU_greater_5 = 0
        TMU_greater_5 = 0

        for idx in completion_memory_usage.keys():
            if idx not in canonical_solution_memory_usage.keys():
                continue

            total_memory_usage += completion_memory_usage[idx]
            total_execution_time += execution_time[idx]
            total_max_memory_usage += max_memory_usage[idx]
            total_canonical_solution_max_memory_usage += canonical_solution_max_memory_usage[idx]
            total_canonical_solution_memory_usage += canonical_solution_memory_usage[idx]
            total_canonical_solution_execution_time += canonical_solution_execution_time[idx]

            norm_exec_time = execution_time[idx] / \
                canonical_solution_execution_time[idx]
            norm_mem_usage = completion_memory_usage[idx] / \
                canonical_solution_memory_usage[idx]
            norm_max_mem_usage = max_memory_usage[idx] / \
                canonical_solution_max_memory_usage[idx]

            max_NET = max(max_NET, norm_exec_time)
            max_NMU = max(max_NMU, norm_mem_usage)
            max_TMU = max(max_TMU, completion_memory_usage[idx])

            if norm_exec_time > 5:
                NET_greater_5 += 1
            if norm_mem_usage > 5:
                NMU_greater_5 += 1
            if completion_memory_usage[idx] > 5:
                TMU_greater_5 += 1

            normalized_execution_time_list.append(norm_exec_time)
            normalized_max_memory_usage_list.append(norm_max_mem_usage)
            normalized_memory_usage_list.append(norm_mem_usage)

            total_codes += 1

        if total_codes == 0:
            print(f"{model_name} has no data")
            continue

        normalized_execution_time = total_execution_time / \
            total_canonical_solution_execution_time
        normalized_max_memory_usage = total_max_memory_usage / \
            total_canonical_solution_max_memory_usage
        normalized_memory_usage = total_memory_usage / \
            total_canonical_solution_memory_usage
        total_execution_time = total_execution_time / \
            len(normalized_execution_time_list)
        total_memory_usage = total_memory_usage / \
            len(normalized_execution_time_list)
        total_max_memory_usage = total_max_memory_usage / \
            len(normalized_execution_time_list)

        NET_percent_greater_5 = (NET_greater_5 / total_codes) * 100
        NMU_percent_greater_5 = (NMU_greater_5 / total_codes) * 100
        TMU_percent_greater_5 = (TMU_greater_5 / total_codes) * 100

        pass1 = len(normalized_execution_time_list) / 1000 * 100

        print(
            f"Model: {model_name}\n"
            f"Execution Time (ET): {total_execution_time:.2f} seconds\n"
            f"Normalized Execution Time (NET): {normalized_execution_time:.2f}\n"
            f"Max Normalized Execution Time (Max_NET): {max_NET:.2f}\n"
            f"Percentage of Tasks with NET > 5: {NET_percent_greater_5:.1f}%\n"
            f"\n"
            f"Memory Usage (MU): {total_memory_usage:.2f} MB/s\n"
            f"Normalized Memory Usage (NMU): {normalized_memory_usage:.2f}\n"
            f"Max Normalized Memory Usage (Max_NMU): {max_NMU:.2f}\n"
            f"Percentage of Tasks with NMU > 5: {NMU_percent_greater_5:.1f}%\n"
            f"\n"
            f"Max Memory Usage (TMU): {total_max_memory_usage:.2f} MB\n"
            f"Normalized Total Memory Usage (NTMU): {normalized_max_memory_usage:.2f}\n"
            f"Max Total Memory Usage (Max_TMU): {max_TMU:.2f} MB\n"
            f"Percentage of Tasks with TMU > 5: {TMU_percent_greater_5:.1f}%\n"
            f"\n"
            f"Pass Rate (pass1): {pass1:.1f}%\n"
            "------------------------------------------------------------\n"
        )
