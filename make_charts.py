import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = "results/a3_results.csv"
E_FOR_CHART_A = 1
N_FOR_CHART_B = 5
SKEW_ORDER = ["none", "label", "quantity", "feature", "concept", "realistic"]

rows = []
with open(CSV_PATH) as f:
    for r in csv.DictReader(f):
        rows.append({
            "n": int(r["n_clients"]), "skew": r["skew"], "E": int(r["E"]),
            "fedavg": float(r["fedavg_acc"]) * 100,
            "worst": float(r["worst_hospital_acc"]) * 100,
            "local": float(r["worst_local_only_acc"]) * 100,
        })

skews = [s for s in SKEW_ORDER if any(r["skew"] == s for r in rows)]
Es = sorted({r["E"] for r in rows})
ns = sorted({r["n"] for r in rows})

# Chart (a): FedAvg accuracy vs number of hospitals, one line per skew
fig, ax = plt.subplots(figsize=(7, 4.5))
for s in skews:
    pts = sorted((r["n"], r["fedavg"]) for r in rows if r["skew"] == s and r["E"] == E_FOR_CHART_A)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=s)
ax.set_xticks(ns)
ax.set_xlabel("Number of hospitals in the consortium")
ax.set_ylabel("FedAvg test accuracy (%)")
ax.set_title(f"(a) FedAvg accuracy by consortium size (E = {E_FOR_CHART_A}, 20 rounds)")
ax.legend(title="Skew", fontsize=8, ncol=2)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("results/chart_a_fedavg_vs_n.png", dpi=200)

# Chart (b): worst-hospital accuracy vs skew, one bar per E
fig, ax = plt.subplots(figsize=(8, 4.5))
width = 0.8 / len(Es)
for i, E in enumerate(Es):
    vals = [next(r["worst"] for r in rows if r["skew"] == s and r["E"] == E and r["n"] == N_FOR_CHART_B) for s in skews]
    xs = [j + (i - (len(Es) - 1) / 2) * width for j in range(len(skews))]
    ax.bar(xs, vals, width, label=f"E = {E}")
local = [next(r["local"] for r in rows if r["skew"] == s and r["n"] == N_FOR_CHART_B) for s in skews]
ax.scatter(range(len(skews)), local, marker="_", s=900, color="black", linewidths=2, zorder=3, label="Worst hospital, local-only")
ax.set_xticks(range(len(skews)))
ax.set_xticklabels(skews)
ax.set_xlabel("Data skew across hospitals")
ax.set_ylabel("Worst-hospital accuracy (%)")
lo = min(min(local), min(r["worst"] for r in rows if r["n"] == N_FOR_CHART_B))
ax.set_ylim(lo - 3, 85)
ax.set_title(f"(b) Worst-hospital accuracy by skew ({N_FOR_CHART_B} hospitals)")
ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=4)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("results/chart_b_worst_vs_skew.png", dpi=200)

print("wrote results/chart_a_fedavg_vs_n.png and results/chart_b_worst_vs_skew.png")