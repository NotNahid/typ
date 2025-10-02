# TypiDesk

TypiDesk is a lightweight, universal desktop assistant that lets users transform text with simple inline commands. Instead of switching apps or copy-pasting into AI tools, users just type normally, append a command like `?polite`, `?fix`, or `?summ` at the end of their text, and TypiDesk instantly rewrites or processes it using AI.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set the Gemini API Key:**
    You need to set the `GEMINI_API_KEY` environment variable to your Gemini API key.
    You can get a free API key at: https://makersuite.google.com/app/apikey

    On Linux and macOS, you can set the environment variable like this:
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```

    On Windows, you can use this command:
    ```powershell
    $env:GEMINI_API_KEY="YOUR_API_KEY"
    ```

3.  **Run the script:**
    ```bash
    python typiDesk.py
    ```

## Usage (New Real-time Mode)

1.  Run the `typiDesk.py` script. It will run in the background.
2.  Go to any application or text box.
3.  Type your text and end it with a command (e.g., `this is a test?fix`).
4.  Press the **Spacebar** key.
5.  TypiDesk will automatically delete what you just typed and write the AI-transformed text in its place.