import * as vscode from 'vscode';

export const API_KEY_SECRET_KEY = 'yacaApiKey';

export async function getOrPromptForApiKey(
	secretStorage: vscode.SecretStorage,
): Promise<string | undefined> {
	let apiKey = await secretStorage.get(API_KEY_SECRET_KEY);

	if (!apiKey) {
		apiKey = await vscode.window.showInputBox({
			prompt: 'Enter your API key for the YACA extension',
			placeHolder: 'Your API key',
			ignoreFocusOut: true,
			password: true,
		});

		if (apiKey) {
			await secretStorage.store(API_KEY_SECRET_KEY, apiKey);
			vscode.window.showInformationMessage(
				'API key stored successfully.',
			);
		} else {
			vscode.window.showErrorMessage(
				'API key is required to use this extension.',
			);
		}
	}

	return apiKey;
}

export async function resetApiKey(
	secretStorage: vscode.SecretStorage,
): Promise<void> {
	await secretStorage.delete(API_KEY_SECRET_KEY);
	vscode.window.showInformationMessage('API key has been reset.');
}
