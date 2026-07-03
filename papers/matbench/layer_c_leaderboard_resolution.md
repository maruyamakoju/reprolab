# Matbench v0.1 leaderboard resolution map

This uses stored fold scores from public `results.json.gz` artifacts. For each task, submissions are ranked by the primary leaderboard metric (`mae` for regression, stored `rocauc` for classification), then adjacent mean gaps are compared with a fold-level standard-error proxy from the five paired fold-score differences.

Classification caveat: the stored `rocauc` values in these artifacts behave as thresholded-label AUC / balanced accuracy for the checked records, as documented in the classification probe.

- Submission-task rows ranked: 180
- Tasks ranked: 13
- Adjacent pairs: 167
- Exact adjacent ties: 6
- Adjacent gaps <= 1 fold-SE proxy: 68
- Adjacent gaps <= 2 fold-SE proxy: 87
- Regression adjacent pairs: 143
- Classification adjacent pairs: 24

## Per-task resolution

| Task | Type | Metric | Entries | Adjacent pairs | Exact ties | <=1 SE | <=2 SE | Min gap | Median gap | Min gap / SE |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| matbench_dielectric | regression | mae | 16 | 15 | 0 | 11 | 11 | 0.000709045 | 0.00491146 | 0.0433745 |
| matbench_expt_gap | regression | mae | 12 | 11 | 0 | 5 | 7 | 0.000750008 | 0.0125305 | 0.0659425 |
| matbench_expt_is_metal | classification | rocauc | 7 | 6 | 1 | 2 | 3 | 0 | 0.0118908 | 0 |
| matbench_glass | classification | rocauc | 7 | 6 | 0 | 1 | 2 | 0.00197173 | 0.0412622 | 0.161961 |
| matbench_jdft2d | regression | mae | 16 | 15 | 0 | 11 | 14 | 0.14923 | 1.34496 | 0.0721843 |
| matbench_log_gvrh | regression | mae | 16 | 15 | 1 | 5 | 6 | 0 | 0.00188593 | 0 |
| matbench_log_kvrh | regression | mae | 16 | 15 | 1 | 4 | 6 | 0 | 0.00202217 | 0 |
| matbench_mp_e_form | regression | mae | 18 | 17 | 1 | 4 | 4 | 0 | 0.00225949 | 0 |
| matbench_mp_gap | regression | mae | 16 | 15 | 1 | 3 | 5 | 0 | 0.0134738 | 0 |
| matbench_mp_is_metal | classification | rocauc | 13 | 12 | 0 | 6 | 6 | 0.000383175 | 0.0040911 | 0.110668 |
| matbench_perovskites | regression | mae | 16 | 15 | 1 | 3 | 4 | 0 | 0.00301299 | 0 |
| matbench_phonons | regression | mae | 16 | 15 | 0 | 8 | 11 | 0.126783 | 1.59285 | 0.111603 |
| matbench_steels | regression | mae | 11 | 10 | 0 | 5 | 8 | 1.279 | 5.54138 | 0.210305 |

## Closest adjacent pairs by fold-SE proxy

| Task | Rank | Better | Worse | Metric | Better mean | Worse mean | Gap | Fold-SE proxy | Gap / SE |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| matbench_expt_is_metal | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | rocauc | 0.916052 | 0.916052 | 0 | 0 | 0 |
| matbench_log_gvrh | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.0731162 | 0.0731162 | 0 | 0 | 0 |
| matbench_log_kvrh | 3 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.05477 | 0.05477 | 0 | 0 | 0 |
| matbench_mp_e_form | 11 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.0447692 | 0.0447692 | 0 | 0 | 0 |
| matbench_mp_gap | 8 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.219872 | 0.219872 | 0 | 0 | 0 |
| matbench_perovskites | 10 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.0907542 | 0.0907542 | 0 | 0 | 0 |
| matbench_dielectric | 4 | matbench_v0.1_coNGN | matbench_v0.1_automatminer_expressv2020 | mae | 0.314157 | 0.315029 | 0.00087203 | 0.0201047 | 0.0433745 |
| matbench_dielectric | 11 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | mae | 0.339066 | 0.340007 | 0.000941329 | 0.0155406 | 0.0605722 |
| matbench_expt_gap | 4 | matbench_v0.1_CrabNet | matbench_v0.1_modnet_v0.1.10 | mae | 0.346265 | 0.347015 | 0.000750008 | 0.0113737 | 0.0659425 |
| matbench_jdft2d | 8 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_CrabNet | mae | 45.4611 | 45.6104 | 0.14923 | 2.06735 | 0.0721843 |
| matbench_mp_is_metal | 6 | matbench_v0.1_modnet_v0.1.12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | rocauc | 0.903809 | 0.903168 | 0.000641083 | 0.00579286 | 0.110668 |
| matbench_phonons | 1 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_coNGN | mae | 28.7606 | 28.8874 | 0.126783 | 1.13602 | 0.111603 |
| matbench_dielectric | 6 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_Finder_v1.2_composition | mae | 0.319656 | 0.320366 | 0.000709045 | 0.00628733 | 0.112774 |
| matbench_jdft2d | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_cgcnnv2019 | mae | 49.0243 | 49.244 | 0.219754 | 1.93619 | 0.113498 |
| matbench_mp_gap | 2 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.16937 | 0.169684 | 0.000314041 | 0.00269319 | 0.116606 |
| matbench_perovskites | 2 | matbench_v0.1_alignn | matbench_v0.1_DeeperGATGNN | mae | 0.0287655 | 0.0288114 | 4.58128e-05 | 0.000388605 | 0.11789 |
| matbench_glass | 2 | matbench_v0.1_automatminer_expressv2020 | matbench_v0.1_rf | rocauc | 0.860672 | 0.858701 | 0.00197173 | 0.0121741 | 0.161961 |
| matbench_expt_gap | 2 | matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | matbench_v0.1_modnet_v0.1.12 | mae | 0.330975 | 0.332674 | 0.00169891 | 0.00985325 | 0.172421 |
| matbench_mp_e_form | 8 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.0337208 | 0.0339587 | 0.000237907 | 0.00131737 | 0.180593 |
| matbench_dielectric | 7 | matbench_v0.1_Finder_v1.2_composition | matbench_v0.1_CrabNet | mae | 0.320366 | 0.323352 | 0.00298632 | 0.0157631 | 0.18945 |
| matbench_mp_gap | 7 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_modnet_v0.1.10 | mae | 0.219283 | 0.219872 | 0.000589556 | 0.00294238 | 0.200367 |
| matbench_dielectric | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_alignn | mae | 0.340007 | 0.344918 | 0.00491146 | 0.0236748 | 0.207455 |
| matbench_steels | 5 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_automatminer_expressv2020 | mae | 96.2139 | 97.4929 | 1.279 | 6.08162 | 0.210305 |
| matbench_log_gvrh | 8 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_automatminer_expressv2020 | mae | 0.0871107 | 0.08741 | 0.000299287 | 0.00131458 | 0.227668 |
| matbench_expt_is_metal | 3 | matbench_v0.1_rf | matbench_v0.1_modnet_v0.1.10 | rocauc | 0.916659 | 0.916052 | 0.000607287 | 0.00255684 | 0.237515 |

## Smallest raw adjacent gaps

| Task | Rank | Better | Worse | Metric | Gap | Gap / SE |
|---|---:|---|---|---|---:|---:|
| matbench_expt_is_metal | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | rocauc | 0 | 0 |
| matbench_log_gvrh | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_log_kvrh | 3 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_mp_e_form | 11 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_mp_gap | 8 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_perovskites | 10 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_perovskites | 2 | matbench_v0.1_alignn | matbench_v0.1_DeeperGATGNN | mae | 4.58128e-05 | 0.11789 |
| matbench_perovskites | 3 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.000172379 | 0.416664 |
| matbench_mp_e_form | 8 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.000237907 | 0.180593 |
| matbench_mp_e_form | 3 | matbench_v0.1_alignn | matbench_v0.1_SchNet_kgcnn_v2.1.0 | mae | 0.000287615 | 0.909748 |
| matbench_log_gvrh | 8 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_automatminer_expressv2020 | mae | 0.000299287 | 0.227668 |
| matbench_mp_gap | 2 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.000314041 | 0.116606 |
| matbench_mp_e_form | 9 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_Finder_v1.2_structure | mae | 0.000360029 | 0.265289 |
| matbench_mp_is_metal | 4 | matbench_v0.1_automatminer_expressv2020 | matbench_v0.1_coNGN | rocauc | 0.000383175 | 0.347879 |
| matbench_log_gvrh | 6 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_SchNet_kgcnn_v2.1.0 | mae | 0.000394917 | 0.53175 |
| matbench_mp_is_metal | 2 | matbench_v0.1_alignn | matbench_v0.1_coGN | rocauc | 0.000395411 | 0.546968 |
| matbench_mp_e_form | 6 | matbench_v0.1_GN-OA | matbench_v0.1_MegNet_kgcnn_v2.1.0 | mae | 0.000431652 | 3.40465 |
| matbench_log_kvrh | 5 | matbench_v0.1_alignn | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | mae | 0.000446188 | 0.905221 |
| matbench_log_kvrh | 10 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_DeeperGATGNN | mae | 0.000535312 | 0.761792 |
| matbench_mp_gap | 7 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_modnet_v0.1.10 | mae | 0.000589556 | 0.200367 |
| matbench_expt_is_metal | 3 | matbench_v0.1_rf | matbench_v0.1_modnet_v0.1.10 | rocauc | 0.000607287 | 0.237515 |
| matbench_log_kvrh | 13 | matbench_v0.1_CrabNet | matbench_v0.1_Finder_v1.2_composition | mae | 0.00061045 | 0.593142 |
| matbench_mp_is_metal | 6 | matbench_v0.1_modnet_v0.1.12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | rocauc | 0.000641083 | 0.110668 |
| matbench_dielectric | 6 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_Finder_v1.2_composition | mae | 0.000709045 | 0.112774 |
| matbench_log_gvrh | 10 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.000716145 | 0.643009 |

## Interpretation

This is a leaderboard-resolution screen, not a formal significance test. It shows where adjacent point estimates are narrow relative to fold-to-fold metric variation. Exact ties and gaps below one fold-SE proxy should be treated as unresolved without a stronger paired uncertainty analysis.
