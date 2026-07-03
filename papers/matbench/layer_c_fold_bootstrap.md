# Matbench v0.1 fold-bootstrap adjacent-pair screen

This is a follow-up to `layer_c_leaderboard_resolution.md`. It takes the closest adjacent leaderboard pairs by gap/fold-SE proxy, then bootstraps the five paired fold-score differences. Positive differences mean the higher-ranked submission remains better under the task's primary metric.

This is a lightweight fold-level uncertainty screen, not a formal statistical test. It has only five folds per pair, and classification uses stored `rocauc`, which behaves as thresholded-label AUC / balanced accuracy for the checked records.

- Adjacent pairs checked: 25
- Bootstrap draws per pair: 20000
- RNG seed: 0
- 95% bootstrap CIs including zero: 25
- P(bootstrapped gap <= 0) >= 0.05: 25
- Exact adjacent ties in checked set: 6

## Pair results

| Task | Rank | Better | Worse | Metric | Gap | Gap / SE | CI low | CI high | P(gap <= 0) | CI includes 0 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---|
| matbench_expt_is_metal | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | rocauc | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_log_gvrh | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_log_kvrh | 3 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_mp_e_form | 11 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_mp_gap | 8 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_perovskites | 10 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_dielectric | 4 | matbench_v0.1_coNGN | matbench_v0.1_automatminer_expressv2020 | mae | 0.00087203 | 0.0433745 | -0.0386628 | 0.0310366 | 0.4255 | yes |
| matbench_dielectric | 11 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | mae | 0.000941329 | 0.0605722 | -0.0256149 | 0.0274976 | 0.4681 | yes |
| matbench_expt_gap | 4 | matbench_v0.1_CrabNet | matbench_v0.1_modnet_v0.1.10 | mae | 0.000750008 | 0.0659425 | -0.0183764 | 0.0211091 | 0.4725 | yes |
| matbench_jdft2d | 8 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_CrabNet | mae | 0.14923 | 0.0721843 | -3.96875 | 3.24105 | 0.45805 | yes |
| matbench_mp_is_metal | 6 | matbench_v0.1_modnet_v0.1.12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | rocauc | 0.000641083 | 0.110668 | -0.0103745 | 0.00988183 | 0.42745 | yes |
| matbench_phonons | 1 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_coNGN | mae | 0.126783 | 0.111603 | -2.15202 | 1.43937 | 0.3151 | yes |
| matbench_dielectric | 6 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_Finder_v1.2_composition | mae | 0.000709045 | 0.112774 | -0.0108184 | 0.0107964 | 0.4384 | yes |
| matbench_jdft2d | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_cgcnnv2019 | mae | 0.219754 | 0.113498 | -2.65548 | 4.00417 | 0.48355 | yes |
| matbench_mp_gap | 2 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.000314041 | 0.116606 | -0.00410629 | 0.0054197 | 0.4557 | yes |
| matbench_perovskites | 2 | matbench_v0.1_alignn | matbench_v0.1_DeeperGATGNN | mae | 4.58128e-05 | 0.11789 | -0.000680917 | 0.000624587 | 0.427 | yes |
| matbench_glass | 2 | matbench_v0.1_automatminer_expressv2020 | matbench_v0.1_rf | rocauc | 0.00197173 | 0.161961 | -0.0212167 | 0.0204627 | 0.39925 | yes |
| matbench_expt_gap | 2 | matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | matbench_v0.1_modnet_v0.1.12 | mae | 0.00169891 | 0.172421 | -0.0122981 | 0.0209692 | 0.47005 | yes |
| matbench_mp_e_form | 8 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.000237907 | 0.180593 | -0.00200926 | 0.0027376 | 0.41045 | yes |
| matbench_dielectric | 7 | matbench_v0.1_Finder_v1.2_composition | matbench_v0.1_CrabNet | mae | 0.00298632 | 0.18945 | -0.0284995 | 0.0257243 | 0.3892 | yes |
| matbench_mp_gap | 7 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_modnet_v0.1.10 | mae | 0.000589556 | 0.200367 | -0.00371107 | 0.00643074 | 0.4289 | yes |
| matbench_dielectric | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_alignn | mae | 0.00491146 | 0.207455 | -0.0403924 | 0.0368495 | 0.39215 | yes |
| matbench_steels | 5 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_automatminer_expressv2020 | mae | 1.279 | 0.210305 | -9.01348 | 12.1864 | 0.42925 | yes |
| matbench_log_gvrh | 8 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_automatminer_expressv2020 | mae | 0.000299287 | 0.227668 | -0.00190315 | 0.00267186 | 0.4104 | yes |
| matbench_expt_is_metal | 3 | matbench_v0.1_rf | matbench_v0.1_modnet_v0.1.10 | rocauc | 0.000607287 | 0.237515 | -0.00430554 | 0.00468892 | 0.37515 | yes |

## Interpretation

For these closest adjacent pairs, a CI crossing zero means the five-fold score pattern does not stably separate the two neighboring submissions under this coarse fold-bootstrap screen. Exact ties are deterministic ties in the stored fold scores.
