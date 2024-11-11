# User Flows

## User Creates a Completion Request

1. User runs one of the completion commands and provides a prompt if applicable.
2. The extension captures the user's current file context and the prompt.
3. The extension generates a summarization of user's intent.
4. The extension uses RAG for the following:
    1. Retrieve relevant code snippets from the codebase.
    2. Retrieve code snippets from a corpus that are relevant to the user's intent.
5. The extension generates a completion based on the summarization and the retrieved code snippets.
6. The extension presents the completion to the user.

# Trade offs Considered

## HPC-Enhanced RAG or HPC-Enhanced Inference Model

-   Papers: HPC Coder, A Systematic Evaluation of Large Language Models of Code
-   ParEval:

## To Answer

-   Difference in performance of fine-tuning vs. RAG
-   Few-shot vs. fine-tuning
