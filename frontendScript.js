async function runScript() {
    const response = await fetch('/run-script', { method: 'POST' });
    const result = await response.json();

    if (result.status === 'success') {
        alert("Script Output: " + result.output);
    } else {
        alert("Error: " + result.error);
    }
}