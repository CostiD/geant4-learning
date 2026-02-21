"""
CR-39 Proton Irradiation — Publication-Quality Analysis
========================================================
GEANT4 11 MT — parser pentru formatul wcsv::ntuple
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec
from scipy.stats import gaussian_kde
from scipy.optimize import curve_fit
from pathlib import Path

# ── Style publicabil ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":         "serif",
    "font.serif":          ["Times New Roman", "DejaVu Serif"],
    "font.size":           11,
    "axes.labelsize":      12,
    "axes.titlesize":      12,
    "legend.fontsize":     10,
    "xtick.direction":     "in",  "ytick.direction":     "in",
    "xtick.top":           True,  "ytick.right":         True,
    "xtick.minor.visible": True,  "ytick.minor.visible": True,
    "axes.linewidth":      1.2,   "lines.linewidth":     1.8,
    "figure.dpi":          300,   "savefig.dpi":         300,
    "savefig.bbox":        "tight",
})
BLUE, RED, GREEN, GOLD = "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"

# ── Parser robust pentru GEANT4 wcsv::ntuple ─────────────────────────────────
def load_geant4_csv(path):
    with open(path) as f:
        lines = f.readlines()
    data_start = next(i for i, l in enumerate(lines) if not l.startswith('#'))
    columns = ['EventID','Edep_MeV','TrackLen_mm','LET_MeV_mm',
               'EntryX_mm','EntryY_mm','Hit']
    df = pd.read_csv(path, skiprows=data_start, header=None,
                     names=columns, on_bad_lines='skip')
    return df.apply(pd.to_numeric, errors='coerce').dropna()

# ── Încarcă date ──────────────────────────────────────────────────────────────
csv_path = Path("cr39_output.csv")
if csv_path.exists():
    df = load_geant4_csv(csv_path)
    print(f"[OK] Date GEANT4 încărcate: {len(df):,} evenimente")
else:
    print("[INFO] Fișier negăsit — date sintetice pentru demo")
    rng = np.random.default_rng(42)
    N = 50_000
    hit = rng.random(N) > 0.02
    edep = rng.normal(2.35, 0.08, N) * hit
    tlen = rng.normal(0.47, 0.02, N) * hit
    let  = np.where(tlen > 0, edep / tlen, 0.)
    df = pd.DataFrame(dict(EventID=np.arange(N), Edep_MeV=edep,
                           TrackLen_mm=tlen, LET_MeV_mm=let,
                           EntryX_mm=rng.normal(0,1.,N),
                           EntryY_mm=rng.normal(0,1.,N),
                           Hit=hit.astype(int)))

hits = df[df["Hit"] == 1].copy()
print(f"Hits în CR-39 : {len(hits):,}  ({100*len(hits)/len(df):.1f} %)")
print(f"Edep mediu    : {hits['Edep_MeV'].mean():.3f} +/- {hits['Edep_MeV'].std():.3f} MeV")
print(f"LET mediu     : {hits['LET_MeV_mm'].mean():.3f} MeV/mm")

# ── Layout figură ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 10))
gs  = GridSpec(2, 3, figure=fig, hspace=0.38, wspace=0.38)
ax1, ax2, ax3 = fig.add_subplot(gs[0,0]), fig.add_subplot(gs[0,1]), fig.add_subplot(gs[0,2])
ax4, ax5, ax6 = fig.add_subplot(gs[1,0]), fig.add_subplot(gs[1,1]), fig.add_subplot(gs[1,2])

# ── 1. Spectrul energiei depuse ───────────────────────────────────────────────
ax1.hist(hits["Edep_MeV"], bins=120, color=BLUE, alpha=0.85,
         edgecolor="white", lw=0.3, density=True)
ax1.axvline(hits["Edep_MeV"].mean(), color=RED, ls="--", lw=1.5,
            label=fr"$\langle E_{{dep}}\rangle={hits['Edep_MeV'].mean():.2f}$ MeV")
ax1.set_xlabel(r"$E_{\rm dep}$ (MeV)")
ax1.set_ylabel(r"Densitate probabilitate (MeV$^{-1}$)")
ax1.set_title("Spectrul energiei depuse")
ax1.legend(framealpha=0.9)

# ── 2. Distribuția LET ────────────────────────────────────────────────────────
let_v = hits["LET_MeV_mm"][hits["LET_MeV_mm"] > 0]
ax2.hist(let_v, bins=100, color=GREEN, alpha=0.85,
         edgecolor="white", lw=0.3, density=True)
ax2.axvline(let_v.mean(), color=RED, ls="--", lw=1.5,
            label=fr"$\langle LET\rangle={let_v.mean():.1f}$ MeV/mm")
ax2.set_xlabel(r"LET (MeV mm$^{-1}$)")
ax2.set_ylabel(r"Densitate probabilitate")
ax2.set_title("Linear Energy Transfer in CR-39")
ax2.legend(framealpha=0.9)

# ── 3. Lungimea urmei ─────────────────────────────────────────────────────────
tl = hits["TrackLen_mm"][hits["TrackLen_mm"] > 0]
ax3.hist(tl, bins=100, color=GOLD, alpha=0.85,
         edgecolor="white", lw=0.3, density=True)
ax3.axvline(tl.mean(), color=RED, ls="--", lw=1.5,
            label=fr"$\langle\ell\rangle={tl.mean():.4f}$ mm")
ax3.set_xlabel(r"Track length $\ell$ (mm)")
ax3.set_ylabel(r"Probability density (mm$^{-1}$)")
ax3.set_title("Proton Track Length in CR-39")
ax3.legend(framealpha=0.9)

# ── 4. Spot fascicul 2D ───────────────────────────────────────────────────────
lim = max(8., hits["EntryX_mm"].abs().quantile(0.995))
h, xe, ye = np.histogram2d(hits["EntryX_mm"], hits["EntryY_mm"],
                            bins=80, range=[[-lim,lim],[-lim,lim]])
h[h == 0] = np.nan
im = ax4.pcolormesh(xe, ye, h.T, norm=LogNorm(vmin=1, vmax=np.nanmax(h)), cmap="plasma")
fig.colorbar(im, ax=ax4, pad=0.02).set_label("Counts / bin")
ax4.set_xlabel("$x$ (mm)"); ax4.set_ylabel("$y$ (mm)")
ax4.set_title("Proton Beam Spot on CR-39")
ax4.set_aspect("equal"); ax4.set_xlim(-lim,lim); ax4.set_ylim(-lim,lim)

# ── 5. Profil radial fluență ──────────────────────────────────────────────────
r = np.sqrt(hits["EntryX_mm"]**2 + hits["EntryY_mm"]**2)
r_bins = np.linspace(0, lim, 60)
r_mid  = 0.5*(r_bins[:-1]+r_bins[1:])
counts_r, _ = np.histogram(r, bins=r_bins)
fluence = counts_r / (np.pi*(r_bins[1:]**2 - r_bins[:-1]**2))
ax5.plot(r_mid, fluence, color=BLUE, lw=2, label="GEANT4")
try:
    def gauss_r(r, A, s): return A*np.exp(-r**2/(2*s**2))
    popt, _ = curve_fit(gauss_r, r_mid, fluence, p0=[fluence.max(), 1.5])
    r_f = np.linspace(0, lim, 300)
    ax5.plot(r_f, gauss_r(r_f, *popt), "--", color=RED, lw=1.5,
             label=fr"Gaussian fit $\sigma={popt[1]:.2f}$ mm")
except Exception: pass
ax5.set_xlabel("Radial distance $r$ (mm)")
ax5.set_ylabel(r"Fluence (rel. protons mm$^{-2}$)")
ax5.set_title("Radial Fluence Profile")
ax5.legend(framealpha=0.9)

# ── 6. LET vs Edep ───────────────────────────────────────────────────────────
idx = np.random.choice(len(hits), size=min(8000,len(hits)), replace=False)
x6  = hits["Edep_MeV"].values[idx]
y6  = hits["LET_MeV_mm"].values[idx]
msk = (x6>0)&(y6>0); x6, y6 = x6[msk], y6[msk]
ax6.hexbin(x6, y6, gridsize=50, cmap="YlOrRd", mincnt=1, linewidths=0.1)
try:
    kde = gaussian_kde(np.vstack([x6,y6]))
    xg = np.linspace(x6.min(),x6.max(),80)
    yg = np.linspace(y6.min(),y6.max(),80)
    XX,YY = np.meshgrid(xg,yg)
    ZZ = kde(np.vstack([XX.ravel(),YY.ravel()])).reshape(XX.shape)
    lvls = np.percentile(ZZ[ZZ>0],[20,50,80,95])
    ax6.contour(XX, YY, ZZ, levels=lvls, colors="navy", linewidths=0.8, alpha=0.7)
except Exception: pass
ax6.set_xlabel(r"$E_{\rm dep}$ (MeV)")
ax6.set_ylabel(r"LET (MeV mm$^{-1}$)")
ax6.set_title(r"LET vs $E_{\rm dep}$ Correlation")

# ── Titlu global ──────────────────────────────────────────────────────────────
fig.suptitle(
    "GEANT4 Simulation — 2.5 MeV Proton Irradiation of CR-39 Nuclear Track Detector\n"
    r"Beam-to-detector distance: 3 cm | CR-39 ($\rho$=1.31 g cm$^{-3}$, 0.5 mm) | "
    f"$N_{{\\rm events}}$={len(df):,}",
    fontsize=12, y=1.01, weight="semibold"
)

for ext in ["pdf", "png"]:
    fig.savefig(f"cr39_proton_analysis.{ext}", format=ext)
print("\nFiguri salvate: cr39_proton_analysis.pdf + .png")
plt.show()
