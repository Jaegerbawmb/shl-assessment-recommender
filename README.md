
# SHL Assessment Recommender (Generative AI Internship Assignment)



This project implements an AI-powered assessment recommendation system for SHL, designed to recommend the most relevant assessments from SHL’s product catalog given a query, job description, or hiring requirement.

Built using FastAPI, FAISS, and Sentence Transformers, the system can be queried directly via API or explored through a simple Streamlit UI.

## 🚀 Features

Semantic Search: Uses all-MiniLM-L6-v2 embeddings to capture contextual meaning of queries.

FAISS Indexing: Enables fast and scalable similarity search across assessment metadata.

Fallback TF-IDF Engine: Provides backup retrieval when embeddings are unavailable.

Re-ranking & Balancing: Prioritizes diverse test types (Knowledge, Personality, Simulation, etc.).

REST API + Streamlit UI: For easy querying, testing, and demonstration.

🧩 Project Structure

shl-assessment-recommender/


1) app/

 main.py # FastAPI backend (API endpoint)
 schemas.py # Request/response models
 balancer.py # Balances assessment types


 2) scripts/

 crawl_catalog.py # Crawls SHL catalog pages

 build_index.py # Builds FAISS index and metadata

 query_recommender.py # CLI for testing the recommender

 fetch_details.py # Fetches detailed assessment info

 3) models/
 embed_index.py # Embedding & FAISS retrieval

 tfidf_fallback.py # TF-IDF retrieval backup

 utils/

 text.py # Text cleaning helpers

 jd_extract.py # Job description extraction

 taxonomy.py # Taxonomy/tag mapping

 4) ui/

 app.py # Streamlit front-end app

5)  data/

 catalog_full.json # Crawled catalog data

 index.faiss # FAISS vector index

 meta.parquet # Metadata for FAISS

 test_dataset.xlsx # Unlabeled test queries

 submission_results.csv

 README.md

 test_api.py # Automated API testing

## ⚙️ Setup Instructions

### Clone the Repository

git clone https://github.com/<your-username>/shl-assessment-recommender.git
cd shl-assessment-recommender


### Create and Activate a Virtual Environment

python -m venv venv
venv\Scripts\activate    # on Windows
source venv/bin/activate # on macOS/Linux


### Install Dependencies

pip install -r requirements.txt


### Run the FastAPI Server

uvicorn app.main:app --reload


The API will now be available at:

http://127.0.0.1:8000/recommend


### Run the Streamlit Web App

streamlit run ui/app.py


## 🧠 API Usage
Endpoint:
POST /recommend

Example Request:
{
  "query": "Looking to hire a Java developer for backend applications",
  "k": 5
}

Example Response:
{
  "recommended_assessments": [
    {
      "name": "Java Developer Test",
      "url": "https://www.shl.com/products/java-developer-test/",
      "description": "Multiple-choice test assessing Java knowledge...",
      "duration": 30,
      "remote_support": "Yes",
      "test_type": ["Knowledge & Skills", "Aptitude"]
    }
  ]
}


## 📄 Deliverables Summary

Web App URL: Interactive Streamlit interface for user queries.

Get API Endpoint: FastAPI /recommend endpoint returning JSON recommendations.

Report: Approach_and_Optimization.pdf (2-page write-up).

Test Results: submission_results.csv and submission_results_final.csv.

## ✨ Notes

The recommendation logic can be fine-tuned by enriching catalog metadata or improving embedding reranking.

Future improvements may include multilingual support, adaptive scoring, and LLM-based reranking for domain adaptability.


