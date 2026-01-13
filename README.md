# ElectriAI Research

A research project analyzing YouTube video transcripts and comments related to electrical construction, using GPT-based analysis for topic extraction and thematic classification.

## Project Structure

```
ElectriAI_Research/
├── notebooks/
│   ├── 01_Data_Collection.ipynb      # Collect YouTube URLs, transcripts, and comments
│   ├── 02_Transcript_Analysis.ipynb  # Summarize transcripts and extract topics
│   ├── 03_Comment_Analysis.ipynb     # Analyze comments with transcript context
│   └── 04_Theme_Dictionary.ipynb     # Classify comments into themes
├── data/
│   ├── raw/                          # Input data (videos, transcripts, comments)
│   ├── processed/                    # Analysis outputs (CSVs, checkpoints)
│   └── reference/                    # Reference files (theme dictionaries)
├── figures/                          # Generated visualizations
├── src/
│   ├── __init__.py
│   ├── paths.py                      # Shared path definitions
│   └── tools/
│       └── extract_dependencies.py   # Dependency extraction utility
├── requirements.txt                  # Python dependencies
└── README.md
```

## Environment Setup (.venv)

This project uses a Python virtual environment to manage dependencies. Follow the instructions for your operating system:

### Linux / macOS

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
# Create virtual environment
py -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Windows (cmd)

```bat
:: Create virtual environment
py -m venv .venv

:: Activate virtual environment
.venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt
```

### Create / Update requirements.txt

To freeze current dependencies (after installing new packages):

```bash
pip freeze > requirements.txt
```

## Dependencies

This project requires the following Python packages (third-party):

| Package | Description |
|---------|-------------|
| `google-api-python-client` | YouTube Data API access |
| `httpx` | HTTP client (used by OpenAI) |
| `openai` | OpenAI GPT API client |
| `openpyxl` | Excel file support for pandas |
| `pandas` | Data manipulation and analysis |
| `python-dotenv` | Load environment variables from `.env` |
| `requests` | HTTP requests |
| `tiktoken` | Token counting for OpenAI models |
| `tqdm` | Progress bars |
| `youtube-transcript-api` | Fetch YouTube video transcripts |

## Setup

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd ElectriAI_Research

# Set up virtual environment (see above), then:
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with your API keys:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Input Data

Place your input files in the appropriate directories:

| File | Location | Description |
|------|----------|-------------|
| Video URLs Excel | `data/raw/electrical_construction_videos_combined_Sep19.xlsx` | Excel file with YouTube video URLs |
| Transcripts JSON | `data/raw/transcripts.json` | Previously collected transcript data |
| Comments JSON | `data/raw/youtube_comments.json` | Raw YouTube comments data |
| Theme Dictionary | `data/reference/Theme_Dictionary.json` | Pre-defined theme categories (optional) |

## Run Order

Execute the notebooks in the following order:

1. **01_Data_Collection.ipynb** — Collect YouTube video URLs, fetch transcripts, and download comments
2. **02_Transcript_Analysis.ipynb** — Summarize transcripts and extract problem/solution/topic information
3. **03_Comment_Analysis.ipynb** — Analyze comments using transcript context, extract Q&A and topics
4. **04_Theme_Dictionary.ipynb** — Classify analyzed comments into predefined themes

## Outputs

After running all notebooks, you'll find the following outputs:

| Output | Location | Description |
|--------|----------|-------------|
| Video URLs CSV | `data/raw/electrical_construction_videos_max.csv` | Collected video URLs |
| New Transcripts | `data/raw/new_transcripts.json` | Newly fetched transcripts |
| YouTube Comments | `data/raw/youtube_comments.json` | Raw comment data |
| Transcript Summaries | `data/processed/GPT_5_Mini_Transcripts_Summary.csv` | Initial transcript analysis |
| Transcript Summaries V2 | `data/processed/GPT_5_Mini_Transcripts_SummaryV2.csv` | Refined summaries |
| Comment Analysis | `data/processed/GPT_5_Mini_Comment_Analysis.csv` | Analyzed comments with topics |
| Thematic Analysis | `data/processed/Thematic_Analysis_Output.csv` | Theme classifications |
| Theme Dictionary | `data/reference/Theme_Dictionary.json` | Theme definitions |

## Portability

This project uses **pathlib** for all file paths, making it fully portable across:
- Windows
- macOS
- Linux

All paths are defined relative to the project root in `src/paths.py`. The notebooks automatically detect the project root regardless of the current working directory.

## Notes

- Each notebook includes a **Paths / Configuration** cell at the top that sets up imports and file paths
- Checkpointing is built into each notebook for resumable processing
- API rate limiting is respected with appropriate delays between requests
- Progress is saved incrementally to prevent data loss on interruption (Ctrl+C is handled gracefully)

## License

[Add your license here]
