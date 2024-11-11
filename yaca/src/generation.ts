import * as vscode from 'vscode';
import { getOrPromptForApiKey } from './api';

export async function generateCompletion(secretStorage: vscode.SecretStorage) {
	const apiKey = await getOrPromptForApiKey(secretStorage);
	if (!apiKey) {
		vscode.window.showErrorMessage(
			'API key is required to use this command.',
		);
		return;
	}

	const editor = vscode.window.activeTextEditor;
	if (!editor) {
		vscode.window.showErrorMessage('No active editor found.');
		return;
	}

	const position = editor.selection.active;
	const completionItem = new vscode.CompletionItem('ExampleCompletion');
	completionItem.insertText = 'std::cout << "Hello, VS Code!" << std::endl;';
	completionItem.detail = 'Inserts a sample print statement';

	editor
		.edit((editBuilder) => {
			editBuilder.insert(position, completionItem.insertText!.toString());
		})
		.then((success) => {
			if (success) {
				vscode.window.showInformationMessage('Completion added!');
			} else {
				vscode.window.showErrorMessage('Failed to add completion.');
			}
		});
}

export async function generateCompletionWithContext(
	secretStorage: vscode.SecretStorage,
) {
	const apiKey = await getOrPromptForApiKey(secretStorage);
	if (!apiKey) {
		vscode.window.showErrorMessage(
			'API key is required to use this command.',
		);
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

	const position = editor.selection.active;
	const completionText = `// Note: ${message}\nstd::cout << "${message}" << std::endl;`;
	const completionItem = new vscode.CompletionItem('ContextCompletion');
	completionItem.insertText = completionText;
	completionItem.detail =
		'Inserts a custom message print statement based on user input';

	editor
		.edit((editBuilder) => {
			editBuilder.insert(position, completionItem.insertText!.toString());
		})
		.then((success) => {
			if (success) {
				vscode.window.showInformationMessage(
					'Contextual completion added!',
				);
			} else {
				vscode.window.showErrorMessage(
					'Failed to add contextual completion.',
				);
			}
		});
}
