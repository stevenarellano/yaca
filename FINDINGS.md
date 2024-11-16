# Findings

This file contains information on the research findings of the project. The findings are organized by the following sections:

1. **Embeddings Fine-tuning**: My improvements in creating an embeddings model on HPC datasets.
2. **HPC Code Completions**: My improvements on HPC code generation.

## Embeddings Fine-tuning

This section outlines the process and findings from fine-tuning embeddings models specifically for High-Performance Computing (HPC) datasets, aimed at improving code retrieval accuracy in code completion tasks.

### Experiment Overview

This experiment attempts to improve the embedding's model ability to retrieve relevant code snippets to a given prompt; in this case, the prompt is a code completion task, and the code snippets are the solutions to the task.

The base model used for this experiment is the `all-MiniLM-L6-v2` model from [sentence transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). The model is fine-tuned on two different datasets, both containing code snippets from the `hpc-instruct` dataset. The first dataset contains only C++ code snippets, while the second dataset contains both C++ and Python code snippets. They contain positive samples of "performant" code snippets, and -- AI generated -- negative samples of "non-performant" code snippets. The experiment fine-tunes a linear adapter on top of the base model to optimize the model's performance in retrieving the correct code snippets.

The fine-tuning process involved a few hyperparams that were tuned to optimize the model's performance. Specifically, we experimented with different learning rates, number of epochs, and the presence or absence of negative samples during training. The negative samples chosen were language model generated "non-performant" versions of the solution code. For each model, their hyperparams are listed as follows:

| Adapter File Name                               | Num Epochs | Batch Size | Learning Rate | Warmup Steps | Max Grad Norm | Margin | Use Negatives |
| ----------------------------------------------- | ---------- | ---------- | ------------- | ------------ | ------------- | ------ | ------------- |
| `adapter_cpp_10_lr0.01_negatives.pth`           | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | True          |
| `adapter_cpp_10_lr0.01_no_negatives.pth`        | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | False         |
| `adapter_cpp_5_negatives.pth`                   | 5          | 32         | 0.003         | 100          | 1.0           | 1.0    | True          |
| `adapter_cpp_5_no_negatives.pth`                | 5          | 32         | 0.003         | 100          | 1.0           | 1.0    | False         |
| `adapter_cpp_python_10_lr0.01_negatives.pth`    | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | True          |
| `adapter_cpp_python_10_lr0.01_no_negatives.pth` | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | False         |

### Baseline and Evaluation Metrics

To measure the effectiveness of our fine-tuned model, we compared it against the baseline `all-MiniLM-L6-v2` model in retrieving the correct code (`solution`) from the `hpc-instruct` corpus in a chromadb embeddings database. We evaluated the models on the following metrics:

1. Hit Rate @k: measures whether the correct code is in the top-k retrieved results.
2. Mean Reciprocal Rank @k: measures the average reciprocal rank of the correct code in the top-k retrieved results.
3. Mean Average Precision @k: measures the average precision of the correct code in the top-k retrieved results.
4. Normalized Discounted Cumulative Gain @k: measures the quality of the ranking of the correct code in the top-k retrieved results.

### Experiment Results

I evaluated the models on a variety of k's. The results of the experiment are summarized in the table below:

| Model Type                             | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| -------------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model (cpp)                       | 1   | 0.6164              | 0.6164                  | 0.6164                    | 0.6164          |
| adapter_cpp_10_lr0.01_negatives.pth    | 1   | 0.1330              | 0.1330                  | 0.1330                    | 0.1330          |
| adapter_cpp_10_lr0.01_no_negatives.pth | 1   | 0.7425              | 0.7425                  | 0.7425                    | 0.7425          |
| Base Model (cpp)                       | 3   | 0.6707              | 0.6398                  | 0.6398                    | 0.6478          |
| adapter_cpp_10_lr0.01_negatives.pth    | 3   | 0.1943              | 0.1608                  | 0.1608                    | 0.1714          |
| adapter_cpp_10_lr0.01_no_negatives.pth | 3   | 0.7985              | 0.7676                  | 0.7676                    | 0.7756          |
| Base Model (cpp)                       | 10  | 0.7285              | 0.6500                  | 0.6500                    | 0.6689          |
| adapter_cpp_10_lr0.01_negatives.pth    | 10  | 0.2592              | 0.1641                  | 0.1641                    | 0.2361          |
| adapter_cpp_10_lr0.01_no_negatives.pth | 10  | 0.8406              | 0.7788                  | 0.7788                    | 0.8000          |

| Model Type                                    | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| --------------------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model (cpp_python)                       | 1   | 0.6733              | 0.6733                  | 0.6733                    | 0.6733          |
| adapter_cpp_python_10_lr0.01_negatives.pth    | 1   | 0.0700              | 0.0700                  | 0.0700                    | 0.0700          |
| adapter_cpp_python_10_lr0.01_no_negatives.pth | 1   | 0.7733              | 0.7733                  | 0.7733                    | 0.7733          |
| Base Model (cpp_python)                       | 3   | 0.7358              | 0.6996                  | 0.6996                    | 0.7089          |
| adapter_cpp_python_10_lr0.01_negatives.pth    | 3   | 0.0950              | 0.0807                  | 0.0807                    | 0.0853          |
| adapter_cpp_python_10_lr0.01_no_negatives.pth | 3   | 0.8325              | 0.7993                  | 0.7993                    | 0.8078          |
| Base Model (cpp_python)                       | 10  | 0.7758              | 0.7041                  | 0.7041                    | 0.7215          |
| adapter_cpp_python_10_lr0.01_negatives.pth    | 10  | 0.1383              | 0.0822                  | 0.0822                    | 0.1012          |
| adapter_cpp_python_10_lr0.01_no_negatives.pth | 10  | 0.8517              | 0.7977                  | 0.7977                    | 0.8110          |

### Analysis

In the CPP only corpus, the results show that the `adapter_10_lr0.01_no_negatives.pth` model performed best across all metrics when compared to other other models of the same `k`. One interesting finding was that when incorporating negatives, the model performed poorly. This could be due to the negative samples being too similar to the positive samples. Ultimately, for further use in the HPC code completion testing, the `adapter_10_lr0.01_no_negatives.pth` model will be used.

Meanwhile, in the C++ and Python corpus, the `adapter_cpp_python_10_lr0.01_no_negatives.pth` model outperformed the non-finetuned model across all metrics. It also exhibited better performance than all other models at all `k`'s including the C++ only corpus models. The negative sample version of the linear adapter also performed poorly. The `adapter_cpp_python_10_lr0.01_no_negatives.pth` model will also be used for further testing in the HPC code completion testing to see the impact of incorporating a Python data into the corpus on the model's performance.

I would like to find a way to incorporate negatives in a way that is more beneficial to the model. I propose two potential solutions:

1. Better Negative Sampling Strategy: Instead of using very similar negative samples (with just different performance), use negative samples that are entirely different from the positive samples.
2. Increase model size: The model may be able to differentiate between the current performance and non-performance samples if it is larger.

## HPC Code Completions

This section details the research conducted to assess and improve code generation for High-Performance Computing (HPC) tasks using large language models (LLMs).

### Experiment Overview

The experiment will tests two areas:

1. The effect of a Retrieval-Augmented Generation (RAG) pipeline on the efficiency of code generated by LLMs.
2. The effect the specific code in each corpus has on the efficiency of code generated by LLMs.

First, the experiment utilized [EffiBench](https://github.com/huangd1999/EffiBench), a benchmark suite containing 1,000 efficiency-critical coding problems from LeetCode, to generate code samples. In this stage, we generate code completion for models with RAG and without RAG. The closed source models used include `gpt-4o-mini`, `gpt-4-turbo-preview`, and `gpt-3.5-turbo-0125`. For `gpt-4o-mini`, experiments incorporated a custom Retrieval-Augmented Generation (RAG) pipeline to evaluate if providing additional context could yield more efficient code. This RAG pipeline utilized the `adapter_cpp_10_lr0.01_no_negatives.pth` and `adapter_cpp_python_10_lr0.01_no_negatives.pth` linear adapter from before (paired again with the `all-MiniLM-L6-v2` model) to retrieve performant code snippets from their previously used high performant corpuses, which were then used as context for code generation. Next, we run diagnostics on the generated code to evaluate the efficiency of the code and generate a report on the overhead of each model.

### Baseline and Evaluation Metrics

The experiment evaluated the RAG's pipeline ability to generate efficient code by comparing its completions against those of standalone models of varying sizes.

In comparing the models, the following metrics were used:

-   Execution Time (ET) (milliseconds): The average time taken by the model to execute a task.
-   Normalized Execution Time (NET): The ratio of the model's execution time to the canonical solution's execution time.
-   Maximum Normalized Execution Time (Max_NET): The highest value of NET across all tasks.
-   Percentage of Tasks with NET > 5 (NET>5) (%): The percentage of tasks where the model's execution time is more than five times that of the canonical solution.
-   Memory Usage (MU) (megabyte-seconds, MB·s): The average memory consumption of the model over time during task execution, calculated as the integral of memory usage over time.
-   Normalized Memory Usage (NMU): The ratio of the model's memory usage to the canonical solution's memory usage.
-   Maximum Normalized Memory Usage (Max_NMU): The highest value of NMU across all tasks.
-   Percentage of Tasks with NMU > 5 (NMU>5) (%): The percentage of tasks where the model's memory usage is more than five times that of the canonical solution.
-   Total Max Memory Usage (TMU) (megabytes, MB): The average of the maximum memory usage observed during each task's execution.
-   Normalized Total Max Memory Usage (NTMU): The ratio of the model's maximum memory usage to the canonical solution's maximum memory usage.
-   Maximum Total Memory Usage (Max_TMU) (megabytes, MB): The highest total memory usage recorded across all tasks.
-   Percentage of Tasks with TMU > 5 (TMU>5) (%): The percentage of tasks where the maximum memory usage exceeds 5 MB.
-   Pass Rate (pass1) (%): The percentage of tasks that the model completed successfully without errors.

### Table of Results

The results of the experiment are as follows:

| Model                                                          | ET   | NET  | Max_NET | NET>5 | MU    | NMU  | Max_NMU | NMU>5 | TMU   | NTMU | Max_TMU | TMU>5 | pass1 |
| -------------------------------------------------------------- | ---- | ---- | ------- | ----- | ----- | ---- | ------- | ----- | ----- | ---- | ------- | ----- | ----- |
| **rag3_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini**    | 1.31 | 0.71 | 1.41    | 0.0   | 43.00 | 0.72 | 1.64    | 0.0   | 47.44 | 1.01 | 81.77   | 100.0 | 14.0  |
| **rag2_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini**    | 1.45 | 0.80 | 1.40    | 0.0   | 47.45 | 0.80 | 1.65    | 0.0   | 47.48 | 1.01 | 90.81   | 100.0 | 15.2  |
| **gpt-3.5-turbo-0125**                                         | 1.47 | 0.80 | 2.42    | 0.0   | 48.41 | 0.81 | 2.87    | 0.0   | 47.48 | 1.02 | 119.33  | 100.0 | 12.7  |
| **gpt-4o-mini**                                                | 1.58 | 0.86 | 2.02    | 0.0   | 52.11 | 0.87 | 2.36    | 0.0   | 47.46 | 1.01 | 121.91  | 100.0 | 14.4  |
| **rag1_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini**    | 1.71 | 0.93 | 2.08    | 0.0   | 56.50 | 0.94 | 2.20    | 0.0   | 47.42 | 1.01 | 109.23  | 100.0 | 13.4  |
| **rag1_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini** | 1.72 | 0.95 | 2.33    | 0.0   | 56.80 | 0.96 | 2.50    | 0.0   | 47.45 | 1.01 | 103.88  | 100.0 | 14.1  |
| **rag3_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini** | 1.72 | 0.94 | 1.74    | 0.0   | 56.45 | 0.95 | 1.96    | 0.0   | 47.44 | 1.01 | 98.89   | 100.0 | 13.8  |
| **rag2_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini** | 1.80 | 1.00 | 1.69    | 0.0   | 59.29 | 1.01 | 1.98    | 0.0   | 47.44 | 1.01 | 102.76  | 100.0 | 13.9  |
| **gpt-4-turbo-preview**                                        | 1.95 | 1.07 | 1.93    | 0.0   | 64.03 | 1.08 | 2.18    | 0.0   | 47.45 | 1.01 | 114.98  | 100.0 | 15.2  |

Note, that for the RAG models, they are named as `rag{num}_adapter_{lang}_{num}_lr{num}_no_negatives_{model}`, where `{lang}` indicates the language of the corpus used in the RAG pipeline, `{num}` indicates the number of shots used in the RAG pipeline, and `{model}` indicates the model used in the experiment.

### Analysis

Models utilizing two-shot (`rag2_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini`) and three-shot (`rag3_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini`) learning demonstrated notable improvements over both the base model (`gpt-4o-mini`). The `rag3_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini` model achieved a NET of 0.71, which is approximately a 17% improvement compared to the base model's NET of 0.86. Similarly, `rag2_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini` recorded a NET of 0.80, reflecting about a 7% improvement. In terms of memory efficiency, the few-shot models also outperformed the base model. The `rag3_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini` model achieved an NMU of 0.72, representing a 17% reduction compared to the base model's NMU of 0.87. The `rag2_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini` model had an NMU of 0.80, marking an 8% reduction.

Interestingly, it seemed that one-shot learning had an adverse effect. The `rag1_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini` model showed a NET of 0.93, which is about an 8% slow down compared to the base model's NET of 0.86. Its NMU increased to 0.94, also an 8% increase over the base model. These results suggest that a single example may not provide sufficient context for the model to generalize efficient coding patterns, potentially leading to decreased performance.

In analyzing the effects of the particular corpuses, it seemed that RAG pipelines learning from both C++ and Python code snippets performed much worse than those learning from only C++ code snippets. The RAG pipelines trained on both C++ and Python code snippets (e.g., `rag1_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini`) consistently exhibited higher NET and NMU values compared to those trained exclusively on C++. For example, the `rag3_adapter_cpp_10_lr0.01_no_negatives_gpt-4o-mini` model had a NET of 0.71 and NMU of 0.72, whereas its dual-language counterpart, `rag3_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini`, recorded slightly higher values of 0.94 (NET) and 0.95 (NMU). This trend indicates that the inclusion of Python code snippets introduced additional complexity, likely due to divergent syntactic structures and patterns between the two languages, making it harder for the model to generalize effectively. Moreover, maximum NET and NMU values (Max_NET and Max_NMU) also saw increases in models trained on both C++ and Python, suggesting that certain examples within the Python corpus may be particularly challenging for the model to process. For instance, `rag2_adapter_cpp_10_lr0.01_no_negatives_gpt-4o-mini` had a Max_NET of 1.40 and Max_NMU of 1.65, while its dual-language counterpart, `rag2_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini`, recorded higher values of 1.69 and 1.98, respectively.

Another significant finding is the drastic lowering of the maximum normalized execution time (Max_NET) and maximum normalized memory usage (Max_NMU) in the few-shot RAG models. The `rag3_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini` model had a Max_NET of 1.41, a 30% reduction compared to the base model's Max_NET of 2.02. Its Max_NMU was 1.64, approximately a 31% reduction from the base model's Max_NMU of 2.36. Similarly, `rag2_adapter_cpp_10_lr0.01_no_negatives_and_gpt-4o-mini` showed substantial decreases in these maxima. These reduction indicate that few-shot learning helps works well in reducing the worst-case scenario inefficiencies of the base model.

In the future, I would like to explore the following:

1. Exploring more models: I would like to test more models to see if the improvements seen in the few-shot RAG models are consistent across different LLMs.
2. Different RAG configurations: I would like to explore how far few-shot learning can be pushed in the RAG framework to see when there is a point of diminishing returns.
3. More nuance study of corpus language: I would like to understand how Python-only or other language-only corpuses affect the efficiency of code generated by LLMs.

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
    4. The introduction of Python code snippets can drastically reduce the efficiency of code generated by LLMs.
