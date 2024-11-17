# Findings

This file contains information on the project's research findings; general interest in the code editor `yaca` should start at [./README.md](./README.md). The following sections organize the findings:

1. **Embedding Fine-tuning**: My improvements in creating an embedding model on HPC datasets.
2. **HPC Code Completions**: My improvements on HPC code generation.

## Embedding Fine-tuning

This section outlines the process and findings from fine-tuning embedding models specifically for High-Performance Computing (HPC) datasets to improve code retrieval accuracy in code completion tasks.

### Experiment Overview

This experiment improves the embedding model's ability to retrieve relevant code snippets for a given prompt; in this case, the prompt is a code completion task, and the code snippets are the solutions to the task.

The base model used for this experiment is the `all-MiniLM-L6-v2` model from [sentence transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). The experiment fine-tunes a linear adapter on top of the base model to optimize the model's performance in retrieving the correct code snippets. The model is fine-tuned on three different datasets containing code snippets from the `hpc-instruct` dataset. The first dataset contains only C++ code snippets, the second contains only Python code snippets, and the third contains both C++ and Python. They include positive samples of "performant" code snippets and -- AI-generated -- negative samples of "non-performant" code snippets. After training these fine-tuned models, they are evaluated on their ability to retrieve the correct code snippets from the `hpc-instruct` corpus in a chromadb Embedding database.

The fine-tuning process involved a few hyper-params tuned to optimize the model's performance. Specifically, we experimented with different learning rates, the number of epochs, and the presence or absence of negative samples during training. For each model, their hyper-params are listed as follows:

| Adapter File Name                               | Num Epochs | Batch Size | Learning Rate | Warmup Steps | Max Grad Norm | Margin | Use Negatives |
| ----------------------------------------------- | ---------- | ---------- | ------------- | ------------ | ------------- | ------ | ------------- |
| `adapter_cpp_10_lr0.01_negatives.pth`           | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | True          |
| `adapter_cpp_10_lr0.01_no_negatives.pth`        | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | False         |
| `adapter_cpp_python_10_lr0.01_negatives.pth`    | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | True          |
| `adapter_cpp_python_10_lr0.01_no_negatives.pth` | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | False         |
| `adapter_python_10_lr0.01_negatives.pth`        | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | True          |
| `adapter_python_10_lr0.01_no_negatives.pth`     | 10         | 32         | 0.01          | 100          | 1.0           | 1.0    | False         |

Note that the embedding models are named as `adapter_{language}_{num_epochs}_lr{learning_rate}_{negatives}.pth` where `{language}` is the language of the dataset, `{num_epochs}` is the number of epochs, `{learning_rate}` is the learning rate, and `{negatives}` is whether negatives were used during training.

### Baseline and Evaluation Metrics

To measure the effectiveness of our fine-tuned model, we compared it against the baseline `all-MiniLM-L6-v2` model in retrieving the correct code (`solution`) from the `hpc-instruct` corpus in a chromadb Embedding database. We evaluated the models on the following metrics:

1. Hit Rate @k: measures whether the correct code is in the top-k retrieved results.
2. Mean Reciprocal Rank @k: measures the average reciprocal rank of the correct code in the top-k retrieved results.
3. Mean Average Precision @k: measures the average precision of the correct code in the top-k retrieved results.
4. Normalized Discounted Cumulative Gain @k: measures the quality of ranking the correct code in the top-k retrieved results.

### Experiment Results

I evaluated the models on a variety of k's. The results of the experiment are summarized in the table below separated by the corpus used in training the model (C++-only and C++ and Python):

**C++-only corpus:**

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

**Python-only corpus:**

| Model Type                                | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| ----------------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model (python)                       | 1   | 0.7650              | 0.7650                  | 0.7650                    | 0.7650          |
| adapter_python_10_lr0.01_negatives.pth    | 1   | 0.1783              | 0.1783                  | 0.1783                    | 0.1783          |
| adapter_python_10_lr0.01_no_negatives.pth | 1   | 0.8600              | 0.8600                  | 0.8600                    | 0.8600          |
| Base Model (python)                       | 3   | 0.8250              | 0.7931                  | 0.7931                    | 0.8013          |
| adapter_python_10_lr0.01_negatives.pth    | 3   | 0.2583              | 0.2133                  | 0.2133                    | 0.2249          |
| adapter_python_10_lr0.01_no_negatives.pth | 3   | 0.8900              | 0.8733                  | 0.8733                    | 0.8776          |
| Base Model (python)                       | 10  | 0.8517              | 0.7975                  | 0.7975                    | 0.8107          |
| adapter_python_10_lr0.01_negatives.pth    | 10  | 0.3133              | 0.2220                  | 0.2220                    | 0.2439          |
| adapter_python_10_lr0.01_no_negatives.pth | 10  | 0.9183              | 0.8782                  | 0.8782                    | 0.8878          |

**C++ and Python corpus:**

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

The fine-tuning experiments yielded significant insights into improving code retrieval accuracy for High-Performance Computing (HPC) tasks. Across all three corpora—C++-only, Python-only, and combined C++ and Python—the fine-tuned models trained without negatives consistently outperformed both the baseline models and those trained with negatives. Models fine-tuned without negatives significantly outperformed the baselines across all corpora. In the C++-only corpus at k=1, the Average Hit Rate improved from 0.6164 to 0.7425, a 12.6% increase; similar enhancements were seen at k=3 and k=10. The Python-only model showed a 9.5% increase over the baseline at k=1 (from 0.7650 to 0.8600), and in the combined corpus, the model outperformed the baseline by 14.8% at k=1, demonstrating enhanced retrieval accuracy and ranking across all values of k.

Interestingly, models fine-tuned with negatives performed significantly worse than both the baseline and their counterparts trained without negatives. In the C++-only corpus, adapter_cpp_10_lr0.01_negatives.pth had an Average Hit Rate of 0.1330 at k=1, a stark decline from the baseline's 0.6164. This underperformance remained consistent across all values of k, indicating that the inclusion of negatives adversely affected the model's retrieval ability. The Python-only corpus showed a similar pattern; adapter_python_10_lr0.01_negatives.pth achieved an Average Hit Rate of only 0.1783 at k=1, compared to the baseline's 0.7650. In the combined corpus, adapter_cpp_python_10_lr0.01_negatives.pth recorded an Average Hit Rate of 0.0700 at k=1, significantly lower than the baseline's 0.6733. This detrimental effect persisted across higher values of k, confirming that negative samples negatively impacted the models. This counterintuitive result suggests that the negative samples—AI-generated "non-performant" code snippets—may not have been effective in enhancing the model's discriminative capabilities. Instead of helping the model learn to distinguish between efficient and inefficient code, the negatives might have introduced noise or confusion, hindering its ability to learn useful representations.

To better utilize negative samples and improve the models, we can try several strategies:

1. **Increase the number of epochs**: Extending the training duration could allow the model to learn more robust representations and better distinguish between positives and negatives.
2. **Increase the model's capacity**: Using larger models or more complex architectures could enhance the model's ability to learn intricate distinctions between performant and non-performant code.
3. **Adjusting the dataset**: It is possible that the negative samples used were held nuances that were too subtle for the model to learn effectively. By refining the negative samples to include more distinct differences from the positive samples, the model could learn more effectively.

In conclusion, the fine-tuning experiments demonstrate that models trained without negative samples **significantly enhance code retrieval performance in HPC tasks**.

## HPC Code Completions

This section details the research to assess and improve code generation for High-Performance Computing (HPC) tasks using large language models (LLMs).

### Experiment Overview

The experiment will test two areas:

1. The effect of a Retrieval-Augmented Generation (RAG) pipeline on the efficiency of code generated by LLMs.
2. The effect the specific code in each corpus has on the efficiency of code generated by LLMs (e.g. C++ only vs. Python only vs. C++ and Python).

The experiment first utilizes [EffiBench](https://github.com/huangd1999/EffiBench), a benchmark suite containing 1,000 efficiency-critical coding problems from LeetCode, to generate **python** code samples. In this stage, we generate code completion for models with RAG and without RAG. The closed source models include `gpt-4o-mini`, `gpt-4-turbo-preview`, and `gpt-3.5-turbo-0125`. For `gpt-4o-mini`, experiments also incorporated a custom Retrieval-Augmented Generation (RAG) pipeline to evaluate if providing additional context could yield more efficient code. This RAG pipeline utilized the `adapter_cpp_10_lr0.01_no_negatives.pth`, `adapter_python_10_lr0.01_no_negatives.pth`, and `adapter_cpp_python_10_lr0.01_no_negatives.pth` linear adapter from before (paired again with the `all-MiniLM-L6-v2` model) to retrieve performant code snippets from their previously used high performant corpora, which were then used as context for code generation. Next, we run diagnostics on the generated code to evaluate the efficiency of the code and create a report on the overhead of each model.

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

| Model                                                               | ET   | NET  | Max_NET | NET>5 | MU    | NMU  | Max_NMU | NMU>5 | TMU   | NTMU | Max_TMU | TMU>5 | pass1 |
| ------------------------------------------------------------------- | ---- | ---- | ------- | ----- | ----- | ---- | ------- | ----- | ----- | ---- | ------- | ----- | ----- |
| **full_rag3_adapter_python_10_lr0.01_no_negatives_gpt-4o-mini**     | 1.31 | 0.72 | 1.44    | 0.0   | 42.62 | 0.72 | 1.60    | 0.0   | 47.48 | 1.02 | 90.77   | 100.0 | 13.9  |
| **full_rag2_adapter_python_10_lr0.01_no_negatives_gpt-4o-mini**     | 1.48 | 0.81 | 1.60    | 0.0   | 48.44 | 0.82 | 1.81    | 0.0   | 47.45 | 1.01 | 91.01   | 100.0 | 14.6  |
| **gpt-3.5-turbo-0125**                                              | 1.47 | 0.80 | 2.42    | 0.0   | 48.41 | 0.81 | 2.87    | 0.0   | 47.48 | 1.02 | 119.33  | 100.0 | 12.7  |
| **gpt-4o-mini**                                                     | 1.58 | 0.86 | 2.02    | 0.0   | 52.11 | 0.87 | 2.36    | 0.0   | 47.46 | 1.01 | 121.91  | 100.0 | 14.4  |
| **full_rag2_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini** | 1.69 | 0.92 | 1.95    | 0.0   | 55.66 | 0.93 | 2.26    | 0.0   | 47.40 | 1.01 | 116.88  | 100.0 | 14.3  |
| **full_rag3_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini** | 1.72 | 0.94 | 1.85    | 0.0   | 56.40 | 0.95 | 2.03    | 0.0   | 47.45 | 1.01 | 91.21   | 100.0 | 14.2  |
| **full_rag1_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini** | 1.75 | 0.95 | 1.92    | 0.0   | 57.53 | 0.96 | 2.10    | 0.0   | 47.43 | 1.01 | 98.87   | 100.0 | 14.8  |
| **full_rag1_adapter_python_10_lr0.01_no_negatives_gpt-4o-mini**     | 1.77 | 0.96 | 1.94    | 0.0   | 57.89 | 0.97 | 2.12    | 0.0   | 47.41 | 1.01 | 109.75  | 100.0 | 13.5  |
| **full_rag1_adapter_cpp_10_lr0.01_no_negatives_gpt-4o-mini**        | 1.92 | 1.05 | 2.26    | 0.0   | 63.32 | 1.06 | 2.46    | 0.0   | 47.38 | 1.01 | 111.24  | 100.0 | 13.0  |
| **full_rag2_adapter_cpp_10_lr0.01_no_negatives_gpt-4o-mini**        | 1.92 | 1.06 | 2.08    | 0.0   | 63.13 | 1.07 | 2.27    | 0.0   | 47.36 | 1.01 | 110.57  | 100.0 | 13.7  |
| **gpt-4-turbo-preview**                                             | 1.95 | 1.07 | 1.93    | 0.0   | 64.03 | 1.08 | 2.18    | 0.0   | 47.45 | 1.01 | 114.98  | 100.0 | 15.2  |

Note that the RAG models are named as `rag{num}_adapter_{lang}_{num}_lr{num}_no_negatives_{model}`, where `{lang}` indicates the language of the corpus used in the RAG pipeline, `{num}` shows the number of shots used in the RAG pipeline, and `{model}` indicates the model used in the experiment.

### Analysis

The results of the experiment indicate that utilizing a Retrieval-Augmented Generation (RAG) pipeline with a Python-only code corpus significantly improves the efficiency of code generated by the gpt-4o-mini model. The full_rag3_adapter_python_10_lr0.01_no_negatives_gpt-4o-mini model achieved the lowest Normalized Execution Time (NET) of 0.72, representing approximately a 16% improvement over the base model gpt-4o-mini, which had a NET of 0.86. Similarly, this model also achieved the lowest Normalized Memory Usage (NMU) of 0.72, about a 17% reduction compared to the base model's NMU of 0.87.

In contrast, the RAG models that incorporated C++ code snippets, either alone or in combination with Python code (e.g., full_rag1_adapter_cpp_10_lr0.01_no_negatives_gpt-4o-mini, full_rag2_adapter_cpp_python_10_lr0.01_no_negatives_gpt-4o-mini), exhibited higher NET and NMU values than the base model. For instance, full_rag1_adapter_cpp_10_lr0.01_no_negatives_gpt-4o-mini recorded a NET of 1.05 and an NMU of 1.06, indicating a slowdown and increased memory usage of approximately 22% compared to gpt-4o-mini. This results suggest that the inclusion of C++ code snippets in the RAG pipeline may have introduced complexity or conflicting patterns that hindered the model's ability to generate efficient code.

The maximum normalized execution time (Max_NET) and maximum normalized memory usage (Max_NMU) were also lowest for the full_rag3_adapter_python_10_lr0.01_no_negatives_gpt-4o-mini model, with values of 1.44 and 1.60, respectively. This suggests that the worst-case performance scenarios were improved by using the Python-only RAG pipeline.

Analyzing the pass rates (pass1) shows low results across all models, ranging from 12.7% to 15.2%, indicating that while efficiency improved, overall task success rates remain an area for further enhancement.

These findings suggest that providing Python code snippets as additional context in a RAG pipeline helps the model generate more efficient code. The structural simplicity and readability of Python may make it easier for the model to learn and generalize efficient coding patterns. In contrast, including C++ code snippets -- even when Python snippets are still in the corpus -- appears to negatively impact the efficiency of the generated code.

Based on these results, future research could explore the following:

1. Deeper Analysis of Corpus Content: Investigate the specific characteristics of the Python and C++ code in the corpora to understand why Python code snippets enhance performance while C++ snippets do not.
2. Expansion to Other Programming Languages: Examine the effects of incorporating code snippets from other programming languages, such as Java or Go, to see if similar improvements can be achieved.
3. Optimization of RAG Configuration: Experiment with different numbers of shots and retrieval strategies in the RAG pipeline to identify the optimal configuration for maximizing code efficiency.
4. Error Analysis: Conduct a detailed analysis of the tasks where models failed (low pass rates) to identify common failure modes and inform strategies to improve success rates.

As an additional note, the need for a C++-based oriented benchmark suite, similar to EffiBench, is required to further investigate the impact of C++ code snippets on code generation efficiency.

## TLDR

-   2 experiments were conducted with the following goals:
    1. Fine-tune embedding models for HPC datasets to improve code retrieval accuracy in code completion tasks.
    2. Assess and improve code generation for HPC tasks using large language models paired with RAG pipelines.
-   **Embedding Fine-tuning**:
    1. Fine-tuning models on HPC datasets without negative samples significantly improves code retrieval accuracy over baseline models across all languages.
    2. Including negative samples during fine-tuning degrades model performance, causing worse results than both the baseline and models trained without negatives.
    3. To improve models when using negatives, strategies such as increasing training epochs, enhancing model capacity, and refining negative samples are recommended.
-   **HPC Code Completions**:
    1. Using a Python-only RAG pipeline significantly enhances code efficiency (in python-only code generation scenarios), reducing execution time and memory usage in code generated by the gpt-4o-mini model.
    2. Including C++ code snippets in the RAG pipeline reduces efficiency, increasing execution time and memory usage in generated code.
