# Layer C — Statistical audit of the Matbench Discovery leaderboard

Subset: `unique_prototypes` (n=215,488); models: CHGNet, SevenNet-0, MACE-MP-0, ORB v2; paired bootstrap B=2000, seed=42; each_pred built by the exact Layer A path (`compare_metrics.build_each_pred`). **Exploratory analysis** (not pre-registered, unlike Layer B).


## Q1 — Uncertainty and ranking significance (not reported upstream)

| model | F1 | 95% CI | CI width | MAE eV/atom | 95% CI |
|---|---|---|---|---|---|
| ORB v2 | 0.8801 | [0.8775, 0.8827] | 0.0052 | 0.0282 | [0.0279, 0.0285] |
| SevenNet-0 | 0.7244 | [0.7207, 0.7281] | 0.0074 | 0.0484 | [0.0481, 0.0487] |
| MACE-MP-0 | 0.6695 | [0.6657, 0.6733] | 0.0076 | 0.0569 | [0.0566, 0.0573] |
| CHGNet | 0.6126 | [0.6087, 0.6165] | 0.0078 | 0.0635 | [0.0631, 0.0638] |

| pair (better vs worse) | ΔF1 | 95% CI | P(flip) |
|---|---|---|---|
| ORB v2 vs SevenNet-0 | +0.1557 | [+0.1519, +0.1596] | 0 |
| ORB v2 vs MACE-MP-0 | +0.2107 | [+0.2066, +0.2147] | 0 |
| ORB v2 vs CHGNet | +0.2675 | [+0.2634, +0.2718] | 0 |
| SevenNet-0 vs MACE-MP-0 | +0.0550 | [+0.0515, +0.0582] | 0 |
| SevenNet-0 vs CHGNet | +0.1118 | [+0.1083, +0.1153] | 0 |
| MACE-MP-0 vs CHGNet | +0.0569 | [+0.0536, +0.0601] | 0 |

Context — leaderboard resolution: the widest 95% CI measured here is 0.0078 F1. On the full leaderboard at this commit (60 models with a uniq-protos F1), **43 of 59 adjacent pairs are separated by less than that CI width**, i.e. their published order is unlikely to be statistically resolvable without a paired significance test:
  - EquiformerV3+DeNS-OAM vs EquFlashV2: ΔF1 = 0.002
  - EquFlashV2 vs TACE-OAM-RRA-Preview: ΔF1 = 0.001
  - TACE-OAM-RRA-Preview vs eSEN-30M-OAM: ΔF1 = 0.003
  - eSEN-30M-OAM vs PET-OAM-XL: ΔF1 = 0.001
  - PET-OAM-XL vs MatRIS-10M-OAM: ΔF1 = 0.003
  - MatRIS-10M-OAM vs EquFlash: ΔF1 = 0.002
  - EquFlash vs eqV2 M: ΔF1 = 0.002
  - eqV2 M vs TACE-OAM-L: ΔF1 = 0.007
  - TACE-OAM-L vs Nequip-OAM-XL: ΔF1 = 0.004
  - Nequip-OAM-XL vs SevenNet-Omni-i12: ΔF1 = 0.000
  - SevenNet-Omni-i12 vs ORB v3: ΔF1 = 0.001
  - ORB v3 vs AlphaNet-v1-OAM: ΔF1 = 0.004
  - AlphaNet-v1-OAM vs SevenNet-MF-ompa: ΔF1 = 0.000
  - SevenNet-MF-ompa vs Allegro-OAM-L: ΔF1 = 0.006
  - Allegro-OAM-L vs Nequip-OAM-L: ΔF1 = 0.002
  - Nequip-OAM-L vs DPA3-v2-OpenLAM: ΔF1 = 0.003
  - DPA3-v2-OpenLAM vs TACE-v1-OAM-M: ΔF1 = 0.001
  - TACE-v1-OAM-M vs DPA-3.1-3M-FT: ΔF1 = 0.005
  - DPA-3.1-3M-FT vs DPA3-v1-OpenLAM: ΔF1 = 0.001
  - DPA3-v1-OpenLAM vs GRACE-2L-OAM-L: ΔF1 = 0.000
  - GRACE-2L-OAM-L vs GRACE-2L-OAM: ΔF1 = 0.003
  - GRACE-2L-OAM vs ORB v2: ΔF1 = 0.000
  - EquiformerV3+DeNS-MP vs MatterSim v1 5M: ΔF1 = 0.001
  - MatterSim v1 5M vs DPA-4.0.1-Pro-MPtrj: ΔF1 = 0.005
  - DPA-4.0.1-Pro-MPtrj vs MACE-MPA-0: ΔF1 = 0.005
  - MACE-MPA-0 vs DPA-4.0-Pro-MPtrj: ΔF1 = 0.002
  - DPA-4.0-Pro-MPtrj vs MatRIS-10M-MP: ΔF1 = 0.003
  - eSEN-30M-MP vs GNoME: ΔF1 = 0.002
  - GNoME vs GRACE-1L-OAM: ΔF1 = 0.005
  - eqV2 S DeNS vs MatRIS v0.5.0 MPtrj: ΔF1 = 0.006
  - MatRIS v0.5.0 MPtrj vs DPA-3.1-MPtrj: ΔF1 = 0.006
  - DPA-3.1-MPtrj vs AlphaNet-v1-MPtrj: ΔF1 = 0.004
  - DPA3-v2-MPtrj vs Eqnorm MPtrj: ΔF1 = 0.000
  - DPA3-v1-MPtrj vs ORB v2 MPtrj: ΔF1 = 0.000
  - ORB v2 MPtrj vs Nequip-MP-L: ΔF1 = 0.004
  - Nequip-MP-L vs SevenNet-l3i5: ΔF1 = 0.001
  - Allegro-MP-L vs Nequix MP: ΔF1 = 0.000
  - Nequix MP vs Nequix MP PFT: ΔF1 = 0.003
  - ESNet vs M3GNet: ΔF1 = 0.003
  - M3GNet vs ALIGNN: ΔF1 = 0.002
  - MEGNet vs CGCNN: ΔF1 = 0.003
  - CGCNN vs CGCNN+P: ΔF1 = 0.007
  - BOWSR vs AlchemBERT: ΔF1 = 0.002

(Caveat: CI width varies by model; a definitive statement needs the paired bootstrap on each pair's prediction files, as done above for four models. The point stands that the leaderboard reports no uncertainty at all while many gaps are of this order.)

## Q2 — Sensitivity to the 0 eV/atom stability threshold

Same threshold applied to truth and predictions (leaderboard convention in `stable_metrics`). DFT hull energies themselves carry O(10 meV/atom) uncertainty, so ranking stability inside this band matters.

| τ (meV/atom) | ORB v2 | SevenNet-0 | MACE-MP-0 | CHGNet | ranking |
|---|---|---|---|---|---|
| -100 | 0.8803 | 0.7266 | 0.6406 | 0.6367 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -75 | 0.8773 | 0.7126 | 0.6321 | 0.6145 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -50 | 0.8787 | 0.7052 | 0.6303 | 0.6005 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -40 | 0.8775 | 0.7073 | 0.6351 | 0.5990 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -30 | 0.8783 | 0.7076 | 0.6409 | 0.5988 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -20 | 0.8816 | 0.7126 | 0.6506 | 0.6007 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -10 | 0.8820 | 0.7163 | 0.6554 | 0.6007 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -5 | 0.8794 | 0.7195 | 0.6614 | 0.6058 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +0 | 0.8801 | 0.7244 | 0.6695 | 0.6126 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +5 | 0.8817 | 0.7361 | 0.6820 | 0.6264 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +10 | 0.8853 | 0.7479 | 0.6970 | 0.6419 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +20 | 0.8942 | 0.7722 | 0.7274 | 0.6747 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +30 | 0.9028 | 0.7944 | 0.7562 | 0.7073 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +40 | 0.9095 | 0.8122 | 0.7775 | 0.7351 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +50 | 0.9167 | 0.8274 | 0.7984 | 0.7628 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +75 | 0.9288 | 0.8612 | 0.8367 | 0.8120 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +100 | 0.9385 | 0.8867 | 0.8675 | 0.8487 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |

The τ=0 ranking is unchanged at every swept threshold in [-100, +100] meV/atom.

## Q3 — Error correlation and joint blind spots

Signed formation-energy errors (e_form_pred − e_form_dft), common non-NaN rows (n=215,453).

| Pearson | CHGNet | SevenNet-0 | MACE-MP-0 | ORB v2 |
|---|---|---|---|---|
| CHGNet | 1.000 | 0.765 | 0.764 | 0.449 |
| SevenNet-0 | 0.765 | 1.000 | 0.765 | 0.507 |
| MACE-MP-0 | 0.764 | 0.765 | 1.000 | 0.431 |
| ORB v2 | 0.449 | 0.507 | 0.431 | 1.000 |

| Spearman | CHGNet | SevenNet-0 | MACE-MP-0 | ORB v2 |
|---|---|---|---|---|
| CHGNet | 1.000 | 0.667 | 0.677 | 0.157 |
| SevenNet-0 | 0.667 | 1.000 | 0.653 | 0.231 |
| MACE-MP-0 | 0.677 | 0.653 | 1.000 | 0.187 |
| ORB v2 | 0.157 | 0.231 | 0.187 | 1.000 |

- Among the 33,374 DFT-stable structures, **3.59%** are missed (FN) by *all four* models simultaneously; under error independence this would be 0.14% (joint-miss lift **25x**). Per-model miss rates: CHGNet 24.2%, SevenNet-0 18.2%, MACE-MP-0 20.4%, ORB v2 15.9%.
- In the near-hull band |E_hull| ≤ 50 meV/atom (n=66,576), all four models misclassify the same structure 2.61% of the time vs 0.21% under independence (lift 12x).
- Unique true positives (stable materials found by that model and missed by the other three): CHGNet 341, SevenNet-0 361, MACE-MP-0 388, ORB v2 1,886.

## Limitations

- Bootstrap treats WBM as an i.i.d. sample; WBM structures are generated by element substitution from shared seeds, so effective sample size is somewhat smaller than n — CIs here are, if anything, slightly narrow.
- Threshold sweep reuses the same data at every τ (no multiple-comparison correction); it is a sensitivity analysis, not a hypothesis test.
- Analyses are exploratory and were designed after Layers A/B; they should be treated as descriptive audit findings, not confirmatory statistics.
