# Crawlbase Markdown Output Demo

This project shows how to request LLM-ready Markdown from the Crawlbase Crawling API. It is intentionally small so new developers can understand each step before adapting it for larger AI, agent, or RAG pipeline workflows.

The demo uses two important Crawlbase parameters:

- `format=md` asks Crawlbase to return Markdown instead of raw HTML.
- `md_readability=true` asks Crawlbase to extract the main readable page content before converting it to Markdown.

## Why Markdown For AI?

HTML is useful for browsers, but it often contains navigation, scripts, styling, tracking tags, and layout markup that are noisy for language models. Markdown is easier to chunk, embed, summarize, and pass into retrieval systems because it preserves headings, links, lists, and tables in a cleaner text format.

## Project Files

- `crawlbase_markdown_demo.py` - command-line script that calls Crawlbase and saves Markdown.
- `requirements.txt` - Python dependency list.
- `.gitignore` - ignores local secrets, virtual environments, caches, and generated output.

## Prerequisites

- Python 3.10 or newer
- A Crawlbase Crawling API token
- Basic terminal familiarity

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Set Your Crawlbase Token

Do not hardcode your API token in the Python file. Set it as an environment variable instead.

PowerShell:

```powershell
$env:CRAWLBASE_TOKEN = "YOUR_CRAWLBASE_TOKEN"
```

macOS or Linux:

```bash
export CRAWLBASE_TOKEN="YOUR_CRAWLBASE_TOKEN"
```

## Run The Demo

Fetch Markdown from the default demo URL:

```powershell
python crawlbase_markdown_demo.py
```

Fetch Markdown from a specific URL:

```powershell
python crawlbase_markdown_demo.py --url "https://example.com/" --output "output/example.md"
```

The script prints a short summary:

```text
Markdown scrape complete
Resolved URL: https://example.com/
Original status: 200
Crawlbase status: 200
Content-Type: text/markdown; charset=utf-8
Markdown flavor: GitHub Flavored Markdown (GFM)
Saved to: output/example.md
```

Open the saved `.md` file to inspect the Markdown body.

## How The Request Works

The script sends a `GET` request to:

```text
https://api.crawlbase.com/
```

With these query parameters:

```text
token=<your token>
url=<target page>
format=md
md_readability=true
```

Crawlbase returns the page body as Markdown. Response headers may include useful crawl metadata such as:

- `url` - final URL Crawlbase resolved.
- `original_status` - status returned by the target website.
- `pc_status` - Crawlbase processing status.
- `Content-Type` - expected to be `text/markdown; charset=utf-8`.
- `X-Markdown-Flavor` - Markdown format information.

## Where This Fits In AI Pipelines

After saving Markdown, a production pipeline can:

1. Split the Markdown by headings or token count.
2. Store chunks in a vector database.
3. Retrieve relevant chunks for a RAG prompt.
4. Feed clean web context into an LLM or AI agent.

This demo focuses only on the crawling step so the API behavior is easy to see.

## Troubleshooting

If you see `Missing CRAWLBASE_TOKEN`, set the environment variable in the same terminal session where you run the script.

If you see a non-200 `pc_status`, inspect the printed `original_status` and try another URL. Some websites may need Crawlbase's JavaScript token if their main content is rendered client-side.

If a request takes longer than expected, keep the default 90-second timeout. Crawlbase recommends allowing enough time for complex pages.

## Learn More

- [Crawlbase Crawling API documentation](https://crawlbase.com/docs/crawling-api/)
- [Crawlbase Markdown response documentation](https://crawlbase.com/docs/crawling-api/response/#markdown-response)
