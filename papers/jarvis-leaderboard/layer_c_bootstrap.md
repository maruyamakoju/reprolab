# Layer C Bootstrap - JARVIS Close Adjacent Pairs

This is a paired, nonparametric bootstrap over fixed public test rows for
the closest adjacent pairs identified by `layer_c_resolution.md`.

It is not a retraining uncertainty estimate and does not sample alternate
train/validation/test splits. It only tests whether the observed paired
test-row advantage of the official higher-ranked model is stable under
resampling of the published test set.

## Settings

- Bootstrap draws: 2000
- Seed: 42
- Pairs checked: 20

## Results

| rank | target | metric | official pair | rows | official gap | paired advantage | 95% CI | P(tie/reversal) |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coNGN over potnet | 5572 | 0.00020000 | 0.00016852 | [-0.00160975, 0.00156560] | 0.4030 |
| 2 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | alignn_model over kgcnn_schnet | 5572 | 0.00070000 | 0.00068863 | [-0.00285602, 0.00462995] | 0.3635 |
| 3 | `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | matminer_rf over alignn_model | 5222 | 0.00080000 | 0.00076599 | [-0.00555343, 0.00746840] | 0.4245 |
| 4 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | matformer_256 over alignn_model | 5572 | 0.00090000 | 0.00093247 | [-0.00016749, 0.00204791] | 0.0470 |
| 5 | `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | alignn_model over matminer_rf | 5572 | 0.00090000 | 0.00089734 | [-0.00574300, 0.00789663] | 0.3940 |
| 6 | `SinglePropertyClass / slme / dft_3d` | ACC | matminer_rf over matminer_xgboost | 906 | 0.00110000 | 0.00110375 | [-0.01545254, 0.01876380] | 0.4555 |
| 7 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | 5572 | 0.00110000 | 0.00111477 | [-0.00006757, 0.00254979] | 0.0390 |
| 8 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | 5537 | 0.00110000 | 0.00107191 | [-0.00321573, 0.00501498] | 0.3075 |
| 9 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_rf over cgcnn_model | 5572 | 0.00130000 | 0.00136523 | [-0.00857241, 0.01167811] | 0.4240 |
| 10 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | 5572 | 0.00160000 | 0.00158357 | [-0.00966971, 0.01293096] | 0.3860 |
| 11 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | 5537 | 0.00190000 | 0.00191120 | [-0.00189713, 0.00609254] | 0.1655 |
| 12 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_schnet over kgcnn_megnet | 5572 | 0.00190000 | 0.00190516 | [0.00046759, 0.00331262] | 0.0050 |
| 13 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | 5572 | 0.00200000 | 0.00198041 | [0.00073827, 0.00336273] | 0.0000 |
| 14 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_megnet over kgcnn_cgcnn | 5537 | 0.00210000 | 0.00210703 | [-0.00182812, 0.00635259] | 0.1545 |
| 15 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | potnet over kgcnn_coNGN | 5572 | 0.00210000 | 0.00205851 | [-0.00626258, 0.01019696] | 0.3120 |
| 16 | `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | alignn_model over matminer_rf | 2321 | 0.00220000 | 0.00215424 | [-0.00904782, 0.01379793] | 0.3775 |
| 17 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_xgboost over matminer_rf | 5572 | 0.00220000 | 0.00213012 | [-0.00256972, 0.00645132] | 0.1855 |
| 18 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_dimenetPP over kgcnn_cgcnn | 5572 | 0.00230000 | 0.00226462 | [-0.00414618, 0.00743016] | 0.2270 |
| 19 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_coGN over potnet | 5572 | 0.00270000 | 0.00274677 | [-0.00438651, 0.01058822] | 0.2325 |
| 20 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | potnet over matformer_256 | 5572 | 0.00290000 | 0.00292089 | [0.00205824, 0.00384399] | 0.0000 |

## Interpretation

- Pairs whose 95% CI includes zero: 17 / 20
- `paired advantage` is positive when the official higher-ranked model has
  the better metric on the resampled test set.
- For MAE/MULTIMAE, advantage is mean(error_lower-ranked - error_higher-ranked).
- For ACC, advantage is mean(correct_higher-ranked - correct_lower-ranked).
- A high `P(tie/reversal)` means the official adjacent ordering is fragile
  under this fixed-test-set bootstrap.

Pairs with CI crossing zero:

| target | metric | pair | 95% CI | P(tie/reversal) |
|---|---|---|---:|---:|
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coNGN over potnet | [-0.00160975, 0.00156560] | 0.4030 |
| `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | alignn_model over kgcnn_schnet | [-0.00285602, 0.00462995] | 0.3635 |
| `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | matminer_rf over alignn_model | [-0.00555343, 0.00746840] | 0.4245 |
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | matformer_256 over alignn_model | [-0.00016749, 0.00204791] | 0.0470 |
| `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | alignn_model over matminer_rf | [-0.00574300, 0.00789663] | 0.3940 |
| `SinglePropertyClass / slme / dft_3d` | ACC | matminer_rf over matminer_xgboost | [-0.01545254, 0.01876380] | 0.4555 |
| `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | [-0.00006757, 0.00254979] | 0.0390 |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | [-0.00321573, 0.00501498] | 0.3075 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_rf over cgcnn_model | [-0.00857241, 0.01167811] | 0.4240 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | [-0.00966971, 0.01293096] | 0.3860 |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | [-0.00189713, 0.00609254] | 0.1655 |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_megnet over kgcnn_cgcnn | [-0.00182812, 0.00635259] | 0.1545 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | potnet over kgcnn_coNGN | [-0.00626258, 0.01019696] | 0.3120 |
| `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | alignn_model over matminer_rf | [-0.00904782, 0.01379793] | 0.3775 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_xgboost over matminer_rf | [-0.00256972, 0.00645132] | 0.1855 |
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_dimenetPP over kgcnn_cgcnn | [-0.00414618, 0.00743016] | 0.2270 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_coGN over potnet | [-0.00438651, 0.01058822] | 0.2325 |
