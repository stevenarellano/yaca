import * as vscode from 'vscode';
import axios from 'axios';
import * as dotenv from 'dotenv';
import * as path from 'path';

dotenv.config({ path: path.resolve(__dirname, '..', '.env') });
const BASE_URL = process.env.BACKEND_URL_BASE;

interface GenerateCompletionRequest {
	api_key: string;
	document: string;
}

interface GenerateCompletionResponse {
	completion: string;
}

interface GenerateCompletionWithChatRequest {
	api_key: string;
	document: string;
	message: string;
}

interface GenerateCompletionWithChatResponse {
	completion: string;
}

async function getOrPromptForApiKey(
	secretStorage: vscode.SecretStorage,
): Promise<string | null> {
	let apiKey = await secretStorage.get('openai-api-key');
	if (!apiKey) {
		apiKey = await vscode.window.showInputBox({
			prompt: 'Enter your OpenAI API key',
			ignoreFocusOut: true,
			password: true,
		});
		if (apiKey) {
			await secretStorage.store('openai-api-key', apiKey);
		} else {
			vscode.window.showErrorMessage(
				'API key is required to use this command.',
			);
			return null;
		}
	}
	return apiKey;
}

export async function generateCompletion(secretStorage: vscode.SecretStorage) {
	const apiKey = await getOrPromptForApiKey(secretStorage);
	if (!apiKey) {
		return;
	}

	const editor = vscode.window.activeTextEditor;
	if (!editor) {
		vscode.window.showErrorMessage('No active editor found.');
		return;
	}

	const documentText = editor.document.getText();
	const position = editor.selection.active;

	// Insert '___' at the cursor position in the documentText
	const offset = editor.document.offsetAt(position);
	const modifiedDocumentText =
		documentText.slice(0, offset) + '___' + documentText.slice(offset);

	const requestData: GenerateCompletionRequest = {
		api_key: apiKey,
		document: modifiedDocumentText,
	};

	try {
		const response = await axios.post<GenerateCompletionResponse>(
			`${BASE_URL}/generate-completion`,
			requestData,
		);
		console.log(`Response: ${JSON.stringify(response.data)}`);
		const completionText = response.data.completion;

		if (!completionText) {
			vscode.window.showErrorMessage(
				'Received empty completion from backend.',
			);
			return;
		}

		await editor.edit((editBuilder) => {
			editBuilder.insert(position, completionText);
		});

		vscode.window.showInformationMessage('Completion added!');
	} catch (error) {
		vscode.window.showErrorMessage(
			'Failed to get completion from backend.',
		);
		console.error(error);
	}
}

export async function generateCompletionWithChat(
	secretStorage: vscode.SecretStorage,
) {
	const apiKey = await getOrPromptForApiKey(secretStorage);
	if (!apiKey) {
		return;
	}

	const editor = vscode.window.activeTextEditor;
	if (!editor) {
		vscode.window.showErrorMessage('No active editor found.');
		return;
	}

	const message = await vscode.window.showInputBox({
		prompt: 'Enter a custom message for the completion',
		placeHolder: 'Type your message here...',
	});
	if (!message) {
		vscode.window.showInformationMessage(
			'No message provided. Command cancelled.',
		);
		return;
	}

	const documentText = editor.document.getText();
	const position = editor.selection.active;

	// Insert '___' at the cursor position in the documentText
	const offset = editor.document.offsetAt(position);
	const modifiedDocumentText =
		documentText.slice(0, offset) + '___' + documentText.slice(offset);

	const requestData: GenerateCompletionWithChatRequest = {
		api_key: apiKey,
		document: modifiedDocumentText,
		message: message,
	};

	try {
		const response = await axios.post<GenerateCompletionWithChatResponse>(
			`${BASE_URL}/generate-completion-with-chat`,
			requestData,
		);

		const completionText = response.data.completion;

		if (!completionText) {
			vscode.window.showErrorMessage(
				'Received empty completion from backend.',
			);
			return;
		}

		// Insert the completion at the cursor position
		await editor.edit((editBuilder) => {
			editBuilder.insert(position, completionText);
		});

		vscode.window.showInformationMessage('Contextual completion added!');
	} catch (error) {
		vscode.window.showErrorMessage(
			'Failed to get completion from backend.',
		);
		console.error(error);
	}
}
