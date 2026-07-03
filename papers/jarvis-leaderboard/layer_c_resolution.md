# Leaderboard Resolution - JARVIS Layer A

This is a point-gap analysis of the 14 checked JARVIS-Leaderboard pages.
It is not an uncertainty estimate. It only asks how close adjacent official
point estimates are after sorting each page by its metric direction.

## Aggregate

- Reports checked: 14
- Submissions checked: 101
- Adjacent pairs: 87
- Adjacent gaps <= 0.001: 5
- Adjacent gaps <= 0.005: 29
- Adjacent gaps <= 0.010: 38

## Per-page Summary

| target | metric | models | adjacent pairs | min gap | median gap | gaps <= 0.001 | gaps <= 0.005 | closest pair |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | 3 | 2 | 0.00080000 | 0.00195000 | 1 | 2 | matminer_rf to alignn_model |
| `SinglePropertyClass / mbj_bandgap / dft_3d` | ACC | 3 | 2 | 0.00710000 | 0.00850000 | 0 | 0 | matminer_xgboost to matminer_rf |
| `SinglePropertyClass / n_powerfact / dft_3d` | ACC | 3 | 2 | 0.01210000 | 0.01445000 | 0 | 0 | matminer_xgboost to matminer_rf |
| `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | 3 | 2 | 0.00090000 | 0.00215000 | 1 | 2 | alignn_model to matminer_rf |
| `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | 3 | 2 | 0.00220000 | 0.00475000 | 0 | 1 | alignn_model to matminer_rf |
| `SinglePropertyClass / slme / dft_3d` | ACC | 3 | 2 | 0.00110000 | 0.00555000 | 0 | 1 | matminer_rf to matminer_xgboost |
| `SinglePropertyClass / spillage / dft_3d` | ACC | 3 | 2 | 0.00530000 | 0.01145000 | 0 | 0 | matminer_xgboost to matminer_rf |
| `SinglePropertyPrediction / bulk_modulus_kv / dft_3d` | MAE | 12 | 11 | 0.08910000 | 0.41390000 | 0 | 0 | matminer_rf to cfid |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | 11 | 10 | 0.00110000 | 0.00765000 | 0 | 5 | kgcnn_cgcnn to matminer_xgboost |
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | 15 | 14 | 0.00020000 | 0.00605000 | 2 | 6 | kgcnn_coNGN to potnet |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | 14 | 13 | 0.00130000 | 0.01130000 | 0 | 6 | matminer_rf to cgcnn_model |
| `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | 14 | 13 | 0.00070000 | 0.00740000 | 1 | 6 | alignn_model to kgcnn_schnet |
| `SinglePropertyPrediction / slme / dft_3d` | MAE | 13 | 12 | 0.00790000 | 0.09520000 | 0 | 0 | kgcnn_coNGN to kgcnn_coGN |
| `Spectra / ph_dos / edos_pdos` | MULTIMAE | 1 | 0 | n/a | n/a | 0 | 0 | n/a |

## Closest Adjacent Pairs

| rank | target | metric | pair | official gap | reproduced gap |
|---:|---|---|---|---:|---:|
| 1 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coNGN to potnet | 0.00020000 | 0.00016852 |
| 2 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | alignn_model to kgcnn_schnet | 0.00070000 | 0.00068863 |
| 3 | `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | matminer_rf to alignn_model | 0.00080000 | 0.00076599 |
| 4 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | matformer_256 to alignn_model | 0.00090000 | 0.00093247 |
| 5 | `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | alignn_model to matminer_rf | 0.00090000 | 0.00089734 |
| 6 | `SinglePropertyClass / slme / dft_3d` | ACC | matminer_rf to matminer_xgboost | 0.00110000 | 0.00110376 |
| 7 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_coGN to kgcnn_coNGN | 0.00110000 | 0.00111477 |
| 8 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_cgcnn to matminer_xgboost | 0.00110000 | 0.00107190 |
| 9 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_rf to cgcnn_model | 0.00130000 | 0.00136523 |
| 10 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_cgcnn to matminer_xgboost | 0.00160000 | 0.00158356 |
| 11 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_coGN to kgcnn_coNGN | 0.00190000 | 0.00191120 |
| 12 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_schnet to kgcnn_megnet | 0.00190000 | 0.00190516 |
| 13 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coGN to kgcnn_coNGN | 0.00200000 | 0.00198041 |
| 14 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_megnet to kgcnn_cgcnn | 0.00210000 | 0.00210703 |
| 15 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | potnet to kgcnn_coNGN | 0.00210000 | 0.00205852 |
| 16 | `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | alignn_model to matminer_rf | 0.00220000 | 0.00215424 |
| 17 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_xgboost to matminer_rf | 0.00220000 | 0.00213012 |
| 18 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_dimenetPP to kgcnn_cgcnn | 0.00230000 | 0.00226462 |
| 19 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_coGN to potnet | 0.00270000 | 0.00274676 |
| 20 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | potnet to matformer_256 | 0.00290000 | 0.00292089 |

## Interpretation

The checked pages contain many adjacent point estimates below 0.005 in metric
units. Those small gaps are the natural targets for a later uncertainty,
split-sensitivity, or bootstrap-style analysis. Layer A already established
that these point estimates are internally reproducible from public artifacts.
