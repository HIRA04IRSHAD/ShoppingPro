# ShopAI - Smart Shopping Assistant

**Live demo:** https://hira04irshad.github.io/ShoppingPro/ (runs fully in your browser with Pyodide; the first load takes a few seconds)

ShopAI is a Flask-based smart shopping platform that helps users search for products, get personalized recommendations, and find the best deals using an intelligent scoring system.

## Features

- **Natural Language Search** - Search products using plain queries like "best gaming laptop under 80000" or "phone above 20k"
- **Smart Category Detection** - Automatically maps synonyms (e.g., "mobile", "smartphone", "redmi") to the correct product category
- **Budget Extraction** - Understands budget formats like "20k", "under 15000", or "above 30000" directly from the query
- **Deal Score Engine** - Ranks products using a formula based on discount percentage, rating, and customer sentiment
- **Feature & Brand Matching** - Matches queries against product brands, tags, and features (camera, battery, 5G, etc.)
- **Conversational Responses** - Handles identity questions, category browsing, and customer support queries in addition to product search

## Tech Stack

- **Backend**: Python, Flask
- **Data Storage**: JSON-based product database
- **Frontend**: HTML, CSS, JavaScript

## Project Structure

```
ShoppingPro/
├── app.py              # Flask app and API routes
├── assistant.py        # Query handling shared by Flask and the browser demo
├── recommender.py      # Search, category detection, and recommendation logic
├── deal_score.py        # Deal score calculation engine
├── db_manager.py        # Data access layer for products.json
├── products.json        # Product database
├── index.html           # GitHub Pages demo (same Python logic via Pyodide)
├── templates/
│   └── index.html       # Main frontend page
└── static/
    ├── css/
    └── js/
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository
   ```
   git clone https://github.com/HIRA04IRSHAD/ShoppingPro.git
   cd ShoppingPro
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the application
   ```
   python app.py
   ```

4. Open your browser and go to
   ```
   http://localhost:5000
   ```

## How It Works

1. User submits a search query through the frontend
2. The app checks for special intents (identity, support, categories) before running a product search
3. `recommender.py` extracts category, budget, brand, and feature signals from the query
4. Matching products are scored and ranked using both a match score and a deal score
5. Results are returned as JSON and rendered on the frontend

## Live demo on GitHub Pages

GitHub Pages can only serve static files, so the root `index.html` loads [Pyodide](https://pyodide.org) (Python compiled to WebAssembly) and runs the same `assistant.py`, `recommender.py`, `deal_score.py` and `db_manager.py` in the browser. The Flask app and the demo share one copy of the logic.

## API

### `POST /search`

Request body:
```json
{
  "query": "best gaming laptop under 80000"
}
```

Response:
```json
{
  "status": "success",
  "reply": "I found 5 matches for you. Sorting them by the best deals!",
  "products": [ ... ],
  "type": "search"
}
```

## Contributors

- HIRA04IRSHAD
- Ishika-codeit

## License

This project is for academic purposes.
