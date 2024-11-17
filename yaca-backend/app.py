from typing import Literal
import torch
from sentence_transformers import SentenceTransformer
from flask_cors import CORS
from flask import Flask, Response, request, jsonify

from retrieval_service import RetrievalService
from generation_service import GenerationService
from linear_adapter import LinearAdapter

CORPUS_DATA_PATH = './data/cpp_python_corpus_data.json'
ADAPTER_FILE = './adapters/adapter_cpp_10_lr0.01_no_negatives.pth'
COLLECTION_NAME = 'cpp_python'


class YacaBackend:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        CORS(self.app)

        base_model = SentenceTransformer('all-MiniLM-L6-v2')
        adapter = LinearAdapter(
            base_model.get_sentence_embedding_dimension())
        adapter.load_state_dict(torch.load(ADAPTER_FILE)['adapter'])

        self.generation_service = GenerationService(
            retrieval_service=RetrievalService(
                json_data_path=CORPUS_DATA_PATH,
                base_model=base_model,
                adapter=adapter,
                collection_name=COLLECTION_NAME
            )
        )

        self.setup_routes()

    def setup_routes(self) -> None:
        @self.app.route('/generate-completion', methods=['POST'])
        def completion() -> tuple[Response, Literal[400]] | Response:
            print("Received request")
            data = request.json
            api_key = data.get("api_key")
            document_text = data.get("document")

            if not api_key or not document_text:
                return jsonify({"error": "API key and document text are required"}), 400

            result = self.generation_service.generate_completion(
                api_key, document_text)
            return jsonify({"completion": result})

        @self.app.route('/generate-completion-with-chat', methods=['POST'])
        def completion_with_chat() -> tuple[Response, Literal[400]] | Response:
            data = request.json
            api_key = data.get("api_key")
            document_text = data.get("document")
            message = data.get("message")

            if not api_key or not document_text or not message:
                return jsonify({"error": "API key, document text, and message are required"}), 400

            result = self.generation_service.generate_completion_with_chat(
                api_key, document_text, message)
            return jsonify({"completion": result})

    def run(self) -> None:
        self.app.run(debug=True)


if __name__ == '__main__':
    app = YacaBackend()
    app.run()
