# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 5
Final Kiyaslama Raporu
=============================================================

Bu script tum asama sonuclarini birlestirerek
executive-level bir karsilastirma raporu uretir.

Karsilastirilan sistemler:
  [A] Deterministik CVRP (Phase 2a)   -- mevcut sistem benzeri
  [B] Stochastic Loading LP (Phase 3a) -- dagilimleri bilseydik
  [C] MSE Predict-then-Optimize        -- standart ML
  [D] SPO+ Decision-Focused Learning   -- onerilen sistem

Metrikler:
  - Ortalama gunluk toplam maliyet (TL)
  - Stockout orani (%)
  - Kac ATM'de stockout var
  - Yillik toplam ceza maliyeti (TL milyon)
  - Deterministike gore iyilesme (%)
  - VSS (Value of Stochastic Solution)
  - VOL (Value of Learning)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import os, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = os.path.dirname(__file__)

# ─────────────────────────────────────────────
# 1. ONCEKI ASAMALARDAN SONUCLARI YUKlE
# ─────────────────────────────────────────────

# Phase 2a: Deterministik CVRP (sabit - onceden hesaplandi)
DET = {
    "name":        "Deterministik\nCVRP",
    "short":       "Det.",
    "color":       "#ff6b6b",
    "mean_cost":   480_691,
    "stockout_pct": 42.4,
    "annual_penalty": 480_691 * 365 / 1e6,
    "daily_penalty": 477_297,
    "description": "Ortalama talep ile\nsabit rotalama"
}

# Phase 3a: Stochastic LP (oracle)
STO = {
    "name":        "Stochastic LP\n(Oracle)",
    "short":       "Stoch.",
    "color":       "#4ecdc4",
    "mean_cost":   244_191,
    "stockout_pct": 25.4,
    "annual_penalty": 244_191 * 365 / 1e6,
    "daily_penalty": 240_797,
    "description": "SAA ile gercek\ndagilim bilgisi"
}

# Phase 4: MSE P&O + SPO+ (CSV'den yukle)
ph4 = pd.read_csv(os.path.join(BASE, "data_phase4_summary.csv"))
ph4_mse  = ph4[ph4["model"]=="MSE-P&O"].iloc[0]
ph4_q75  = ph4[ph4["model"]=="Quantile-P75"].iloc[0]
ph4_spo  = ph4[ph4["model"]=="SPO+"].iloc[0]

MSE = {
    "name":        "MSE\nPredict & Opt.",
    "short":       "MSE",
    "color":       "#a29bfe",
    "mean_cost":   ph4_mse["mean_cost"],
    "stockout_pct": ph4_mse["mean_stockout"],
    "annual_penalty": ph4_mse["mean_cost"] * 365 / 1e6,
    "daily_penalty": ph4_mse["mean_cost"] - 3394,
    "description": "MSE tahmini +\nLP optimizasyon"
}

Q75 = {
    "name":        "Quantile P75\nNewsvendor",
    "short":       "Q75",
    "color":       "#fd79a8",
    "mean_cost":   ph4_q75["mean_cost"],
    "stockout_pct": ph4_q75["mean_stockout"],
    "annual_penalty": ph4_q75["mean_cost"] * 365 / 1e6,
    "daily_penalty": ph4_q75["mean_cost"] - 3394,
    "description": "P75 tahmini\n(newsvendor)"
}

SPO = {
    "name":        "SPO+\nDec.-Focused",
    "short":       "SPO+",
    "color":       "#ffe66d",
    "mean_cost":   ph4_spo["mean_cost"],
    "stockout_pct": ph4_spo["mean_stockout"],
    "annual_penalty": ph4_spo["mean_cost"] * 365 / 1e6,
    "daily_penalty": ph4_spo["mean_cost"] - 3394,
    "description": "SPO+ regret\nminimizasyon"
}

MODELS = [DET, STO, Q75, MSE, SPO]

# ─────────────────────────────────────────────
# 2. OZET METRIKLER HESAPLA
# ─────────────────────────────────────────────

# VSS = Value of Stochastic Solution
VSS = DET["mean_cost"] - STO["mean_cost"]
VSS_annual = VSS * 365 / 1e6

# VOL = Value of Learning (SPO+ vs MSE)
VOL = MSE["mean_cost"] - SPO["mean_cost"]
VOL_annual = VOL * 365 / 1e6

# Toplam iyilesme (Det -> SPO+)
total_improvement = (DET["mean_cost"] - SPO["mean_cost"]) / DET["mean_cost"] * 100
total_annual_saving = (DET["mean_cost"] - SPO["mean_cost"]) * 365 / 1e6

stockout_reduction = DET["stockout_pct"] - SPO["stockout_pct"]

print("\n" + "="*72)
print("  ARUTE CIT-SVRP -- ASAMA 5: FINAL KIYASLAMA RAPORU")
print("="*72)
print(f"\n  {'Model':<22} {'Maliyet(TL)':>13} {'Stockout%':>11} {'Yillik(M TL)':>13}")
print("  " + "-"*62)
for m in MODELS:
    print(f"  {m['name'].replace(chr(10),' '):<22} {m['mean_cost']:>13,.0f} "
          f"{'%'+str(round(m['stockout_pct'],1)):>11} "
          f"{m['annual_penalty']:>13.1f}")

print("\n" + "="*72)
print(f"  VSS  (Det->Stoch) : {VSS:>10,.0f} TL/gun  =  {VSS_annual:.1f} M TL/yil")
print(f"  VOL  (MSE->SPO+)  : {VOL:>10,.0f} TL/gun  =  {VOL_annual:.1f} M TL/yil")
print(f"  Toplam (Det->SPO+): {DET['mean_cost']-SPO['mean_cost']:>10,.0f} TL/gun  "
      f"=  {total_annual_saving:.1f} M TL/yil  ({total_improvement:.1f}%)")
print(f"  Stockout azalmasi : %{DET['stockout_pct']:.1f} -> %{SPO['stockout_pct']:.1f}  "
      f"({stockout_reduction:.1f} puan dusus)")
print("="*72)


# ─────────────────────────────────────────────
# 3. GORSELLESTIRME (6 panel)
# ─────────────────────────────────────────────

fig = plt.figure(figsize=(26, 18))
fig.patch.set_facecolor('#0d1117')
gs = gridspec.GridSpec(3, 3, figure=fig,
                       hspace=0.38, wspace=0.32,
                       left=0.06, right=0.97,
                       top=0.91, bottom=0.06)

dark   = '#161b27'
grid_c = '#2a2f3e'

COLORS = [m["color"] for m in MODELS]
SHORTS = [m["short"] for m in MODELS]
COSTS  = [m["mean_cost"] for m in MODELS]
SOS    = [m["stockout_pct"] for m in MODELS]
ANN    = [m["annual_penalty"] for m in MODELS]

# ── [0,0] Gunluk maliyet bar + delta ok ──────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(dark)
ax1.set_title("Ortalama Gunluk Toplam Maliyet", color='white',
              fontsize=11, fontweight='bold', pad=8)

bars = ax1.bar(SHORTS, COSTS, color=COLORS, width=0.6,
               edgecolor='none', zorder=3)
for i, (b, v) in enumerate(zip(bars, COSTS)):
    ax1.text(b.get_x()+b.get_width()/2, v+2000,
             f"{v:,.0f}", ha='center', color='white',
             fontsize=8.5, fontweight='bold')

# iyilesme oku: Det -> SPO+
ax1.annotate("", xy=(4, SPO["mean_cost"]+8000),
             xytext=(0, DET["mean_cost"]+8000),
             arrowprops=dict(arrowstyle="<->", color='#a8e6cf', lw=2))
ax1.text(2, (DET["mean_cost"]+SPO["mean_cost"])/2 + 18000,
         f"−%{total_improvement:.0f}\n({total_annual_saving:.0f}M TL/yil)",
         ha='center', color='#a8e6cf', fontsize=9, fontweight='bold')

ax1.set_ylabel("TL/gun", color='#aaaaaa', fontsize=10)
ax1.tick_params(colors='#aaaaaa')
ax1.grid(True, axis='y', alpha=0.15, color=grid_c, ls='--')
[s.set_edgecolor('#333355') for s in ax1.spines.values()]

# ── [0,1] Stockout orani ─────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(dark)
ax2.set_title("Stockout Orani (%)", color='white',
              fontsize=11, fontweight='bold', pad=8)

bars2 = ax2.bar(SHORTS, SOS, color=COLORS, width=0.6,
                edgecolor='none', zorder=3)
for b, v in zip(bars2, SOS):
    ax2.text(b.get_x()+b.get_width()/2, v+0.3,
             f"%{v:.1f}", ha='center', color='white',
             fontsize=9, fontweight='bold')

# Oracle cizgisi
ax2.axhline(25.4, color='#a8e6cf', lw=1.5, ls='--', label='Oracle (%25.4)')
ax2.legend(facecolor=dark, edgecolor='#444466',
           labelcolor='white', fontsize=8)
ax2.set_ylabel("Stockout Orani (%)", color='#aaaaaa')
ax2.tick_params(colors='#aaaaaa')
ax2.grid(True, axis='y', alpha=0.15, color=grid_c, ls='--')
[s.set_edgecolor('#333355') for s in ax2.spines.values()]

# ── [0,2] Yillik ceza maliyeti huni ─────────────
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(dark)
ax3.set_title("Yillik Toplam Maliyet (M TL)", color='white',
              fontsize=11, fontweight='bold', pad=8)

y_pos = np.arange(len(MODELS))
hbars = ax3.barh(y_pos, ANN, color=COLORS, height=0.55,
                 edgecolor='none', zorder=3)
for i, (b, v) in enumerate(zip(hbars, ANN)):
    ax3.text(v + 1, b.get_y()+b.get_height()/2,
             f"{v:.0f} M", va='center', color='white',
             fontsize=8.5, fontweight='bold')

ax3.set_yticks(y_pos)
ax3.set_yticklabels(SHORTS, color='#aaaaaa', fontsize=10)
ax3.set_xlabel("M TL/yil", color='#aaaaaa')
ax3.tick_params(colors='#aaaaaa')
ax3.grid(True, axis='x', alpha=0.15, color=grid_c, ls='--')
[s.set_edgecolor('#333355') for s in ax3.spines.values()]

# ── [1,0:2] Pipeline: 4 asama akis diyagrami ────
ax4 = fig.add_subplot(gs[1, :2])
ax4.set_facecolor(dark)
ax4.set_title("Pipeline: 4 Asamada Iyilesme Yolculugu",
              color='white', fontsize=11, fontweight='bold', pad=8)
ax4.set_xlim(0, 10); ax4.set_ylim(-0.5, 1.5)
ax4.axis('off')

steps = [
    (1.2,  0.5, "AŞAMA 1\nVeri & SAA",   "#667eea", "365 gun\n100 senaryo"),
    (3.4,  0.5, "AŞAMA 2\nDeterministik", "#ff6b6b", f"Stockout\n%{DET['stockout_pct']:.1f}"),
    (5.6,  0.5, "AŞAMA 3\nStochastic LP", "#4ecdc4", f"Stockout\n%{STO['stockout_pct']:.1f}"),
    (7.8,  0.5, "AŞAMA 4\nSPO+ Learning", "#ffe66d", f"Stockout\n%{SPO['stockout_pct']:.1f}"),
]

for i, (x, y, label, color, sub) in enumerate(steps):
    fancy = mpatches.FancyBboxPatch(
        (x-0.9, y-0.38), 1.8, 0.76,
        boxstyle="round,pad=0.05",
        facecolor=color+'33', edgecolor=color,
        linewidth=2, zorder=3)
    ax4.add_patch(fancy)
    ax4.text(x, y+0.13, label, ha='center', va='center',
             color='white', fontsize=9, fontweight='bold')
    ax4.text(x, y-0.18, sub, ha='center', va='center',
             color=color, fontsize=8.5, fontweight='bold')
    if i < len(steps)-1:
        ax4.annotate("", xy=(steps[i+1][0]-0.92, y),
                     xytext=(x+0.92, y),
                     arrowprops=dict(arrowstyle="-|>",
                                     color='#555577', lw=2))

# iyilesme etiketleri
improves = [
    (2.3, 1.15, "Baseline"),
    (4.5, 1.15, f"VSS = {VSS/1000:.0f}k TL/gun\n−%49.2"),
    (6.7, 1.15, f"VOL = {VOL/1000:.0f}k TL/gun\n−%0.3"),
]
for x, y, txt in improves:
    ax4.text(x, y, txt, ha='center', color='#aaaaaa',
             fontsize=8, style='italic')


# ── [1,2] Ozet kart ──────────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor(dark)
ax5.axis('off')

kpi_texts = [
    ("VSS", f"{VSS_annual:.1f} M TL/yil", "#4ecdc4",
     "Stochastic'in\ndeterministike avantaji"),
    ("VOL", f"{abs(VOL_annual):.2f} M TL/yil", "#ffe66d",
     "Karar odakli\nogrenmenin katkilari"),
    ("Stockout\nAzalmasi", f"−{stockout_reduction:.1f} puan", "#a8e6cf",
     "Det → SPO+"),
    ("Toplam\nTasarruf", f"{total_annual_saving:.1f} M TL/yil", "#ff9f43",
     f"−%{total_improvement:.0f} maliyet"),
]

ax5.set_title("KPI Ozeti", color='white', fontsize=11,
              fontweight='bold', pad=8)
for i, (kpi, val, col, desc) in enumerate(kpi_texts):
    y = 0.82 - i * 0.22
    fancy = mpatches.FancyBboxPatch(
        (0.03, y-0.08), 0.94, 0.18,
        boxstyle="round,pad=0.02",
        facecolor=col+'22', edgecolor=col,
        linewidth=1.5, transform=ax5.transAxes, zorder=3)
    ax5.add_patch(fancy)
    ax5.text(0.18, y+0.01, kpi, transform=ax5.transAxes,
             color=col, fontsize=9, fontweight='bold', va='center')
    ax5.text(0.62, y+0.01, val, transform=ax5.transAxes,
             color='white', fontsize=11, fontweight='bold', va='center')
    ax5.text(0.18, y-0.055, desc, transform=ax5.transAxes,
             color='#777799', fontsize=7.5, va='center')


# ── [2,0:3] Birikimli iyilesme waterfall ────────
ax6 = fig.add_subplot(gs[2, :])
ax6.set_facecolor(dark)
ax6.set_title("Birikimli Iyilesme Analizi: Her Adimin Katkilari",
              color='white', fontsize=11, fontweight='bold', pad=8)

waterfall_steps = [
    ("Deterministik\nBaseline",   DET["mean_cost"],     0,              "#ff6b6b"),
    ("SAA Senaryolari\n(+stoch)", STO["mean_cost"],     DET["mean_cost"],"#4ecdc4"),
    ("MSE Predict\n& Optimize",   MSE["mean_cost"],     STO["mean_cost"],"#a29bfe"),
    ("SPO+ Karar\nOgrenme",       SPO["mean_cost"],     MSE["mean_cost"],"#ffe66d"),
]

prev = DET["mean_cost"]
x_pos = np.arange(len(waterfall_steps))

for i, (label, val, base_val, color) in enumerate(waterfall_steps):
    if i == 0:
        ax6.bar(i, val, color=color+'aa', edgecolor=color, lw=2, width=0.55,
                zorder=3, label="Mutlak Deger")
        ax6.text(i, val+3000, f"{val:,.0f}", ha='center',
                 color='white', fontsize=9, fontweight='bold')
    else:
        delta = val - base_val
        bottom = min(val, base_val)
        ax6.bar(i, abs(delta), bottom=bottom,
                color=color+'99' if delta < 0 else '#ff9f43aa',
                edgecolor=color, lw=2, width=0.55, zorder=3)
        ax6.text(i, bottom + abs(delta)/2,
                 f"{delta:+,.0f} TL\n({delta/base_val*100:+.1f}%)",
                 ha='center', color='white', fontsize=8.5,
                 fontweight='bold', va='center')
        ax6.text(i, val + 2000, f"→{val:,.0f}", ha='center',
                 color='white', fontsize=8, fontweight='bold')
        # Yatay baglanti cizgisi
        ax6.plot([i-0.28, i-0.55-0.28], [val, val],
                 color='#555577', lw=1.5, ls='--')

ax6.set_xticks(x_pos)
ax6.set_xticklabels([s[0] for s in waterfall_steps],
                     color='#aaaaaa', fontsize=10)
ax6.set_ylabel("Ortalama Gunluk Maliyet (TL)", color='#aaaaaa')
ax6.tick_params(colors='#aaaaaa')
ax6.grid(True, axis='y', alpha=0.15, color=grid_c, ls='--')
[s.set_edgecolor('#333355') for s in ax6.spines.values()]

# Renk aciklamalari
handles = [mpatches.Patch(color=c+'aa', label=l)
           for l, c in [("Azalma","#4ecdc4"), ("Baslangic","#ff6b6b")]]
ax6.legend(handles=handles, facecolor=dark, edgecolor='#444466',
           labelcolor='white', fontsize=9, loc='upper right')


# ── Baslik ──────────────────────────────────────
fig.text(0.5, 0.955,
         "ARUTE CIT-SVRP — END-TO-END KIYASLAMA RAPORU",
         ha='center', va='top', color='white',
         fontsize=16, fontweight='bold')
fig.text(0.5, 0.935,
         "Deterministik Baseline → Stochastic LP → MSE P&O → SPO+ Karar Odakli Ogrenme",
         ha='center', va='top', color='#8899bb',
         fontsize=10)

out = os.path.join(BASE, "phase5_final_report.png")
plt.savefig(out, dpi=150, bbox_inches='tight',
            facecolor='#0d1117', edgecolor='none')
plt.close()
print(f"\n  [SAVED] {out}")


# ─────────────────────────────────────────────
# 4. CSV RAPORU
# ─────────────────────────────────────────────

report = pd.DataFrame([{
    "sistem":          m["short"],
    "aciklama":        m["description"].replace("\n"," "),
    "gunluk_maliyet":  round(m["mean_cost"]),
    "stockout_pct":    round(m["stockout_pct"],1),
    "yillik_maliyet_M": round(m["annual_penalty"],1),
    "det_e_gore_pct":  round((DET["mean_cost"]-m["mean_cost"])/DET["mean_cost"]*100,1),
} for m in MODELS])

report.to_csv(os.path.join(BASE, "data_phase5_report.csv"), index=False)
print(f"  [SAVED] data_phase5_report.csv")

print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║         ARUTE CIT-SVRP -- PROJE TAMAMLANDI                         ║
╠══════════════════════════════════════════════════════════════════════╣
║  Asama 1 ✅  Veri modellemesi  (365 gun, 100 senaryo, 20 ATM)       ║
║  Asama 2 ✅  Deterministik CVRP baseline  → Stockout %42.4          ║
║  Asama 3 ✅  Two-Stage Stochastic LP      → Stockout %25.4          ║
║  Asama 4 ✅  SPO+ Karar Odakli Ogrenme   → Stockout %25.8          ║
║  Asama 5 ✅  Final Kiyaslama Raporu                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║  TOPLAM KAZANIM (Det -> SPO+):                                      ║
║    Gunluk  : {DET['mean_cost']-SPO['mean_cost']:>8,.0f} TL/gun tasarruf                      ║
║    Yillik  : {total_annual_saving:>8.1f} M TL/yil tasarruf                    ║
║    Stockout: %{DET['stockout_pct']:.1f} → %{SPO['stockout_pct']:.1f}  (−{stockout_reduction:.1f} puan)               ║
║    VSS     : {VSS_annual:>8.1f} M TL/yil (stochastigin degeri)        ║
╚══════════════════════════════════════════════════════════════════════╝
""")
