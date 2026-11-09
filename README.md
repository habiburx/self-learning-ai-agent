# Self-Learning AI Agent

long term goal making a self learning agent using mem0 architecture (https://arxiv.org/pdf/2504.19413)
A command line search assistant built with LangChain and Groq. It accepts a
question, can use web search and Wikipedia tools, and formats its final response
as a structured report with a topic, summary, sources, and the tools used. A
file saving tool is also available to the agent.

## Requirements

- Python 3.11 or newer
- A Groq API key
- Internet access for Groq and external search/Wikipedia requests

## Setup

Run these commands from the project directory.

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

The script uses the Groq model `openai/gpt-oss-20b`. The OpenAI and Anthropic
integrations are listed as alternatives in the source, but are not used by the
current configuration. Do not commit `.env` or share your API key.

## Run

With the virtual environment activated:

```bash
python -m src.main
```

Enter a research question at the prompt. The agent prints a structured report
when the model returns a response that matches the report schema.

## Project files

- `src/main.py` — configures the Groq model and research agent, prompts for a
  question, runs the agent, and parses the final report.
- `src/tools.py` — defines the DuckDuckGo search, Wikipedia, and text-file saving
  tools.
- `output/response.txt` — each successfully parsed report is appended here; the
  `output/` directory is created as needed.
- `src/__init__.py` — makes the source directory an importable Python package.
- `requirements.txt` — Python package dependencies.
- `.env.example` — environment variable template; copy it to `.env` and add
  credentials.

## Reproducibility

To recreate the environment, follow the setup steps in a fresh virtual
environment and run `python -m src.main`. `requirements.txt` lists dependencies
but does not pin exact package versions, so installs made at different times
can resolve to different versions. For identical dependency versions across
machines, generate and maintain a lock file after validating the environment.
Model output and web results can also vary between runs.
