import * as vscode from 'vscode';

import { resetApiKey } from './api';
import { generateCompletion, generateCompletionWithChat } from './generation';

export async function activate(context: vscode.ExtensionContext) {
	console.log('Congratulations, your extension "yaca" is now active!');

	const disposable = vscode.commands.registerCommand(
		'yaca.helloWorld',
		() => {
			vscode.window.showInformationMessage('Hello World from yaca!');
		},
	);
	context.subscriptions.push(disposable);

	const completionDisposable = vscode.commands.registerCommand(
		'yaca.generateCompletion',
		() => generateCompletion(context.secrets),
	);
	context.subscriptions.push(completionDisposable);

	const contextCompletionDisposable = vscode.commands.registerCommand(
		'yaca.generateCompletionWithChat',
		() => generateCompletionWithChat(context.secrets),
	);
	context.subscriptions.push(contextCompletionDisposable);

	const resetDisposable = vscode.commands.registerCommand(
		'yaca.resetApiKey',
		() => resetApiKey(context.secrets),
	);
	context.subscriptions.push(resetDisposable);
}

export function deactivate() {}
