import pandas as pd
import requests
import time

# --- CONFIG ---
API_URL = "http://127.0.0.1:8000/recommend"
TEST_FILE = "data\Gen_AI Dataset.xlsx"
OUTPUT_CSV = "submission_results.csv"
TOP_K = 5  

# --- LOAD TEST SET ---
df = pd.read_excel(TEST_FILE, sheet_name="Test-Set")  
df = df.drop_duplicates(subset=["Query"]).dropna(subset=["Query"]).reset_index(drop=True)
df = df.rename(columns=lambda x: x.strip().lower())

if 'query' not in df.columns:
    for c in df.columns:
        if 'query' in c.lower():
            df.rename(columns={c: 'query'}, inplace=True)
            break

queries = df["query"].dropna().tolist()

results = []

print(f"🧪 Running {len(queries)} test queries against the API...\n")

# --- LOOP OVER EACH QUERY ---
for i, query in enumerate(queries, 1):
    payload = {"query": query, "k": TOP_K}
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            recs = data.get("recommended_assessments", [])
            for rec in recs:
                results.append({
                    "query": query,
                    "assessment_url": rec.get("url", "")
                })
            print(f"✅ [{i}/{len(queries)}] {query[:60]}... → {len(recs)} results")
        else:
            print(f"⚠️ [{i}/{len(queries)}] Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ [{i}/{len(queries)}] Error: {e}")
    time.sleep(1) 

# --- SAVE RESULTS ---
if results:
    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n📁 Saved results → {OUTPUT_CSV}")
else:
    print("\n❌ No results were collected. Check API or data.")
