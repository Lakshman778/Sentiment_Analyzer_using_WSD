***

# Universal WSD Sentiment Analyzer for both content and product reviews

A full‑stack sentiment analysis application that combines a custom **Word Sense Disambiguation (WSD)** engine with a **lexicon‑based sentiment scorer** to handle modern slang like “sick”, “fire”, “cool”, etc. The backend is a Flask REST API and the frontend is a separate client app. It supports both **raw text input** and **URL input** (it fetches a web page and analyzes the extracted article text).

## Features

- Flask REST API for sentiment analysis  
- WSD engine with context clues (e.g. “sick” → health vs. positive slang)  
- Lexicon‑based sentiment scorer with:
  - Intensifiers (very, really, extremely, etc.)  
  - Negation handling (not, never, don’t, didn’t, …)  
- Multiple analysis modes:
  - General text  
  - Product reviews  
  - Social media text  
  - **URL/article analysis (URL as input)**  
- Emoji sentiment lookup  
- Batch sentiment analysis endpoint  
- CORS enabled for frontend integration

## Project Structure

```text
Sentiment_Analyzer/
├── Backend/
│   ├── app.py                 # Flask app (main entrypoint)
│   ├── requirements.txt
│   ├── Procfile               # For deployment (gunicorn app:app)
│   ├── core/
│   │   ├── analyzer.py        # UniversalWSDAnalyzer
│   │   ├── wsd_engine.py      # WSDEngine (context-aware WSD)
│   │   └── sentiment_scorer.py# SentimentScorer
│   ├── modules/
│   │   ├── lexicon_manager.py # Lexicon + emoji sentiment
│   │   ├── validator.py       # Input validation
│   │   └── url_extractor.py   # Fetch & extract text from URLs
│   └── ...                    # Other backend helpers
├── Frontend/                  # UI client (optional)
├── tests/                     # Automated tests
├── Dockerfile                 # Docker setup (optional)
├── docker-compose.yml
└── venv/ or .venv/            # Local virtualenv (not committed)
```

## Backend: Running Locally

1. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   cd Sentiment_Analyzer/Backend
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   # or
   source .venv/bin/activate # macOS/Linux
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK tokenizers (first run only)**:

   ```python
   >>> import nltk
   >>> nltk.download('punkt')
   ```

4. **Run the Flask API**:

   ```bash
   python app.py
   ```

   The server will start at:

   ```text
   http://localhost:5000
   ```

## API Endpoints

All endpoints return JSON.

### 1. Root

`GET /`

Returns basic API info and the list of available endpoints.

### 2. General Sentiment (Text Input)

`POST /api/analyze`

**Request body:**

```json
{
  "text": "The movie is sick"
}
```

**Key response fields:**

- `score`: numeric sentiment score (negative to positive)  
- `sentiment`: `"NEGATIVE"`, `"NEUTRAL"` or `"POSITIVE"`  
- `confidence`: combined score + WSD confidence  
- `intensity`: `"low"`, `"medium"`, `"high"` or `"extreme"`  
- `wsd_analysis`: per‑token word sense information  
- `word_breakdown`: lexicon scores for individual words  

### 3. Product Reviews

`POST /api/analyze-product`

**Request body:**

```json
{
  "text": "The build quality is amazing but the battery life is bad."
}
```

Adds product‑specific information:

- `mode`: `"product"`  
- `aspects`: detected aspects like quality, price, shipping, service, etc.  
- `recommend`: boolean recommendation flag based on the overall score  

### 4. Social Media

`POST /api/analyze-social`

**Request body:**

```json
{
  "text": "This track is fire 🔥🔥 #music"
}
```

Adds social‑specific information:

- `mode`: `"social"`  
- `hashtags`: list of hashtags found in the text  
- `engagement_score`: simple engagement metric using punctuation, hashtags and sentiment  
- `emoji_analysis`: sentiment for emojis found in the text  

### 5. Batch Analysis (List of Texts)

`POST /api/analyze-batch`

**Request body:**

```json
{
  "texts": [
    "The movie is sick",
    "I am feeling sick"
  ]
}
```

Returns:

- `results`: list of per‑text analysis objects (same fields as `/api/analyze`)  
- `summary`: counts of `positive`, `negative`, and `neutral`, plus `average_confidence`  

### 6. URL Analysis (URL as Input)

`POST /api/analyze-url`

This endpoint accepts a web page URL instead of a text string.

**Request body:**

```json
{
  "url": "https://example.com/article"
}
```

The backend workflow:

1. Fetches the page HTML.  
2. Uses `URLTextExtractor` to extract the main article text.  
3. Runs the same WSD‑aware sentiment pipeline used for raw text.  

**Key response fields:**

- `source_url`: the URL that was analyzed  
- `snippet`: first part of the extracted text (preview)  
- All the usual sentiment fields (`score`, `sentiment`, `confidence`, `intensity`, etc.)  

If the extractor cannot retrieve enough text, the endpoint returns an error explaining that the page did not contain enough readable content.

### 7. Health & Version

- `GET /api/health` – health check, status, and timestamp  
- `GET /api/version` – version, name, and features list of the API  

## Core Logic

### Word Sense Disambiguation (WSDEngine)

- Uses a sliding context window around each token.  
- For ambiguous words like `sick`, `bad`, `fire`, and `cool`, matches context tokens against predefined clue lists to choose the correct sense, for example:
  - `sick` → `"health"` in “I am feeling sick”  
  - `sick` → `"positive"` in “The movie is sick bro”  

Each sense choice includes a simple confidence score based on context matches.

### Sentiment Scoring (SentimentScorer)

- For each token:
  - If a WSD override exists (e.g. `sick` → `positive`), that override score is used.  
  - Otherwise, the score comes from the sentiment lexicon.  
- Handles:
  - Negation within a small window before a sentiment word (e.g. “not good”).  
  - Intensifiers directly before a sentiment word (“really good”, “extremely bad”).  
- Produces a normalized average sentiment score over all sentiment‑bearing words in the text.

## Deployment

The backend is prepared to run with Gunicorn on common hosting platforms.

`Backend/Procfile`:

```text
web: gunicorn app:app
```

Typical deployment steps:

1. Push this project to GitHub.  
2. Create a new web service on your hosting provider.  
3. Set the root/working directory to `Backend/`.  
4. Set build command:

   ```text
   pip install -r requirements.txt
   ```

5. Set start command:

   ```text
   gunicorn app:app
   ```

After deployment you can call the same endpoints on the public URL instead of `localhost`.

## Running Tests

From the project root or the `tests/` folder:

```bash
pytest
```

(Adjust if you use a different test runner or command.)

## Future Improvements

- More advanced WSD based on WordNet or contextual embeddings.  
- Additional slang and domain‑specific context clues.  
- User accounts and history for saving analyses.  
- Deploying the frontend to a static hosting service and wiring it to the deployed backend API.

***
