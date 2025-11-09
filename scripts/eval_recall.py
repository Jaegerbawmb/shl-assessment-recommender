import argparse
import pandas as pd
from collections import defaultdict

def recall_at_k(truth_urls, pred_urls, k=10):
    truth = set(u.strip('/') for u in truth_urls)
    preds = [u.strip('/') for u in pred_urls[:k]]
    hit = len(truth.intersection(preds))
    return hit / max(1, len(truth))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--train_xlsx', required=True)
    ap.add_argument('--pred_csv', required=True, help='submission csv to evaluate')
    args = ap.parse_args()

    train = pd.read_excel(args.train_xlsx, sheet_name='Train-Set')
    grouped = train.groupby('Query')['Assessment_url'].apply(list)

    preds = pd.read_csv(args.pred_csv)

    pred_map = defaultdict(list)
    for _, r in preds.iterrows():
        pred_map[r['Query']].append(r['Assessment_url'])

    scores = []
    for q, truth in grouped.items():
        r = recall_at_k(truth, pred_map.get(q, []), k=10)
        scores.append(r)
        print(f"Recall@10 | {r:.3f} | {q[:80]}")

    mean_r = sum(scores)/max(1, len(scores))
    print(f"Mean Recall@10: {mean_r:.4f}")

if __name__ == '__main__':
    main()
