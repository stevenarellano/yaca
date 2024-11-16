# yaca-backend

Yaca-Backend is the server-side component of the code assistant Yaca. Its responsible for providing code completions to the Visual Studio Code extension. This backend utilizes a RAG pipeline to generate highly performance code for the user's query.

It uses a custom C++ and Python corpus based on highly performant code from the [hpcgroup/hpc-instruct](https://huggingface.co/datasets/hpcgroup/hpc-instruct) dataset. Further details can be found in the `<ROOT>/model` directory.

## Architecture

The Yaca-Backend is structured as a Flask application, providing a lightweight and scalable server environment to handle code completion requests from the Yaca VS Code extension.

1. **Language Model**: The backend leverages OpenAI's GPT language model to generate code completions and responses. This model is tuned to interpret and complete code queries, providing relevant, high-quality output. The model of choice is the `gpt-4o-mini` model.

2. **Embeddings Database**: To enhance response accuracy and relevance, Yaca-Backend integrates [ChromaDB](https://www.trychroma.com/) as an embeddings database. ChromaDB stores precomputed embeddings from the custom C++ corpus. To create the emebddings, this code uses a custom embeddings adapter located in the `./adapters/` directory and utilizes code data from `./data/training_data.json`.

3. **Retrieval-Augmented Generation (RAG) Pipeline**: The pipeline follows a RAG architecture to generate responses:
    - **Step 1**: When a code query is received, relevant embeddings are retrieved from ChromaDB based on similarity to the input.
    - **Step 2**: These embeddings, combined with a carefully crafted prompt, are sent to the GPT model.
    - **Step 3**: GPT generates code completions that align with both the query and the context provided by the retrieved embeddings.

This approach provides efficient and contextually aware code completions, making Yaca-Backend a powerful tool for code assistance.

## Installation and Use

To set up and run Yaca-Backend, follow these steps:

```bash
# from the <ROOT> of this github repo
pip3 install -r requirements.txt
cd yaca-backend
python3 app.py
```
