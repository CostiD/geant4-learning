"""
CR-39 Proton Irradiation — Publication-Quality Analysis
========================================================
Reads cr39_output.csv produced by the GEANT4 simulation and generates
a multi-panel figure suitable for submission to journals such as
Nuclear Instruments & Methods B, Radiation Measurements, or NIMB.

Requirements: numpy, pandas, matplotlib, scipy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec
from scipy.stats import gaussian_kde
from pathlib import Path

# ── Matplotlib style ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":         "serif",
    "font.serif":          ["Times New Roman", "DejaVu Serif"],
    "font.size":           11,
    "axes.labelsize":      12,
    "axes.titlesize":      12,
    "legend.fontsize":     10,
    "xtick.direction":     "in",
    "ytick.direction":     "in",
    "xtick.top":           True,
    "ytick.right":         True,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "axes.linewidth":      1.2,
    "lines.linewidth":     1.8,
    "figure.dpi":          300,
    "savefig.dpi":         300,
    "savefig.bbox":        "tight",
})

BLUE  = "#1f77b4"
RED   = "#d62728"
GREEN = "#2ca02c"
GOLD  = "#ff7f0e"

# ── Load data — robust parsing ────────────────────────────────────────────────
csv_path = Path("cr39_output.csv")

if not csv_path.exists():
    print("[INFO] cr39_output.csv not found — generez date sintetice pentru demo.")
    rng = np.random.default_rng(42)
    N = 50_000
    hit_mask = rng.random(N) > 0.02
    edep  = rng.normal(2.35, 0.08, N) * hit_mask
    tlen  = rng.normal(0.47, 0.02, N) * hit_mask
    let   = np.where(tlen > 0, edep / tlen, 0.)
    ex    = rng.normal(0, 1.0, N)
    ey    = rng.normal(0, 1.0, N)
    df = pd.DataFrame(dict(EventID=np.arange(N), Edep_MeV=edep,
                           TrackLen_mm=tlen, LET_MeV_mm=let,
                           EntryX_mm=ex, EntryY_mm=ey,
                           Hit=hit_mask.astype(int)))
else:
    # on_bad_lines='skip' ignoră liniile corupte din MT GEANT4
    df = pd.read_csv(csv_path, on_bad_lines='skip')
    # Păstrează doar coloanele cunoscute, elimină rânduri cu NaN
    expected = ['EventID','Edep_MeV','TrackLen_mm','LET_MeV_mm',
                'EntryX_mm','EntryY_mm','Hit']
    df = df[[c for c in expected if c in df.columns]].dropna()
    df = df[pd.to_numeric(df['Edep_MeV'], errors='coerce').notna()]
    for col in ['Edep_MeV','TrackLen_mm','LET_MeV_mm','EntryX_mm','EntryY_mm']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['Hit'] = pd.to_numeric(df['Hit'], errors='coerce').fillna(0).astype(int)
    df = df.dropna()

print(f"Total events : {len(df):,}")
hits = df[df["Hit"] == 1].copy()
print(f"Hits în CR-39: {len(hits):,}  ({100*len(hits)/len(df):.1f} %)")
print(f"Edep mediu   : {hits['Edep_MeV'].mean():.3f} ± {hits['Edep_MeV'].std():.3f} MeV")
print(f"LET mediu    : {hits['LET_MeV_mm'].mean():.3f} MeV/mm")

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 10))
gs  = GridSpec(2, 3, figure=fig, hspace=0.38, wspace=0.38)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])
ax4 = fig.add_subplot(gs[1, 0])
ax5 = fig.add_subplot(gs[1, 1])
ax6 = fig.add_subplot(gs[1, 2])

# ── Panel 1: Spectrul de energie depusă ───────────────────────────────────────
ax1.hist(hits["Edep_MeV"], bins=120, color=BLUE, alpha=0.85,
         edgecolor="white", linewidth=0.3, density=True)
ax1.axvline(hits["Edep_MeV"].mean(), color=RED, ls="--", lw=1.5,
            label=fr"$\langle E_{{dep}}\rangle = {hits['Edep_MeV'].mean():.2f}$ MeV")
ax1.set_xlabel(r"$E_{\rm dep}$ (MeV)")
ax1.set_ylabel("Densitate de probabilitate (MeV$^{-1}$)")
ax1.set_title("Spectrul energiei depuse")
ax1.legend(framealpha=0.9)

# ── Panel 2: Distribuția LET ──────────────────────────────────────────────────
let_vals = hits["LET_MeV_mm"][hits["LET_MeV_mm"] > 0]
ax2.hist(let_vals, bins=100, color=GREEN, alpha=0.85,
         edgecolor="white", linewidth=0.3, density=True)
ax2.axvline(let_vals.mean(), color=RED, ls="--", lw=1.5,
            label=fr"$\langle\mathrm{{LET}}\rangle = {let_vals.mean():.2f}$ MeV/mm")
ax2.set_xlabel(r"LET (MeV mm$^{-1}$)")
ax2.set_ylabel("Densitate de probabilitate")
ax2.set_title("Linear Energy Transfer în CR-39")
ax2.legend(framealpha=0.9)

# ── Panel 3: Lungimea urmei ────────────────────────────────────────────────────
tl = hits["TrackLen_mm"][hits["TrackLen_mm"] > 0]
ax3.hist(tl, bins=100, color=GOLD, alpha=0.85,
         edgecolor="white", linewidth=0.3, density=True)
ax3.axvline(tl.mean(), color=RED, ls="--", lw=1.5,
            label=fr"$\langle\ell\rangle = {tl.mean():.3f}$ mm")
ax3.set_xlabel(r"Lungimea urmei $\ell$ (mm)")
ax3.set_ylabel("Densitate de probabilitate (mm$^{-1}$)")
ax3.set_title("Lungimea urmei protonului în CR-39")
ax3.legend(framealpha=0.9)

# ── Panel 4: Spot fascicul 2D ─────────────────────────────────────────────────
lim = 8.
h, xedge, yedge = np.histogram2d(hits["EntryX_mm"], hits["EntryY_mm"],
                                   bins=80, range=[[-lim, lim], [-lim, lim]])
h[h == 0] = np.nan
im = ax4.pcolormesh(xedge, yedge, h.T,
                    norm=LogNorm(vmin=1, vmax=np.nanmax(h)),
                    cmap="plasma")
cb = fig.colorbar(im, ax=ax4, pad=0.02)
cb.set_label("Numărătoare / bin")
ax4.set_xlabel("$x$ (mm)")
ax4.set_ylabel("$y$ (mm)")
ax4.set_title("Spot fascicul pe CR-39")
ax4.set_aspect("equal")
ax4.set_xlim(-lim, lim)
ax4.set_ylim(-lim, lim)

# ── Panel 5: Profilul radial de fluență ───────────────────────────────────────
r = np.sqrt(hits["EntryX_mm"]**2 + hits["EntryY_mm"]**2)
r_bins = np.linspace(0, lim, 60)
r_mid  = 0.5*(r_bins[:-1] + r_bins[1:])
counts_r, _ = np.histogram(r, bins=r_bins)
area_annulus = np.pi * (r_bins[1:]**2 - r_bins[:-1]**2)
fluence = counts_r / area_annulus

ax5.plot(r_mid, fluence, color=BLUE, lw=2, label="GEANT4")
from scipy.optimize import curve_fit
def gauss_radial(r, A, sig):
    return A * np.exp(-r**2 / (2*sig**2))
try:
    popt, _ = curve_fit(gauss_radial, r_mid, fluence, p0=[fluence.max(), 1.2])
    r_fine = np.linspace(0, lim, 300)
    ax5.plot(r_fine, gauss_radial(r_fine, *popt), "--", color=RED, lw=1.5,
             label=fr"Fit Gaussian $\sigma={popt[1]:.2f}$ mm")
except Exception:
    pass
ax5.set_xlabel("Distanța radială $r$ (mm)")
ax5.set_ylabel("Fluență (protoni rel. mm$^{-2}$)")
ax5.set_title("Profilul radial al fluenței")
ax5.legend(framealpha=0.9)

# ── Panel 6: LET vs Edep ──────────────────────────────────────────────────────
idx = np.random.choice(len(hits), size=min(8000, len(hits)), replace=False)
x6  = hits["Edep_MeV"].values[idx]
y6  = hits["LET_MeV_mm"].values[idx]
mask = (x6 > 0) & (y6 > 0)
x6, y6 = x6[mask], y6[mask]

ax6.hexbin(x6, y6, gridsize=50, cmap="YlOrRd", mincnt=1, linewidths=0.1)
try:
    kde = gaussian_kde(np.vstack([x6, y6]))
    xg  = np.linspace(x6.min(), x6.max(), 80)
    yg  = np.linspace(y6.min(), y6.max(), 80)
    XX, YY = np.meshgrid(xg, yg)
    ZZ = kde(np.vstack([XX.ravel(), YY.ravel()])).reshape(XX.shape)
    levels = np.percentile(ZZ[ZZ > 0], [20, 50, 80, 95])
    ax6.contour(XX, YY, ZZ, levels=levels, colors="navy",
                linewidths=0.8, alpha=0.7)
except Exception:
    pass
ax6.set_xlabel(r"$E_{\rm dep}$ (MeV)")
ax6.set_ylabel(r"LET (MeV mm$^{-1}$)")
ax6.set_title(r"Corelație LET vs $E_{\rm dep}$")

# ── Titlu global ──────────────────────────────────────────────────────────────
fig.suptitle(
    "Simulare GEANT4 — Iradiere CR-39 cu protoni de 2.5 MeV\n"
    r"Distanță fascicul–detector: 3 cm | CR-39 ($\rho$ = 1.31 g cm$^{-3}$, 0.5 mm) | "
    r"$N_{\rm events}$ = " + f"{len(df):,}",
    fontsize=12, y=1.01, weight="semibold"
)

out = Path("cr39_proton_analysis.pdf")
fig.savefig(out, format="pdf")
fig.savefig(out.with_suffix(".png"), format="png")
print(f"\nFiguri salvate: {out}  +  {out.with_suffix('.png')}")
plt.show()
