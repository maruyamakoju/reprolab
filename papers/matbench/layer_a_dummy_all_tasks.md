# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_dummy/results.json.gz`
- Fold scores checked: 65
- Max absolute stored-vs-recomputed score delta: 3.553e-15

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
| matbench_expt_is_metal | 0 | 985 | bool | 5.551e-17 | 0.469965450992 |  |
| matbench_expt_is_metal | 1 | 984 | bool | 0.000e+00 | 0.500074361728 |  |
| matbench_expt_is_metal | 2 | 984 | bool | 0.000e+00 | 0.487812938941 |  |
| matbench_expt_is_metal | 3 | 984 | bool | 0.000e+00 | 0.507167644386 |  |
| matbench_expt_is_metal | 4 | 984 | bool | 0.000e+00 | 0.49693877551 |  |
| matbench_glass | 0 | 1136 | bool | 0.000e+00 | 0.521244581041 |  |
| matbench_glass | 1 | 1136 | bool | 0.000e+00 | 0.521747400218 |  |
| matbench_glass | 2 | 1136 | bool | 1.110e-16 | 0.484759117599 |  |
| matbench_glass | 3 | 1136 | bool | 0.000e+00 | 0.479860867862 |  |
| matbench_glass | 4 | 1136 | bool | 0.000e+00 | 0.495058436251 |  |
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
| matbench_mp_e_form | 0 | 26551 | float | 3.553e-15 |  |  |
| matbench_mp_e_form | 1 | 26551 | float | 8.882e-16 |  |  |
| matbench_mp_e_form | 2 | 26550 | float | 0.000e+00 |  |  |
| matbench_mp_e_form | 3 | 26550 | float | 1.776e-15 |  |  |
| matbench_mp_e_form | 4 | 26550 | float | 2.220e-16 |  |  |
| matbench_mp_gap | 0 | 21223 | float | 1.776e-15 |  |  |
| matbench_mp_gap | 1 | 21223 | float | 3.553e-15 |  |  |
| matbench_mp_gap | 2 | 21223 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 3 | 21222 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 4 | 21222 | float | 2.220e-16 |  |  |
| matbench_mp_is_metal | 0 | 21223 | bool | 0.000e+00 | 0.506886095257 |  |
| matbench_mp_is_metal | 1 | 21223 | bool | 0.000e+00 | 0.494419221071 |  |
| matbench_mp_is_metal | 2 | 21223 | bool | 5.551e-17 | 0.498590270053 |  |
| matbench_mp_is_metal | 3 | 21222 | bool | 5.551e-17 | 0.50323734241 |  |
| matbench_mp_is_metal | 4 | 21222 | bool | 5.551e-17 | 0.502950061688 |  |
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
| mae | 0.80881997604 | 0.921817134881 | 0.702564297978 | 0.0717835125652 |
| rmse | 1.97276439959 | 3.10548965166 | 1.06773480736 | 0.726270709807 |
| mape | 0.319714785196 | 0.326616109687 | 0.314152052154 | 0.00453389033877 |
| max_error | 35.3994799869 | 59.6652611154 | 14.9500627337 | 17.9221496905 |

### matbench_expt_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 1.14352696092 | 1.19221192656 | 1.09646800468 | 0.0310111790489 |
| rmse | 1.44375982344 | 1.52680793386 | 1.3396579641 | 0.07074457681 |
| mape | 0.951601279953 | 1.24184930189 | 0.780170403994 | 0.169159721419 |
| max_error | 8.93004949746 | 10.7354493619 | 7.01188433342 | 1.23283288667 |

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.492384136024 | 0.507113821138 | 0.470050761421 | 0.0127716285884 |
| balanced_accuracy | 0.492391834312 | 0.507167644386 | 0.469965450992 | 0.0128213058361 |
| f1 | 0.491344921998 | 0.51256281407 | 0.453974895397 | 0.0207164926849 |
| rocauc | 0.492391834312 | 0.507167644386 | 0.469965450992 | 0.0128213058361 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.590669014085 | 0.612676056338 | 0.573063380282 | 0.0164685624418 |
| balanced_accuracy | 0.500534080594 | 0.521747400218 | 0.479860867862 | 0.0178053004541 |
| f1 | 0.712669719722 | 0.730392156863 | 0.700061842919 | 0.0125196238713 |
| rocauc | 0.500534080594 | 0.521747400218 | 0.479860867862 | 0.0178053004541 |

### matbench_jdft2d

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 67.2850873958 | 83.1220028779 | 53.1447467433 | 10.1832326615 |
| rmse | 126.844613359 | 192.236461159 | 74.1059643166 | 45.2193370998 |
| mape | 7.8079477369 | 35.3098249284 | 0.79210307142 | 13.7515312089 |
| max_error | 827.476377735 | 1491.79929416 | 468.041237726 | 385.901595872 |

### matbench_log_gvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.293147728528 | 0.296893245401 | 0.287489096428 | 0.00309088260967 |
| rmse | 0.371590544033 | 0.374890372437 | 0.364594619641 | 0.00379960401816 |
| mape | 0.233303472103 | 0.236753399418 | 0.225144441871 | 0.00422138007666 |
| max_error | 1.55363851107 | 1.55523707332 | 1.55239936687 | 0.00102394167409 |

### matbench_log_kvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.289693942024 | 0.295295712664 | 0.283276966769 | 0.00429747595087 |
| rmse | 0.369280680266 | 0.377400150458 | 0.363406251279 | 0.00589772165866 |
| mape | 0.187715572834 | 0.19264256072 | 0.182488864206 | 0.00348128655996 |
| max_error | 1.88044586043 | 1.88222304717 | 1.87899627074 | 0.0010767375786 |

### matbench_mp_e_form

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 1.00592689696 | 1.01107559823 | 1.00239527876 | 0.00298062807204 |
| rmse | 1.16313008776 | 1.16750266496 | 1.15966709918 | 0.00322549492437 |
| mape | 9.9487032688 | 11.6408738141 | 7.28677669784 | 1.71343664278 |
| max_error | 3.89700288851 | 3.90963195498 | 3.87819929834 | 0.0109045417018 |

### matbench_mp_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 1.32715612132 | 1.33479749605 | 1.31988057023 | 0.00596803481226 |
| rmse | 1.59893509043 | 1.61182033281 | 1.58633655116 | 0.0108240191848 |
| mape | 15.5847966914 | 19.3774275113 | 12.1281805816 | 2.70223814416 |
| max_error | 7.75845333957 | 8.50918423154 | 7.10789517022 | 0.49632018836 |

### matbench_mp_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.509918708023 | 0.515808321161 | 0.503227630401 | 0.00438899647352 |
| balanced_accuracy | 0.501216598096 | 0.506886095257 | 0.494419221071 | 0.0042972883326 |
| f1 | 0.435332826842 | 0.440548780488 | 0.42766407904 | 0.00433704294907 |
| rocauc | 0.501216598096 | 0.506886095257 | 0.494419221071 | 0.0042972883326 |

### matbench_perovskites

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.565998636192 | 0.574237337498 | 0.561199645022 | 0.00476994826584 |
| rmse | 0.742436343233 | 0.761797387026 | 0.734215871229 | 0.0102276667648 |
| mape | 0.758264985415 | 0.804586721598 | 0.705803135105 | 0.0333563178526 |
| max_error | 3.47706803685 | 3.68732796196 | 3.31226918505 | 0.126433463808 |

### matbench_phonons

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 323.98222624 | 348.257637178 | 299.120899653 | 17.7268997573 |
| rmse | 492.15330732 | 545.477181807 | 439.316559745 | 44.5175589932 |
| mape | 0.892570224044 | 1.02675700404 | 0.79769445702 | 0.0809879835419 |
| max_error | 2760.79467567 | 3062.34498517 | 1970.08835251 | 417.15805845 |

### matbench_steels

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 229.744529653 | 241.459074393 | 219.377031937 | 9.69580568939 |
| rmse | 301.221148667 | 343.934626844 | 287.68027737 | 21.4550756918 |
| mape | 0.158816036383 | 0.164724706551 | 0.155028132877 | 0.00335870996462 |
| max_error | 1032.32451791 | 1088.0568 | 941.064257028 | 59.3578666672 |
