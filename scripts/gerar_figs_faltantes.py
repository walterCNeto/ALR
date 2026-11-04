"""
Gera as 3 figuras faltantes do paper:
  fig_heatmap_pestab.png
  fig_pestab_historico.png
  fig_hiato_hp.png

Uso: rodar na pasta que contem cache_dados/
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.filters.hp_filter import hpfilter

CACHE = Path("cache_dados")
assert CACHE.exists(), "Nao achei cache_dados"
Path("figs").mkdir(exist_ok=True)


def load(code):
    df = pd.read_csv(CACHE / f"sgs_{code}.csv")
    dc = [c for c in df.columns if c.lower() in ("data", "date")][0]
    vc = [c for c in df.columns if c.lower() in ("valor", "value")][0]
    df[dc] = pd.to_datetime(df[dc], errors="coerce")
    s = pd.to_numeric(df[vc], errors="coerce")
    s.index = df[dc]
    s = s.dropna()
    s.index = s.index + pd.offsets.MonthEnd(0)
    return s


# Carrega series
ipca = load(433)
selic = load(432)
dbgg = load(13762)
primario = load(5793)
ibc = load(24364)


# Trimestrais
frac = ipca / 100
ipca12 = ((1 + frac).rolling(12).apply(np.prod, raw=True) - 1) * 100
pi_q = ipca12.resample("QE").last()
i_q = selic.resample("QE").mean()
dbgg_q = dbgg.resample("QE").last()
prim_q = primario.resample("QE").last()


def p_estab(b, i, pi, g):
    return ((1 + i / 100) / ((1 + pi / 100) * (1 + g / 100)) - 1) * b


# --------------------------------------------------------------
# FIG 1: HEATMAP p*
# --------------------------------------------------------------
b_grid = np.arange(60, 95, 5)
i_grid = np.arange(8, 18, 1)
pi_curr = 4.39
g_curr = 0.87

M = np.zeros((len(b_grid), len(i_grid)))
for ib, b in enumerate(b_grid):
    for ii, i in enumerate(i_grid):
        M[ib, ii] = p_estab(b, i, pi_curr, g_curr)

fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(M, cmap="RdYlGn_r", aspect="auto", origin="lower")
ax.set_xticks(range(len(i_grid)))
ax.set_xticklabels(i_grid)
ax.set_yticks(range(len(b_grid)))
ax.set_yticklabels(b_grid)
for ib in range(len(b_grid)):
    for ii in range(len(i_grid)):
        ax.text(ii, ib, f"{M[ib, ii]:.1f}", ha="center", va="center", fontsize=9)
plt.colorbar(im, ax=ax, label="p* (% do PIB)")
ax.set_xlabel("Selic nominal (% a.a.)")
ax.set_ylabel("Divida/PIB inicial (%)")
ax.set_title(f"Superavit primario estabilizador (pi = {pi_curr}%, g real = {g_curr}%)")
plt.tight_layout()
plt.savefig("figs/fig_heatmap_pestab.png", dpi=120, bbox_inches="tight")
plt.close()
print("OK fig_heatmap_pestab.png")


# --------------------------------------------------------------
# FIG 2: p* HISTORICO vs observado
# --------------------------------------------------------------
g_yoy = ibc.pct_change(12).resample("QE").last() * 100

df_hist = pd.DataFrame({
    "b": dbgg_q,
    "i": i_q,
    "pi": pi_q,
    "g": g_yoy,
    "p": prim_q,
}).dropna()

df_hist["p_star"] = df_hist.apply(
    lambda r: p_estab(r["b"], r["i"], r["pi"], r["g"]), axis=1
)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_hist.index, df_hist["p_star"], color="crimson", lw=2, label="p* requerido")
ax.plot(df_hist.index, df_hist["p"], color="steelblue", lw=2, label="p observado (12m)")
ax.fill_between(
    df_hist.index, df_hist["p_star"], df_hist["p"],
    where=df_hist["p_star"] > df_hist["p"], color="pink", alpha=0.3,
    label="Gap (divida cresce)"
)
ax.fill_between(
    df_hist.index, df_hist["p_star"], df_hist["p"],
    where=df_hist["p_star"] <= df_hist["p"], color="lightgreen", alpha=0.3,
    label="Gap (divida cai)"
)
ax.set_ylabel("% do PIB")
ax.legend()
ax.grid(alpha=0.3)
ax.set_title("Superavit primario requerido vs observado")
plt.tight_layout()
plt.savefig("figs/fig_pestab_historico.png", dpi=120, bbox_inches="tight")
plt.close()
print("OK fig_pestab_historico.png")


# --------------------------------------------------------------
# FIG 3: HIATO HP
# --------------------------------------------------------------
ibc_q = ibc.resample("QE").last().dropna()
log_ibc = np.log(ibc_q)
cycle, trend = hpfilter(log_ibc, lamb=1600)
hiato = cycle * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
ax1.plot(ibc_q.index, ibc_q, color="steelblue", lw=1.5, label="IBC-Br observado")
ax1.plot(ibc_q.index, np.exp(trend), color="crimson", lw=2, label="Tendencia HP (lambda=1600)")
ax1.set_ylabel("Indice")
ax1.set_title("IBC-Br e tendencia potencial")
ax1.legend()
ax1.grid(alpha=0.3)

ax2.fill_between(ibc_q.index, 0, hiato, where=hiato >= 0, color="green", alpha=0.3)
ax2.fill_between(ibc_q.index, 0, hiato, where=hiato < 0, color="red", alpha=0.3)
ax2.plot(ibc_q.index, hiato, color="k", lw=1.5)
ax2.axhline(0, color="k", ls="--", alpha=0.5)
ax2.set_ylabel("% do potencial")
ax2.set_title("Hiato do produto")
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("figs/fig_hiato_hp.png", dpi=120, bbox_inches="tight")
plt.close()
print("OK fig_hiato_hp.png")

print()
print("As 3 figuras foram geradas em figs/")