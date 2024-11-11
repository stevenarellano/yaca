import * as assert from 'assert';
import * as vscode from 'vscode';
import {
	generateCompletion,
	generateCompletionWithContext,
} from '../extension';

suite('Extension Test Suite', () => {
	vscode.window.showInformationMessage('Start all tests.');

	test('Sample test', () => {
		assert.strictEqual(-1, [1, 2, 3].indexOf(5));
		assert.strictEqual(-1, [1, 2, 3].indexOf(0));
	});

	test('Generate Completion Test', async () => {
		// Open a new document
		const document = await vscode.workspace.openTextDocument({
			language: 'cpp',
			content: '',
		});
		const editor = await vscode.window.showTextDocument(document);

		// Trigger the generateCompletion function
		await generateCompletion(
			vscode.workspace
				.getConfiguration()
				.get('secretStorage') as vscode.SecretStorage,
		);

		// Verify that the expected text has been added
		const expectedText = 'std::cout << "Hello, VS Code!" << std::endl;';
		const documentText = editor.document.getText();
		assert.strictEqual(
			documentText.includes(expectedText),
			true,
			'Completion text not found in document.',
		);
	});

	test('Generate Completion with Context Test', async () => {
		// Open a new document
		const document = await vscode.workspace.openTextDocument({
			language: 'cpp',
			content: '',
		});
		const editor = await vscode.window.showTextDocument(document);

		// Define a sample message and trigger the generateCompletionWithContext function
		const testMessage = 'Test Message';
		const secretStorage = vscode.workspace
			.getConfiguration()
			.get('secretStorage') as vscode.SecretStorage | undefined;
		if (secretStorage) {
			await generateCompletionWithContext(secretStorage);
		} else {
			throw new Error('SecretStorage is not defined.');
		}

		// Verify that the contextual completion text has been added
		const expectedText = `// Note: ${testMessage}\nstd::cout << "${testMessage}" << std::endl;`;
		const documentText = editor.document.getText();
		assert.strictEqual(
			documentText.includes(expectedText),
			true,
			'Contextual completion text not found in document.',
		);
	});
});
