# About

This is the repository for fine-tuning our embeddings model. It will be used in our RAG pipeline for code generation.

See `../DESIGN.md` for more information on how RAG is used in this project.

# Notebooks

## `notebooks/synthetic-data.ipynb`

The purpose of this notebook is to generate synthetic data for training our embeddings' adapter. In the RAG pipeline, we will use the user's intent and code location to generate completions.

Initially, the RAG pipeline will use an input such as the following:

```
Generate fill a vector with integers from 0 to 999
```

In this example, we'd like to retrieve code related to filling out vectors of fixed length. There may be future plans to enhance this input with additional context, such as the current document's contents or metadata on the user's project.

Hence, the synthetic data pipeline will look to generate highly performant positive and negative code examples for the embeddings model.

## `notebooks/train.ipynb`

This notebook will be used to train the embeddings' adapter.

To start, this will take inspiration from Chroma's [Embedding Adapters Technical Report](https://research.trychroma.com/embedding-adapters), we will train a query-only adapter using positive and negative samples.

Future work will involve training different types of adapters, full fine-tuning, and different datasets.

## `notebooks/evaluate.ipynb`

This notebook will be used to evaluate our embeddings models in a RAG-like pipeline.
