---
title: Template Final Assignment
emoji: 🕵🏻‍♂️
colorFrom: indigo
colorTo: indigo
sdk: gradio
sdk_version: 5.25.2
app_file: app.py
pinned: false
hf_oauth: true
# optional, default duration is 8 hours/480 minutes. Max duration is 30 days/43200 minutes.
hf_oauth_expiration_minutes: 480
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# GAIA Agent for Hugging Face Agents Course

This project implements a powerful intelligent agent using the SmolAgents framework to tackle the GAIA benchmark questions for the Hugging Face Agents course final assessment.

## Project Overview

The GAIA benchmark consists of challenging questions that require an agent to use various tools, including web search, file processing, and reasoning capabilities. This agent is designed to:

1. Receive questions from the GAIA API
2. Process and understand the questions
3. Use appropriate tools to find answers
4. Format and return precise answers

## Features

- **LangChain Integration**: Uses CodeAgent for flexible problem-solving with Python code execution
- ** OpenAI Model support**: OpenAI models (GPT-4o and others)
- **Enhanced Tool Suite**:
  - Web search via DuckDuckGo
- **Flexible Environment Configuration**:
  - Easy setup via environment variables or .env file
  - Fallback mechanisms for missing dependencies
  - Support for both local and secure E2B code execution
- **Answer Processing**:
  - Special handling for reversed text questions
  - Precise answer formatting for benchmark submission
  - Automatic cleanup of model responses for exact matching
- **Interactive UI**: Gradio interface for running the agent and submitting answers

## Setup

### Prerequisites

- Python 3.8+
- Hugging Face account
- API keys for your preferred models (HuggingFace, OpenAI)

### Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example environment file and add your API keys:

```bash
cp env.example .env
# Edit .env with your API keys and configuration
```

### Configuration

Configure the agent by setting these environment variables or editing the `.env` file:

#### API Keys
```
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
OPENAI_API_KEY=your_openai_key_here
XAI_API_KEY=your_xai_api_key_here  # For X.AI/Grok models
```

#### Agent Configuration
```
AGENT_MODEL_TYPE=OpenAIServerModel  # HfApiModel, InferenceClientModel, LiteLLMModel, OpenAIServerModel
AGENT_MODEL_ID=gpt-4o  # Model ID depends on the model type
AGENT_TEMPERATURE=0.2
AGENT_EXECUTOR_TYPE=local  # local or e2b for secure execution
AGENT_VERBOSE=true  # Set to true for detailed logging
```

#### Advanced Configuration
```
AGENT_PROVIDER=hf-inference  # Provider for InferenceClientModel
AGENT_TIMEOUT=120  # Timeout in seconds for API calls
AGENT_API_BASE=https://api.groq.com/openai/v1  # For X.AI when using OpenAIServerModel
```

### Hugging Face Spaces Setup

When deploying to Hugging Face Spaces, you need to add your API keys as secrets:

1. Go to your Space's Settings → Repository Secrets
2. Add the following secrets (add at least one of these API keys):
   - `HF_TOKEN` - Your Hugging Face API token
   - `OPENAI_API_KEY` - Your OpenAI API key

3. Add additional configuration secrets as needed:
   - `AGENT_MODEL_TYPE` - Model type (e.g., "OpenAIServerModel")
   - `AGENT_MODEL_ID` - Model ID to use (e.g., "gpt-4o")
   - `AGENT_TEMPERATURE` - Temperature setting (e.g., "0.2")
   - `AGENT_VERBOSE` - Set to "true" for detailed logging

4. **Important**: If you're using OpenAIServerModel, ensure the requirements.txt includes:
   ```
langchain[openai]
openai
   ```

   If the space gives an error about OpenAI modules, rebuild the space after updating requirements.txt.


## Usage

### Running the Agent

Launch the Gradio interface with:

```bash
python app.py
```

Then:
1. Log in to your Hugging Face account using the button in the interface
2. Click "Run Evaluation & Submit All Answers"

### Testing

To test the agent with sample questions before running the full evaluation:

```bash
python test_agent.py
```

## Project Structure

- `app.py`: Main application with Gradio interface
- `core_agent.py`: Agent implementation with LangChain framework
- `test_agent.py`: Testing script with sample questions
- `requirements.txt`: Project dependencies

## Tools Implementation

The agent includes several custom tools:

### Implemented Tools

### Tools to be implemented

1. **save_and_read_file**: Save content to a temporary file and return the path
2. **download_file_from_url**: Download a file from a URL and save it locally
3. **extract_text_from_image**: OCR for extracting text from images (requires pytesseract)
4. **analyze_csv_file**: Load and analyze CSV files using pandas
5. **analyze_excel_file**: Load and analyze Excel files using pandas

## Resources

- [GAIA Benchmark Information](https://huggingface.co/spaces/gaia-benchmark/leaderboard)
- [SmolAgents Documentation](https://huggingface.co/docs/smolagents/en/index)
- [Hugging Face Agents Course](https://huggingface.co/agents-course)

## License

This project is licensed under the MIT License.