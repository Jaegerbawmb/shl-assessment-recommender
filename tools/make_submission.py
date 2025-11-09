import argparse, pandas as pd, requests

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--api', default='http://localhost:8000')
    ap.add_argument('--test_xlsx', default='data/Gen_AI Dataset.xlsx')
    ap.add_argument('--out_csv', default='submission.csv')
    ap.add_argument('--k', type=int, default=10)
    args = ap.parse_args()

    test_df = pd.read_excel(args.test_xlsx, sheet_name='Test-Set')

    rows = []
    for q in test_df['Query'].tolist():
        r = requests.post(f"{args.api}/recommend", json={"query": q, "k": args.k}).json()
        for rec in r['recommendations']:
            rows.append({"Query": q, "Assessment_url": rec['url']})
    pd.DataFrame(rows, columns=["Query","Assessment_url"]).to_csv(args.out_csv, index=False)
    print("Wrote:", args.out_csv)

if __name__ == '__main__':
    main()
