import csv
R = "C:/Users/mikha/Documents/dpc-research/connectome-seed/results/genome/c6/checks/"
S = {"A": R + "knockout_regrow/synthetic_worlds.csv", "L": R + "knockout_regrow_male_cns/synthetic_worlds_L.csv", "R": R + "knockout_regrow_male_cns/synthetic_worlds_R.csv"}
for b, p in S.items():
    rows = [r for r in csv.DictReader(open(p, encoding="utf-8")) if r["predictor"] == "rule #2.1"]
    nf = [(r["seed"], r["auc"][:6], r["p_P"]) for r in rows if r["family"] == "Nf"]
    seen = [(r["family"], r["seed"], float(r["auc"]), r["p_P"]) for r in rows if r["family"].startswith("M") and float(r["p_P"]) <= 0.01]
    uns = [(r["family"], r["seed"], float(r["auc"]), r["p_P"]) for r in rows if r["family"].startswith("M") and float(r["p_P"]) > 0.01]
    print(b, "Nf", nf)
    print(b, "min AUC seen", min(seen, key=lambda x: x[2]), "max AUC unseen", max(uns, key=lambda x: x[2]))
