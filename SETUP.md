# Quick Setup Guide

## Installation Complete! ✓

Your Python 3.11 conda environment is ready with all dependencies installed.

## Next Steps

### 1. Set your OpenAI API Key

Create a `.env` file:
```bash
cp .env.example .env
```

Then edit `.env` and add your API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. Test the Server

Activate the environment and run:
```bash
conda activate resume-analyzer
python server.py
```

### 3. Add to Claude Desktop

Edit your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "resume-gap-analyzer": {
      "command": "/opt/anaconda3/envs/resume-analyzer/bin/python",
      "args": ["/Users/pardhuvarma/Downloads/buildmcpservers/gapsinmyresume/server.py"]
    }
  }
}
```

Note: Replace the path with your actual path if different.

### 4. Add Sample Resumes (Optional)

Place `.docx` resume files in the `sample-resumes/` directory to test with resources.

### 5. Restart Claude Desktop

After adding the MCP server config, restart Claude Desktop to load the server.

## Usage in Claude Desktop

Once configured, you can use the tool:

**Tool**: `analyze_resume_gaps`
- `resume_path`: Full path to your .docx resume file
- `job_description`: The complete job posting text

**Resources**: Access sample resumes via `resume://sample-{filename}`

## Troubleshooting

**If the server doesn't show up in Claude Desktop:**
1. Check Claude Desktop logs for errors
2. Verify the paths in the config are correct
3. Make sure the .env file has your API key
4. Restart Claude Desktop

**To test manually:**
```bash
conda activate resume-analyzer
python server.py
```

The server should start without errors (will wait for MCP client connection).
