# browser-use-web-a11y-agent
Proof-of-concept browser-use web agent for automated accessibility audits

**Overview**
- **Purpose:** Automate quick accessibility audits of web pages using a headless browser and external APIs.
- **Usage:** Run `audit.py` with a target URL; configure API keys via a `.env` file.

**Prerequisites**
- **Python:** Recommended Python 3.8 or newer installed and available on `PATH`.
- **Virtual environment tooling:** `virtualenv` or the standard `venv` module.

**Installation**
- **Clone the repository:**

```powershell
git clone https://github.com/Maryland-State-Innovation-Team/browser-use-web-a11y-agent.git
cd browser-use-web-a11y-agent
```

- **Create a virtual environment (two common options):**

Windows (using `virtualenv`):
```powershell
python -m virtualenv venv
```

Cross-platform (using the standard venv module):
```bash
python -m venv venv
```

- **Activate the virtual environment:**

PowerShell (recommended):
```powershell
.\n+# If using PowerShell, run:
.\n+\venv\Scripts\Activate.ps1
```

Command Prompt (cmd.exe):
```cmd
venv\Scripts\activate.bat
```

Git Bash / macOS / Linux:
```bash
source venv/bin/activate
```

- **Install dependencies:**

```powershell
pip install -r requirements.txt
```

**Environment configuration**
- Copy the example environment file and set your API key(s):

PowerShell:
```powershell
Copy-Item .env-example .env
```

Unix/macOS:
```bash
cp .env-example .env
```

- Open ` .env` and set the following variable at minimum:

- **`GOOGLE_API_KEY`**: Your Google API key used by the project (fill in the value in `.env`).

Example `.env` contents (do not commit secrets):

```
GOOGLE_API_KEY=your_google_api_key_here
```

**Running the auditor**
- The script accepts a URL as the first argument. Example (Windows PowerShell):

```powershell
# Activate the virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# Run the audit
python audit.py https://www.maryland.gov/
```

Or in Command Prompt (cmd.exe):
```cmd
venv\Scripts\activate.bat
python audit.py https://www.maryland.gov/
```

Or on macOS / Linux:
```bash
source venv/bin/activate
python audit.py https://www.maryland.gov/
```

**Options & behavior**
- The tool expects the first positional argument to be a fully-qualified URL (including `http://` or `https://`).
- Output, logging, and any generated artifacts are created in the local working directory unless configured otherwise in the code or environment.

**Contributing**
- Contributions are welcome. Open an issue or submit a pull request with a clear description of changes and rationale.

**License**
- This repository includes a `LICENSE` file in the project root. Follow the license terms provided there.
