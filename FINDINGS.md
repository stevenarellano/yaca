# Findings

This file contains information on the research findings of the project. The findings are organized by the following sections:

1. **Embeddings Fine-tuning**: My improvements in creating an embeddings model on HPC datasets.
2. **HPC Code Completions**: My improvements on HPC code generation.

## Embeddings Fine-tuning

This section outlines the process and findings from fine-tuning embeddings models specifically for High-Performance Computing (HPC) datasets, aimed at improving code retrieval accuracy in code completion tasks.

### Experiment Overview

The goal of our embeddings model is to take a problem statement or incomplete code snippet as input and return a list of relevant code completions, as defined by `problem statement` and `solution` columns in the [hpc-instruct](https://huggingface.co/datasets/hpcgroup/hpc-instruct) dataset. To find the best model capable of doing so, we fine-tuned linear adapter model on top of the pre-trained `all-MiniLM-L6-v2` model from [sentence transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) on the `hpc-instruct` dataset.

The fine-tuning process involved a few hyperparams that were tuned to optimize the model's performance. Specifically, we experimented with different learning rates, number of epochs, and the presence or absence of negative samples during training. The negative samples chosen were language model generated "non-performant" versions of the solution code. For each model, their hyperparams are listed as follows:

| Adapter File Name                    | Num Epochs | Batch Size | Learning Rate | Warmup Steps | Max Grad Norm | Margin | Use Negatives |
| ------------------------------------ | ---------- | ---------- | ------------- | ------------ | ------------- | ------ | ------------- |
| `adapter_10_lr0.01_negatives.pth`    | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | True          |
| `adapter_10_lr0.01_no_negatives.pth` | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | False         |
| `adapter_5_negatives.pth`            | 5          | 32         | 0.003         | 100          | 1.0           | 1.0    | True          |
| `adapter_5_no_negatives.pth`         | 5          | 32         | 0.003         | 100          | 1.0           | 1.0    | False         |

### Baseline and Evaluation Metrics

To measure the effectiveness of our fine-tuned model, we compared it against the baseline `all-MiniLM-L6-v2` model in retrieving the correct code (`solution`) from the `hpc-instruct` corpus in a chromadb embeddings database. We evaluated the models on the following metrics:

1. Hit Rate @k: measures whether the correct code is in the top-k retrieved results.
2. Mean Reciprocal Rank @k: measures the average reciprocal rank of the correct code in the top-k retrieved results.
3. Mean Average Precision @k: measures the average precision of the correct code in the top-k retrieved results.
4. Normalized Discounted Cumulative Gain @k: measures the quality of the ranking of the correct code in the top-k retrieved results.

### Experiment Results

I evaluated the models on a variety of k's. The results of the experiment are summarized in the table below:

| Model Type                         | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| ---------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model                         | 1   | 0.6164              | 0.6164                  | 0.6164                    | 0.6164          |
| adapter_5_no_negatives.pth         | 1   | 0.6374              | 0.6374                  | 0.6374                    | 0.6374          |
| adapter_5_negatives.pth            | 1   | 0.0350              | 0.0350                  | 0.0350                    | 0.0350          |
| adapter_10_lr0.01_negatives.pth    | 1   | 0.1330              | 0.1330                  | 0.1330                    | 0.1330          |
| adapter_10_lr0.01_no_negatives.pth | 1   | 0.7425              | 0.7425                  | 0.7425                    | 0.7425          |
| Base Model                         | 3   | 0.6707              | 0.6398                  | 0.6398                    | 0.6478          |
| adapter_5_no_negatives.pth         | 3   | 0.7022              | 0.6663                  | 0.6663                    | 0.6756          |
| adapter_5_negatives.pth            | 3   | 0.0665              | 0.0484                  | 0.0484                    | 0.0550          |
| adapter_10_lr0.01_negatives.pth    | 3   | 0.1943              | 0.1608                  | 0.1608                    | 0.1714          |
| adapter_10_lr0.01_no_negatives.pth | 3   | 0.7985              | 0.7676                  | 0.7676                    | 0.7756          |
| Base Model                         | 10  | 0.7285              | 0.6500                  | 0.6500                    | 0.6689          |
| adapter_5_no_negatives.pth         | 10  | 0.7740              | 0.6896                  | 0.6896                    | 0.7100          |
| adapter_5_negatives.pth            | 10  | 0.1015              | 0.0469                  | 0.0469                    | 0.0658          |
| adapter_10_lr0.01_negatives.pth    | 10  | 0.2592              | 0.1641                  | 0.1641                    | 0.2361          |
| adapter_10_lr0.01_no_negatives.pth | 10  | 0.8406              | 0.7788                  | 0.7788                    | 0.8000          |

### Analysis

The results show that the `adapter_10_lr0.01_no_negatives.pth` model performed best across all metrics when compared to other other models of the same `k`. One interesting finding was that when incorporating negatives, the model performed poorly. This could be due to the negative samples being too similar to the positive samples. Ultimately, for further use in the HPC code completion testing, the `adapter_10_lr0.01_no_negatives.pth` model will be used.

I would like to find a way to incorporate negatives in a way that is more beneficial to the model. I propose three potential solutions:

1. Better Negative Sampling Strategy: Instead of using very similar negative samples (with just different performance), use negative samples that are entirely different from the positive samples.
2. Increase model size: The model may be able to differentiate between the current performance and non-performance samples if it is larger.

## HPC Code Completions

This section details the research conducted to assess and improve code generation for High-Performance Computing (HPC) tasks using large language models (LLMs).

### Experiment Overview

The primary objective was to analyze the efficiency of code generated by these models, comparing it against human-written canonical solutions to understand where automated code generation excels and where it falls short in terms of execution speed, memory usage, and overall computational efficiency. The experiment utilized EffiBench, a benchmark suite containing 1,000 efficiency-critical coding problems from LeetCode. Each problem in the suite was paired with a human-written canonical solution optimized for minimal runtime and memory consumption. Multiple closed source LLMs were tasked with generating code to solve these problems.

### Experiment Overview

The experiment utilized EffiBench, a benchmark suite containing 1,000 efficiency-critical coding problems from LeetCode. Each problem in the suite was paired with a human-written canonical solution optimized for minimal runtime and memory consumption. Multiple closed source LLMs were tasked with generating code to solve these problems. Generated solutions were then evaluated against EffiBench’s canonical solutions, focusing on execution time (ET), normalized execution time (NET), memory usage (MU), normalized memory usage (NMU), and total memory usage (TMU) to benchmark efficiency.

For certain models, experiments incorporated a custom Retrieval-Augmented Generation (RAG) pipeline to evaluate if providing additional context could yield more efficient code. This RAG pipeline utilized the `adapter_10_lr0.01_no_negatives.pth` linear adapter from before (paired again with the `all-MiniLM-L6-v2` model) to retrieve performant code snippets from the `hpc-instruct` dataset, which were then used as context for code generation.

### Baseline and Evaluation Metrics

The experiment evaluated the RAG's pipeline ability to generate efficient code by comparing its completions against those of standalone models of varying sizes. These models include `gpt-4o-mini`, `gpt-4-turbo-preview`, and `gpt-3.5-turbo-0125`.

In comparing the models, the following metrics were used:

-   Execution Time (ET) (milliseconds): The average time taken by the model to execute a task.
-   Normalized Execution Time (NET) (unitless): The ratio of the model's execution time to the canonical solution's execution time.
-   Maximum Normalized Execution Time (Max_NET) (unitless): The highest value of NET across all tasks.
-   Percentage of Tasks with NET > 5 (NET>5) (%): The percentage of tasks where the model's execution time is more than five times that of the canonical solution.
-   Memory Usage (MU) (megabyte-seconds, MB·s): The average memory consumption of the model over time during task execution, calculated as the integral of memory usage over time.
-   Normalized Memory Usage (NMU) (unitless): The ratio of the model's memory usage to the canonical solution's memory usage.
-   Maximum Normalized Memory Usage (Max_NMU) (unitless): The highest value of NMU across all tasks.
-   Percentage of Tasks with NMU > 5 (NMU>5) (%): The percentage of tasks where the model's memory usage is more than five times that of the canonical solution.
-   Total Max Memory Usage (TMU) (megabytes, MB): The average of the maximum memory usage observed during each task's execution.
-   Normalized Total Max Memory Usage (NTMU) (unitless): The ratio of the model's maximum memory usage to the canonical solution's maximum memory usage.
-   Maximum Total Memory Usage (Max_TMU) (megabytes, MB): The highest total memory usage recorded across all tasks.
-   Percentage of Tasks with TMU > 5 (TMU>5) (%): The percentage of tasks where the maximum memory usage exceeds 5 MB.
-   Pass Rate (pass1) (%): The percentage of tasks that the model completed successfully without errors.

### Table of Results

| Model                    | ET   | NET  | Max_NET | NET>5 | MU    | NMU  | Max_NMU | NMU>5 | TMU   | NTMU | Max_TMU | TMU>5 | pass1 |
| ------------------------ | ---- | ---- | ------- | ----- | ----- | ---- | ------- | ----- | ----- | ---- | ------- | ----- | ----- |
| **rag3_and_gpt-4o-mini** | 1.31 | 0.71 | 1.41    | 0.0   | 43.00 | 0.72 | 1.64    | 0.0   | 47.44 | 1.01 | 81.77   | 100.0 | 14.0  |
| **rag2_and_gpt-4o-mini** | 1.45 | 0.80 | 1.40    | 0.0   | 47.45 | 0.80 | 1.65    | 0.0   | 47.48 | 1.01 | 90.81   | 100.0 | 15.2  |
| **gpt-3.5-turbo-0125**   | 1.47 | 0.80 | 2.42    | 0.0   | 48.41 | 0.81 | 2.87    | 0.0   | 47.48 | 1.02 | 119.33  | 100.0 | 12.7  |
| **gpt-4o-mini**          | 1.58 | 0.86 | 2.02    | 0.0   | 52.11 | 0.87 | 2.36    | 0.0   | 47.46 | 1.01 | 121.91  | 100.0 | 14.4  |
| **rag1_and_gpt-4o-mini** | 1.71 | 0.93 | 2.08    | 0.0   | 56.50 | 0.94 | 2.20    | 0.0   | 47.42 | 1.01 | 109.23  | 100.0 | 13.4  |
| **gpt-4-turbo-preview**  | 1.95 | 1.07 | 1.93    | 0.0   | 64.03 | 1.08 | 2.18    | 0.0   | 47.45 | 1.01 | 114.98  | 100.0 | 15.2  |

### Analysis

The experiment results indicate that the RAG pipeline, did generally improve the efficiency of code generated by the LLMs. Specifically, incorporating few-shot learning within the RAG framework led to significant enhancements in normalized execution time (NET) and normalized memory usage (NMU).

Models utilizing two-shot (`rag2_and_gpt-4o-mini`) and three-shot (`rag3_and_gpt-4o-mini`) learning demonstrated notable improvements over both the base model (`gpt-4o-mini`). The `rag3_and_gpt-4o-mini` model achieved a NET of 0.71, which is approximately a 17% improvement compared to the base model's NET of 0.86. Similarly, `rag2_and_gpt-4o-mini` recorded a NET of 0.80, reflecting about a 7% improvement. In terms of memory efficiency, the few-shot models also outperformed the base model. The `rag3_and_gpt-4o-mini` model achieved an NMU of 0.72, representing a 17% reduction compared to the base model's NMU of 0.87. The `rag2_and_gpt-4o-mini` model had an NMU of 0.80, marking an 8% reduction.

Interestingly, it seemed that one-shot learning had an adverse effect. The `rag1_and_gpt-4o-mini` model showed a NET of 0.93, which is about an 8% slow down compared to the base model's NET of 0.86. Its NMU increased to 0.94, also an 8% increase over the base model. These results suggest that a single example may not provide sufficient context for the model to generalize efficient coding patterns, potentially leading to decreased performance.

Another significant finding is the drastic lowering of the maximum normalized execution time (Max_NET) and maximum normalized memory usage (Max_NMU) in the few-shot RAG models. The `rag3_and_gpt-4o-mini` model had a Max_NET of 1.41, a 30% reduction compared to the base model's Max_NET of 2.02. Its Max_NMU was 1.64, approximately a 31% reduction from the base model's Max_NMU of 2.36. Similarly, `rag2_and_gpt-4o-mini` showed substantial decreases in these maxima. These reduction indicate that few-shot learning helps works well in reducing the worst-case scenario inefficiencies of the base model.

In the future, I would like to explore the following:

1. Exploring more models: I would like to test more models to see if the improvements seen in the few-shot RAG models are consistent across different LLMs.
2. Different RAG configurations: I would like to explore how far few-shot learning can be pushed in the RAG framework to see when there is a point of diminishing returns.

## TLDR

-   2 experiments were conducted with the following goals:
    1. Fine-tune embeddings models for HPC datasets to improve code retrieval accuracy in code completion tasks.
    2. Assess and improve code generation for HPC tasks using large language models paired with RAG pipelines.
-   For the embeddings fine-tuning experiment my takeaways:
    1. Fine-tuning embeddings models for HPC datasets can improve code retrieval accuracy by double-digit percentage improvements.
    2. Drastically more compute is needed to incorporate semi-similar negative samples in the training process.
-   For the HPC code completions experiment my takeaways:
    1. Few-shot learning within the RAG framework can significantly improve the efficiency of code generated by LLMs by sometimes double-digit percentage improvements.
    2. One-shot learning exhibited adverse effects on the efficiency of code generated by LLMs, seeing single digit percentage decline in efficiency.
    3. Few-shot learning can reduce the worst-case scenario inefficiencies of the base model by double-digit percentage improvements (best case observed >=30%).
