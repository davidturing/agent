# SKILL: Self-Learning Agent

This agent implements a closed-loop data pipeline: Ingestion -> Internalization -> Iteration -> Publication.
It autonomously learns from external sources (GitHub, X, Web), updates its internal knowledge base (ChromaDB), and publishes synthesized insights to WordPress.

## Usage

```bash
# Run the full pipeline (Ingest -> Learn -> Publish)
python3 skills/self-learning-agent/src/pipeline.py
```

## Architecture

1.  **Ingestion (感知)**: `ingest.py`
    *   Fetches latest updates from GitHub (davidturing), X (via bird/API), and specified URLs.
    *   Outputs raw text/JSON to `data/raw/`.

2.  **Internalization (内化)**: `brain.py`
    *   Uses Gemini to decompose text into "Atomic Insights".
    *   Stores insights in local ChromaDB (`db/`).

3.  **Iteration (迭代)**: `brain.py`
    *   Queries ChromaDB for similar existing insights.
    *   **LLM Judge**: Decides if new info contradicts, updates, or adds to old info.
    *   Generates a "Learning Log" markdown.

4.  **Publication (发表)**: `publish.py`
    *   Posts the "Learning Log" to WordPress (dvspace5).

## Configuration

Ensure `.env` contains:
*   `GOOGLE_API_KEY`: For Gemini.
*   `WP_URL`, `WP_USERNAME`, `WP_PASSWORD`: For WordPress.
*   `GITHUB_TOKEN`: Optional, for higher rate limits.
