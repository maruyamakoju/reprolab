# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 65
- Max absolute stored-vs-recomputed score delta: 1.776e-15

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_dielectric | 0 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 1 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 2 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 3 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 4 | 952 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 0 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 1 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 2 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 3 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 4 | 920 | float | 0.000e+00 |  |  |
| matbench_expt_is_metal | 0 | 985 | bool | 0.000e+00 | 0.924829110219 |  |
| matbench_expt_is_metal | 1 | 984 | bool | 0.000e+00 | 0.916632239941 |  |
| matbench_expt_is_metal | 2 | 984 | bool | 1.110e-16 | 0.909481120383 |  |
| matbench_expt_is_metal | 3 | 984 | bool | 1.110e-16 | 0.922746426506 |  |
| matbench_expt_is_metal | 4 | 984 | bool | 1.110e-16 | 0.909605056598 |  |
| matbench_glass | 0 | 1136 | bool | 0.000e+00 | 0.886006937775 |  |
| matbench_glass | 1 | 1136 | bool | 0.000e+00 | 0.840239093344 |  |
| matbench_glass | 2 | 1136 | bool | 1.110e-16 | 0.849521474334 |  |
| matbench_glass | 3 | 1136 | bool | 1.110e-16 | 0.852619367766 |  |
| matbench_glass | 4 | 1136 | bool | 0.000e+00 | 0.865116401698 |  |
| matbench_jdft2d | 0 | 128 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 1 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 2 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 3 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 4 | 127 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_mp_e_form | 0 | 26551 | float | 1.110e-16 |  |  |
| matbench_mp_e_form | 1 | 26551 | float | 0.000e+00 |  |  |
| matbench_mp_e_form | 2 | 26550 | float | 2.220e-16 |  |  |
| matbench_mp_e_form | 3 | 26550 | float | 1.110e-16 |  |  |
| matbench_mp_e_form | 4 | 26550 | float | 1.388e-17 |  |  |
| matbench_mp_gap | 0 | 21223 | float | 1.776e-15 |  |  |
| matbench_mp_gap | 1 | 21223 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 2 | 21223 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 3 | 21222 | float | 1.776e-15 |  |  |
| matbench_mp_gap | 4 | 21222 | float | 1.776e-15 |  |  |
| matbench_mp_is_metal | 0 | 21223 | bool | 0.000e+00 | 0.902515493193 |  |
| matbench_mp_is_metal | 1 | 21223 | bool | 0.000e+00 | 0.896777056389 |  |
| matbench_mp_is_metal | 2 | 21223 | bool | 0.000e+00 | 0.898733815358 |  |
| matbench_mp_is_metal | 3 | 21222 | bool | 1.110e-16 | 0.899366668787 |  |
| matbench_mp_is_metal | 4 | 21222 | bool | 0.000e+00 | 0.898371847031 |  |
| matbench_perovskites | 0 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 1 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 2 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 3 | 3785 | float | 0.000e+00 |  |  |
| matbench_perovskites | 4 | 3785 | float | 0.000e+00 |  |  |
| matbench_phonons | 0 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 1 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 2 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 3 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 4 | 253 | float | 0.000e+00 |  |  |
| matbench_steels | 0 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 1 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 2 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 3 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 4 | 62 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_dielectric

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.419578159259 | 0.52198700518 | 0.304162451401 | 0.0750037451263 |
| rmse | 1.85382481618 | 2.98323049778 | 0.785044337763 | 0.770049375991 |
| mape | 0.139968218264 | 0.188632999374 | 0.10574510663 | 0.0288667979365 |
| max_error | 34.8805599225 | 59.1201445981 | 14.5978573183 | 16.9979726853 |

### matbench_expt_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.446054992487 | 0.481156868621 | 0.434542420557 | 0.0176552424643 |
| rmse | 0.824300735345 | 0.943523224093 | 0.781867354239 | 0.0601326123053 |
| mape | 0.369492377556 | 0.43851001849 | 0.304356979438 | 0.0470475962382 |
| max_error | 6.046496 | 9.5428 | 4.71216 | 1.76997564717 |

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.916681936363 | 0.924873096447 | 0.909552845528 | 0.00641463134 |
| balanced_accuracy | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |
| f1 | 0.915855162513 | 0.923553719008 | 0.907580477674 | 0.00628063358071 |
| rocauc | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.895422535211 | 0.919894366197 | 0.884683098592 | 0.0130969823334 |
| balanced_accuracy | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |
| f1 | 0.927798088561 | 0.944881889764 | 0.919975565058 | 0.00908698827732 |
| rocauc | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |

### matbench_jdft2d

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 50.04399974 | 66.2421301222 | 42.7472945267 | 8.62712887611 |
| rmse | 112.265975486 | 159.638986052 | 72.7391490957 | 36.7066225573 |
| mape | 5.23911546788 | 23.7624894676 | 0.43823538542 | 9.26294774418 |
| max_error | 718.045733692 | 1538.60726856 | 295.743678511 | 453.647322018 |

### matbench_log_gvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.103998778594 | 0.106730986524 | 0.102382766772 | 0.00158833792656 |
| rmse | 0.154040121902 | 0.160123342295 | 0.149548591245 | 0.00365247845886 |
| mape | 0.0807614737326 | 0.0832065562181 | 0.0776724866644 | 0.0018807671835 |
| max_error | 1.15770278575 | 1.69423726872 | 0.904052794872 | 0.284521613255 |

### matbench_log_kvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.0819825484217 | 0.0862696399472 | 0.0783141445137 | 0.00271972565089 |
| rmse | 0.145360912566 | 0.150255516099 | 0.138320059166 | 0.00462831988118 |
| mape | 0.054592530708 | 0.0607661711246 | 0.050921152629 | 0.00348070098442 |
| max_error | 1.37315631231 | 1.76416363754 | 1.11891531674 | 0.231105610567 |

### matbench_mp_e_form

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.116450238243 | 0.117945584401 | 0.115797966884 | 0.000798121161187 |
| rmse | 0.241940247639 | 0.245915868682 | 0.237323137793 | 0.00335752922832 |
| mape | 0.679807113796 | 0.933100288396 | 0.506812454973 | 0.149239730501 |
| max_error | 4.11834095889 | 5.43820297872 | 2.93736137858 | 0.800820896985 |

### matbench_mp_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.345156150814 | 0.351217869437 | 0.341694434699 | 0.00332691657799 |
| rmse | 0.612501885046 | 0.627629509615 | 0.604668073226 | 0.00785109927504 |
| mape | 7.63147228584 | 11.9090490977 | 4.35469060744 | 2.68347073039 |
| max_error | 6.39584315417 | 7.0601086 | 5.92008807086 | 0.418177009281 |

### matbench_mp_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.905063466294 | 0.907977194553 | 0.902747019743 | 0.00167604998183 |
| balanced_accuracy | 0.899152976151 | 0.902515493193 | 0.896777056389 | 0.00188589705907 |
| f1 | 0.88664732113 | 0.890520769101 | 0.883862255233 | 0.00217933157754 |
| rocauc | 0.899152976151 | 0.902515493193 | 0.896777056389 | 0.00188589705907 |

### matbench_perovskites

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.235500182628 | 0.239509685601 | 0.229107455746 | 0.00344641995434 |
| rmse | 0.334613028166 | 0.339431954877 | 0.32924887781 | 0.00441961063639 |
| mape | 0.267833188583 | 0.288835902682 | 0.241102775512 | 0.016844798769 |
| max_error | 2.557712 | 2.88704 | 2.20832 | 0.218511273338 |

### matbench_phonons

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 67.6126142422 | 82.3862649649 | 58.6036107598 | 8.9899908374 |
| rmse | 146.276431864 | 172.801458959 | 122.15658115 | 21.4751689658 |
| mape | 0.118485135116 | 0.134769893668 | 0.104049045388 | 0.00979558791325 |
| max_error | 1270.68885897 | 2024.7301119 | 861.90049904 | 402.730658047 |

### matbench_steels

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 103.512486062 | 114.63311746 | 85.6694031746 | 11.0367786926 |
| rmse | 149.383944441 | 196.358570629 | 113.154922817 | 27.4893431478 |
| mape | 0.0744721297401 | 0.0807437889227 | 0.0653807405884 | 0.0056047478171 |
| max_error | 594.98156 | 1121.1276 | 362.663 | 278.700159881 |
