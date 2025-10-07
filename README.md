# Resume Gap Analyzer MCP Server

An MCP (Model Context Protocol) server that analyzes resumes against job descriptions to identify gaps, missing keywords, and improvement opportunities using OpenAI's GPT-4o-mini.

<iframe width="560" height="315" src="https://www.youtube.com/embed/JnteMtI5nCs?si=hB1p5CdMmHGAyZlA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Features

- **Gap Analysis**: Identifies missing skills, experience, certifications, and keywords
- **Prioritized Recommendations**: Actionable feedback organized by impact
- **ATS Optimization**: Ensures resume compatibility with Applicant Tracking Systems
- **Strength Mapping**: Highlights existing qualifications to emphasize
- **Sample Resume Resources**: Test with pre-loaded sample resumes

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd gapsinmyresume
```

2. **Create and activate a virtual environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set your OpenAI API key**:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your actual API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

### Configuration for Claude Desktop

To use this MCP server with Claude Desktop, add it to your config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "resume-gap-analyzer": {
      "command": "/absolute/path/to/gapsinmyresume/.venv/bin/python",
      "args": ["/absolute/path/to/gapsinmyresume/server.py"]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/gapsinmyresume` with your actual path. Use the `.venv/bin/python` from the virtual environment you created.

After updating the config, **restart Claude Desktop** for changes to take effect.

## Usage

### Option 1: Via Claude Desktop (Recommended)

Once configured, simply ask Claude in the desktop app:

```
"Analyze my resume at /Users/you/Documents/resume.docx against this job description:

[paste full job description here]"
```

Claude will automatically use the `analyze_resume_gaps` tool.

### Option 2: Direct CLI Testing

Run the included test script to test without Claude Desktop:

```bash
# Make sure your .env file has OPENAI_API_KEY set
source .venv/bin/activate
python test_cli.py
```

This will analyze the first resume in `sample-resumes/` against a sample job description.

### Option 3: MCP Server Directly

Start the MCP server (for debugging or integration):

```bash
source .venv/bin/activate
python server.py
```

The server runs in stdio mode and accepts MCP protocol messages.

### Tool Parameters

**`analyze_resume_gaps`**
- `resume_path` (string, required): Absolute path to resume file (.docx)
- `job_description` (string, required): Full text of the job posting

**Example in Claude Desktop:**
```
"Analyze /Users/you/Documents/resume.docx for the Senior Software Engineer role at XYZ Corp.

Job description:
We are seeking a Senior Software Engineer with 5+ years of experience in Python, AWS, and React..."
```

## Output Format

The tool returns structured JSON with:

```json
{
  "overall_match_score": 75,
  "critical_gaps": [
    {
      "category": "hard_skill",
      "gap": "AWS certification missing",
      "importance": "high",
      "recommendation": "Obtain AWS Solutions Architect certification",
      "keywords_to_add": ["AWS", "cloud architecture", "EC2"]
    }
  ],
  "missing_keywords": {
    "technical": ["Kubernetes", "Docker", "CI/CD"],
    "soft_skills": ["leadership", "mentoring"],
    "industry_terms": ["agile", "scrum"]
  },
  "experience_analysis": {
    "required_years": 5,
    "resume_shows_years": 3,
    "gap_exists": true,
    "notes": "Resume shows 3 years but requires 5+"
  },
  "strengths_to_highlight": [
    {
      "strength": "Python expertise",
      "relevance": "Primary language for the role",
      "current_prominence": "medium",
      "recommendation": "Move Python projects to top of experience section"
    }
  ],
  "formatting_suggestions": [
    {
      "issue": "No clear metrics in achievements",
      "impact": "both",
      "fix": "Add quantifiable results (e.g., 'Improved performance by 40%')"
    }
  ],
  "content_improvements": [
    {
      "section": "Professional Summary",
      "current_state": "Generic software engineer summary",
      "suggested_change": "Emphasize Python, AWS, and senior-level leadership",
      "example": "Senior Software Engineer with 3+ years specializing in Python-based cloud solutions...",
      "priority": "high"
    }
  ],
  "quick_wins": [
    "Add 'AWS' keyword to technical skills section",
    "Quantify achievement in Project X with metrics",
    "Reorder skills to match job description priority"
  ],
  "summary": "Strong Python foundation but needs more AWS experience. Highlight existing cloud projects and add relevant certifications. Focus on quantifying achievements."
}
```

## Development

```bash
# Run the server directly (for testing)
python server.py

# Format code
black server.py prompts.py

# Lint code
ruff check .
```

## File Structure

```
gapsinmyresume/
├── server.py                           # Main FastMCP server implementation
├── prompts.py                          # System prompts and Pydantic models
├── test_cli.py                         # CLI test script
├── sample-resumes/                     # Place sample .docx files here
├── sample-job-descriptions/            # Example job descriptions
│   └── senior-software-engineer.txt
├── pyproject.toml                      # Python project configuration
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── .env                                # Your API keys (git ignored)
├── README.md                           # This file
└── SETUP.md                            # Additional setup notes
```

## How It Works

1. **Document Parsing**: Extracts text from DOCX files using python-docx
2. **LLM Analysis**: Sends resume and job description to OpenAI gpt-4o-mini
3. **Structured Output**: Uses Pydantic models with OpenAI's structured output API
4. **MCP Integration**: FastMCP exposes analysis as a tool callable from Claude Desktop

## Tips for Best Results

- Provide complete job descriptions (not just titles)
- Ensure resume files are properly formatted .docx files
- Include both required and preferred qualifications in job description
- Use the quick wins section for immediate, high-impact changes
- Place test resumes in `sample-resumes/` to use the resource feature

## Quick Start Example

After setup, try this:

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Run the test script (uses sample resume + sample job description)
python test_cli.py

# 3. Or use with Claude Desktop
# Just ask: "Analyze my resume at /path/to/resume.docx against this job description: [paste description]"
```

## Testing with Sample Resumes

1. Add `.docx` files to the `sample-resumes/` directory
2. Sample job descriptions are in `sample-job-descriptions/`
3. Run `python test_cli.py` for quick testing
4. In Claude Desktop, reference your resume files by absolute path

## License

MIT
