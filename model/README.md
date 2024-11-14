# About

This is the repository for fine-tuning our embeddings model. It will be used in our RAG pipeline for code generation.

# `code/`

## `code/synthetic-data.ipynb`

The purpose of this notebook is to generate synthetic data for training our embeddings' adapter. In the RAG pipeline, we will use the user's intent and code location to generate completions.

Initially, the RAG pipeline will use an input such as the following:

```
Generate fill a vector with integers from 0 to 999
```

In this example, we'd like to retrieve code related to filling out vectors of fixed length. There may be future plans to enhance this input with additional context, such as the current document's contents or metadata on the user's project.

Hence, the synthetic data pipeline will look to generate highly performant positive and negative code examples for the embeddings model.

## `code/train.ipynb`

This notebook will be used to train the embeddings' adapter.

To start, this will take inspiration from Chroma's [Embedding Adapters Technical Report](https://research.trychroma.com/embedding-adapters), we will train a query-only adapter using positive and negative samples.

Future work will involve training different types of adapters, full fine-tuning, and different datasets.

## `code/evaluation.ipynb`

This notebook evaluates how well different embeddings adapters perform at retrieving the proper code completions relative to a base embeddings model.

## `code/few_shots.py`

This program contains few-shot examples of performant code.

## `code/utils.py`

This program contains shared utilities between the notebooks.

## Workflows

0. Before Running Any Notebooks

Before running any notebooks, ensure that you have the following dependencies installed:

```bash
# from the <ROOT> of this github repo
pip3 install -r requirements.txt
cd model
touch secret.json # add your openai api key under the key "OPEN_AI_API_KEY"
```

1. Generating Synthetic Data:

Run the `synthetic-data.ipynb` notebook to generate synthetic data for training the embeddings' adapter.

2. Training the Adapter:

Run the `train.ipynb` notebook to train the embeddings' adapter.

3. Evaluating the Adapter:

Run the `evaluation.ipynb` notebook to evaluate the embeddings' adapter.
