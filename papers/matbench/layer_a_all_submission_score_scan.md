# Matbench v0.1 all-submission score scan

- Submissions checked: 28
- Submission/task records checked: 180
- Folds checked: 900
- Max absolute stored-vs-recomputed score delta: 1.217e+01
- Failing folds at tolerance 1e-12: 5
- Classification folds checked: 135
- Classification folds with stored `rocauc == balanced_accuracy`: 135

## Per-submission summary

| Submission | Tasks | Folds | Max score delta | Failing folds |
|---|---:|---:|---:|---:|
| matbench_v0.1_Auto-sklearn | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_Ax_10_90_CrabNet_v1.2.7 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_Ax_CrabNet_v1.2.1 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_CrabNet | 10 | 50 | 8.882e-16 | 0 |
| matbench_v0.1_CrabNet_v1.2.1 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_DeeperGATGNN | 8 | 40 | 8.882e-16 | 0 |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | 9 | 45 | 1.776e-15 | 0 |
| matbench_v0.1_Finder_v1.2_composition | 8 | 40 | 8.882e-16 | 0 |
| matbench_v0.1_Finder_v1.2_structure | 8 | 40 | 1.776e-15 | 0 |
| matbench_v0.1_GN-OA | 1 | 5 | 1.217e+01 | 5 |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | 9 | 45 | 1.776e-15 | 0 |
| matbench_v0.1_RFLR | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_SchNet_kgcnn_v2.1.0 | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_TPOT | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_alignn | 9 | 45 | 1.776e-15 | 0 |
| matbench_v0.1_automatminer_expressv2020 | 13 | 65 | 4.441e-16 | 0 |
| matbench_v0.1_cgcnnv2019 | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_coGN | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_coNGN | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_darwin | 4 | 20 | 1.110e-16 | 0 |
| matbench_v0.1_dummy | 13 | 65 | 3.553e-15 | 0 |
| matbench_v0.1_gptchem | 4 | 20 | 1.110e-16 | 0 |
| matbench_v0.1_lattice_xgboost | 1 | 5 | 1.776e-15 | 0 |
| matbench_v0.1_matformer | 1 | 5 | 1.110e-16 | 0 |
| matbench_v0.1_modnet_v0.1.10 | 13 | 65 | 1.776e-15 | 0 |
| matbench_v0.1_modnet_v0.1.12 | 13 | 65 | 1.776e-15 | 0 |
| matbench_v0.1_rf | 13 | 65 | 1.776e-15 | 0 |

## Task coverage

| Task | Submission records |
|---|---:|
| matbench_dielectric | 16 |
| matbench_expt_gap | 12 |
| matbench_expt_is_metal | 7 |
| matbench_glass | 7 |
| matbench_jdft2d | 16 |
| matbench_log_gvrh | 16 |
| matbench_log_kvrh | 16 |
| matbench_mp_e_form | 18 |
| matbench_mp_gap | 16 |
| matbench_mp_is_metal | 13 |
| matbench_perovskites | 16 |
| matbench_phonons | 16 |
| matbench_steels | 11 |

## Largest score deltas

| Submission | Task | Fold | n | Prediction type | Worst metric | Max delta | Stored rocauc | Stored bal. acc. | Probability rocauc |
|---|---|---|---:|---|---|---:|---:|---:|---:|
| matbench_v0.1_GN-OA | matbench_mp_e_form | 0 | 26551 | float | mape | 1.217e+01 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 4 | 26550 | float | mape | 1.199e+01 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 3 | 26550 | float | mape | 1.165e+01 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 2 | 26550 | float | mape | 9.114e+00 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 1 | 26551 | float | mape | 7.809e+00 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_e_form | 0 | 26551 | float | mape | 3.553e-15 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_gap | 1 | 21223 | float | mape | 3.553e-15 |  |  |  |
| matbench_v0.1_alignn | matbench_mp_gap | 2 | 21223 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_e_form | 3 | 26550 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_gap | 0 | 21223 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_Finder_v1.2_structure | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_lattice_xgboost | matbench_mp_e_form | 0 | 26551 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_lattice_xgboost | matbench_mp_e_form | 4 | 26550 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_modnet_v0.1.10 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_modnet_v0.1.12 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_rf | matbench_mp_gap | 0 | 21223 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_rf | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_rf | matbench_mp_gap | 4 | 21222 | float | mape | 1.776e-15 |  |  |  |

## Failures

| Submission | Task | Fold | Problem |
|---|---|---|---|
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_0 | delta 1.217e+01 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_1 | delta 7.809e+00 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_2 | delta 9.114e+00 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_3 | delta 1.165e+01 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_4 | delta 1.199e+01 |
