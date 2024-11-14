from openai import OpenAI

from retrieval_service import RetrievalService


class GenerationService:
    def __init__(self, retrieval_service: RetrievalService):
        self.retrieval_service = retrieval_service

    def generate_prompt(self, document_text, message=None, k=2) -> str:
        base_prompt = (
            "You are an AI code assistant that provides code completions. "
            "Your task is to replace the '___' in the code with the appropriate code completion. "
            "Only provide the code that should replace '___', without any additional explanations or text. "
            "Do not include any backticks, language descriptors, or repeat existing code."
        )

        examples = self.retrieval_service.retrieve_context(document_text, k)
        examples_text = "\n\n".join(
            [f"Example {i+1}:\n{example}" for i,
                example in enumerate(examples)]
        )

        if message:
            prompt = (
                f"{base_prompt}\n\nHere are some relevant examples:\n\n{examples_text}\n\n"
                f"Based on the following code and the message '{message}', provide the code that should replace '___':\n\n{document_text}"
            )
        else:
            prompt = (
                f"{base_prompt}\n\nHere are some relevant examples:\n\n{examples_text}\n\n"
                f"Provide the code that should replace '___' in the following code:\n\n{document_text}"
            )

        return prompt

    def generate_completion(self, api_key, document_text) -> str | None:
        openai = self.get_openai_client(api_key)
        prompt = self.generate_prompt(document_text)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_completion_with_chat(self, api_key, document_text, message) -> str | None:
        openai = self.get_openai_client(api_key)
        prompt = self.generate_prompt(document_text, message)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def get_openai_client(self, api_key):
        return OpenAI(api_key=api_key)
