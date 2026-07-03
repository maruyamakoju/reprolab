
### 2026-07-03 07:29 UTC — paper003 clone Matbench candidate repo

```
$ git clone --depth 1 https://github.com/materialsproject/matbench vendor\matbench
```

- exit code: **0**  | duration: 20.4s  | raw log: `logs/cmd-20260703-072910.log`

output tail:
```
Cloning into 'vendor\matbench'...
```

### 2026-07-03 07:29 UTC — paper003 inspect Matbench result schema

```
$ .venv\Scripts\python.exe -c import gzip,json; from pathlib import Path; p=Path('vendor/matbench/benchmarks/matbench_v0.1_dummy/results.json.gz'); data=json.loads(gzip.open(p,'rt',encoding='utf-8').read()); print('top_keys', sorted(data)); print('benchmark', data.get('benchmark_name')); print('tasks', list(data['tasks'])[:5], 'n_tasks', len(data['tasks'])); task=next(iter(data['tasks'])); print('task', task); print('task_keys', sorted(data['tasks'][task])); fold=next(k for k in data['tasks'][task] if k.startswith('fold_')); print('fold', fold, sorted(data['tasks'][task][fold])); print('fold_scores', data['tasks'][task][fold].get('scores')); print('results_sample_keys', list(data['tasks'][task][fold].get('results', {}))[:5])
```

- exit code: **1**  | duration: 0.3s  | raw log: `logs/cmd-20260703-072957.log`

output tail:
```
top_keys ['@class', '@module', 'benchmark_name', 'datestamp', 'hash', 'tasks', 'user_metadata', 'version']
benchmark matbench_v0.1
tasks ['matbench_dielectric', 'matbench_expt_gap', 'matbench_expt_is_metal', 'matbench_glass', 'matbench_jdft2d'] n_tasks 13
task matbench_dielectric
task_keys ['@class', '@module', 'benchmark_name', 'dataset_name', 'results']
Traceback (most recent call last):
  File "<string>", line 1, in <module>
StopIteration
```

### 2026-07-03 07:30 UTC — paper003 inspect Matbench result schema corrected

```
$ .venv\Scripts\python.exe -c import gzip,json; from pathlib import Path; p=Path('vendor/matbench/benchmarks/matbench_v0.1_dummy/results.json.gz'); data=json.loads(gzip.open(p,'rt',encoding='utf-8').read()); task='matbench_dielectric'; t=data['tasks'][task]; print('task_keys', sorted(t)); print('result_folds', sorted(t['results'])[:5]); fold='fold_0'; f=t['results'][fold]; print('fold_keys', sorted(f)); print('scores', f['scores']); print('params', f.get('parameters')); print('data_keys', sorted(f['data'])); print('data_sample', list(f['data'].items())[:3])
```

- exit code: **0**  | duration: 0.3s  | raw log: `logs/cmd-20260703-073009.log`

output tail:
```
task_keys ['@class', '@module', 'benchmark_name', 'dataset_name', 'results']
result_folds ['fold_0', 'fold_1', 'fold_2', 'fold_3', 'fold_4']
fold_keys ['data', 'parameters', 'scores']
scores {'mae': 0.7025642979783651, 'mape': 0.3200531656619666, 'max_error': 14.950062733735118, 'rmse': 1.0677348073603554}
params {'constant_': [[2.4569770107667264]]}
data_keys ['mb-dielectric-0008', 'mb-dielectric-0010', 'mb-dielectric-0019', 'mb-dielectric-0025', 'mb-dielectric-0031', 'mb-dielectric-0036', 'mb-dielectric-0038', 'mb-dielectric-0040', 'mb-dielectric-0041', 'mb-dielectric-0051', 'mb-dielectric-0062', 'mb-dielectric-0071', 'mb-dielectric-0076', 'mb-dielectric-0077', 'mb-dielectric-0085', 'mb-dielectric-0086', 'mb-dielectric-0098', 'mb-dielectric-0107', 'mb-dielectric-0113', 'mb-dielectric-0117', 'mb-dielectric-0120', 'mb-dielectric-0126', 'mb-dielectric-0143', 'mb-dielectric-0147', 'mb-dielectric-0157', 'mb-dielectric-0158', 'mb-dielectric-0168', 'mb-dielectric-0171', 'mb-dielectric-0172', 'mb-dielectric-0185', 'mb-dielectric-0190', 'mb-dielectric-0191', 'mb-dielectric-0192', 'mb-dielectric-0197', 'mb-dielectric-0200', 'mb-dielectric-0202', 'mb-dielectric-0204', 'mb-dielectric-0209', 'mb-dielectric-0210', 'mb-dielectric-0216', 'mb-dielectric-0218', 'mb-dielectric-0225', 'mb-dielectric-0229', 'mb-dielectric-0233', 'mb-dielectric-0236', 'mb-dielectric-0238', 'mb-dielectric-0246', 'mb-dielectric-0253', 'mb-dielectric-0265', 'mb-dielectric-0267', 'mb-dielectric-0268', 'mb-dielectric-0269', 'mb-dielectric-0272', 'mb-dielectric-0276', 'mb-dielectric-0279', 'mb-dielectric-0281', 'mb-dielectric-0296', 'mb-dielectric-0300', 'mb-dielectric-0307', 'mb-dielectric-0309', 'mb-dielectric-0313', 'mb-dielectric-0331', 'mb-dielectric-0337', 'mb-dielectric-0340', 'mb-dielectric-0344', 'mb-dielectric-0347', 'mb-dielectric-0356', 'mb-dielectric-0370', 'mb-dielectric-0373', 'mb-dielectric-0375', 'mb-dielectric-0376', 'mb-dielectric-0380', 'mb-dielectric-0381', 'mb-dielectric-0383', 'mb-dielectric-0408', 'mb-dielectric-0409', 'mb-dielectric-0412', 'mb-dielectric-0418', 'mb-dielectric-0422', 'mb-dielectric-0426', 'mb-dielectric-0432', 'mb-dielectric-0460', 'mb-dielectric-0464', 'mb-dielectric-0471', 'mb-dielectric-0482', 'mb-dielectric-0487', 'mb-dielectric-0488', 'mb-dielectric-0517', 'mb-dielectric-0521', 'mb-dielectric-0523', 'mb-dielectric-0529', 'mb-dielectric-0530', 'mb-dielectric-0534', 'mb-dielectric-0535', 'mb-dielectric-0547', 'mb-dielectric-0552', 'mb-dielectric-0567', 'mb-dielectric-0569', 'mb-dielectric-0573', 'mb-dielectric-0588', 'mb-dielectric-0592', 'mb-dielectric-0594', 'mb-dielectric-0598', 'mb-dielectric-0612', 'mb-dielectric-0617', 'mb-dielectric-0628', 'mb-dielectric-0644', 'mb-dielectric-0648', 'mb-dielectric-0652', 'mb-dielectric-0661', 'mb-dielectric-0669', 'mb-dielectric-0672', 'mb-dielectric-0682', 'mb-dielectric-0686', 'mb-dielectric-0687', 'mb-dielectric-0694', 'mb-dielectric-0709', 'mb-dielectric-0710', 'mb-dielectric-0712', 'mb-dielectric-0716', 'mb-dielectric-0719', 'mb-dielectric-0724', 'mb-dielectric-0733', 'mb-dielectric-0743', 'mb-dielectric-0752', 'mb-dielectric-0754', 'mb-dielectric-0758', 'mb-dielectric-0759', 'mb-dielectric-0762', 'mb-dielectric-0766', 'mb-dielectric-0769', 'mb-dielectric-0773', 'mb-dielectric-0782', 'mb-dielectric-0794', 'mb-dielectric-0797', 'mb-dielectric-0799', 'mb-dielectric-0803', 'mb-dielectric-0808', 'mb-dielectric-0809', 'mb-dielectric-0815', 'mb-dielectric-0818', 'mb-dielectric-0833', 'mb-dielectric-0834', 'mb-dielectric-0835', 'mb-dielectric-0843', 'mb-dielectric-0844', 'mb-dielectric-0845', 'mb-dielectric-0850', 'mb-dielectric-0865', 'mb-dielectric-0874', 'mb-dielectric-0876', 'mb-dielectric-0884', 'mb-dielectric-0885', 'mb-dielectric-0890', 'mb-dielectric-0905', 'mb-dielectric-0908', 'mb-dielectric-0914', 'mb-dielectric-0915', 'mb-dielectric-0916', 'mb-dielectric-0919', 'mb-dielectric-0925', 'mb-dielectric-0928', 'mb-dielectric-0932', 'mb-dielectric-0942', 'mb-dielectric-0944', 'mb-dielectric-0948', 'mb-dielectric-0950', 'mb-dielectric-0955', 'mb-dielectric-0957', 'mb-dielectric-0958', 'mb-dielectric-0960', 'mb-dielectric-0961', 'mb-dielectric-0977', 'mb-dielectric-0979', 'mb-dielectric-0984', 'mb-dielectric-0991', 'mb-dielectric-0994', 'mb-dielectric-0999', 'mb-dielectric-1000', 'mb-dielectric-1012', 'mb-dielectric-1013', 'mb-dielectric-1015', 'mb-dielectric-1021', 'mb-dielectric-1029', 'mb-dielectric-1032', 'mb-dielectric-1033', 'mb-dielectric-1046', 'mb-dielectric-1048', 'mb-dielectric-1051', 'mb-dielectric-1056', 'mb-dielectric-1057', 'mb-dielectric-1059', 'mb-dielectric-1061', 'mb-dielectric-1065', 'mb-dielectric-1066', 'mb-dielectric-1082', 'mb-dielectric-1083', 'mb-dielectric-1091', 'mb-dielectric-1097', 'mb-dielectric-1109', 'mb-dielectric-1115', 'mb-dielectric-1117', 'mb-dielectric-1119', 'mb-dielectric-1123', 'mb-dielectric-1140', 'mb-dielectric-1141', 'mb-dielectric-1154', 'mb-dielectric-1171', 'mb-dielectric-1175', 'mb-dielectric-1178', 'mb-dielectric-1191', 'mb-dielectric-1192', 'mb-dielectric-1195', 'mb-dielectric-1197', 'mb-dielectric-1207', 'mb-dielectric-1214', 'mb-dielectric-1215', 'mb-dielectric-1220', 'mb-dielectric-1240', 'mb-dielectric-1249', 'mb-dielectric-1250', 'mb-dielectric-1262', 'mb-dielectric-1267', 'mb-dielectric-1269', 'mb-dielectric-1275', 'mb-dielectric-1276', 'mb-dielectric-1277', 'mb-dielectric-1282', 'mb-dielectric-1291', 'mb-dielectric-1304', 'mb-dielectric-1312', 'mb-dielectric-1315', 'mb-dielectric-1319', 'mb-dielectric-1321', 'mb-dielectric-1325', 'mb-dielectric-1331', 'mb-dielectric-1332', 'mb-dielectric-1337', 'mb-dielectric-1345', 'mb-dielectric-1352', 'mb-dielectric-1355', 'mb-dielectric-1357', 'mb-dielectric-1363', 'mb-dielectric-1369', 'mb-dielectric-1373', 'mb-dielectric-1374', 'mb-dielectric-1379', 'mb-dielectric-1380', 'mb-dielectric-1381', 'mb-dielectric-1382', 'mb-dielectric-1384', 'mb-dielectric-1389', 'mb-dielectric-1390', 'mb-dielectric-1394', 'mb-dielectric-1397', 'mb-dielectric-1398', 'mb-dielectric-1407', 'mb-dielectric-1408', 'mb-dielectric-1409', 'mb-dielectric-1419', 'mb-dielectric-1426', 'mb-dielectric-1430', 'mb-dielectric-1431', 'mb-dielectric-1433', 'mb-dielectric-1436', 'mb-dielectric-1438', 'mb-dielectric-1443', 'mb-dielectric-1452', 'mb-dielectric-1455', 'mb-dielectric-1463', 'mb-dielectric-1478', 'mb-dielectric-1484', 'mb-dielectric-1491', 'mb-dielectric-1499', 'mb-dielectric-1503', 'mb-dielectric-1511', 'mb-dielectric-1524', 'mb-dielectric-1527', 'mb-dielectric-1531', 'mb-dielectric-1539', 'mb-dielectric-1550', 'mb-dielectric-1567', 'mb-dielectric-1574', 'mb-dielectric-1578', 'mb-dielectric-1579', 'mb-dielectric-1584', 'mb-dielectric-1585', 'mb-dielectric-1598', 'mb-dielectric-1599', 'mb-dielectric-1608', 'mb-dielectric-1610', 'mb-dielectric-1620', 'mb-dielectric-1623', 'mb-dielectric-1641', 'mb-dielectric-1659', 'mb-dielectric-1660', 'mb-dielectric-1661', 'mb-dielectric-1663', 'mb-dielectric-1665', 'mb-dielectric-1671', 'mb-dielectric-1678', 'mb-dielectric-1682', 'mb-dielectric-1684', 'mb-dielectric-1686', 'mb-dielectric-1703', 'mb-dielectric-1705', 'mb-dielectric-1714', 'mb-dielectric-1723', 'mb-dielectric-1724', 'mb-dielectric-1726', 'mb-dielectric-1737', 'mb-dielectric-1738', 'mb-dielectric-1747', 'mb-dielectric-1750', 'mb-dielectric-1752', 'mb-dielectric-1755', 'mb-dielectric-1756', 'mb-dielectric-1764', 'mb-dielectric-1781', 'mb-dielectric-1787', 'mb-dielectric-1789', 'mb-dielectric-1803', 'mb-dielectric-1804', 'mb-dielectric-1809', 'mb-dielectric-1810', 'mb-dielectric-1829', 'mb-dielectric-1838', 'mb-dielectric-1848', 'mb-dielectric-1854', 'mb-dielectric-1859', 'mb-dielectric-1861', 'mb-dielectric-1864', 'mb-dielectric-1878', 'mb-dielectric-1880', 'mb-dielectric-1883', 'mb-dielectric-1885', 'mb-dielectric-1886', 'mb-dielectric-1888', 'mb-dielectric-1893', 'mb-dielectric-1894', 'mb-dielectric-1895', 'mb-dielectric-1900', 'mb-dielectric-1905', 'mb-dielectric-1909', 'mb-dielectric-1910', 'mb-dielectric-1911', 'mb-dielectric-1914', 'mb-dielectric-1923', 'mb-dielectric-1927', 'mb-dielectric-1932', 'mb-dielectric-1933', 'mb-dielectric-1939', 'mb-dielectric-1942', 'mb-dielectric-1943', 'mb-dielectric-1955', 'mb-dielectric-1964', 'mb-dielectric-1966', 'mb-dielectric-1967', 'mb-dielectric-1968', 'mb-dielectric-1971', 'mb-dielectric-1972', 'mb-dielectric-1976', 'mb-dielectric-1984', 'mb-dielectric-1995', 'mb-dielectric-1998', 'mb-dielectric-1999', 'mb-dielectric-2001', 'mb-dielectric-2005', 'mb-dielectric-2017', 'mb-dielectric-2020', 'mb-dielectric-2022', 'mb-dielectric-2023', 'mb-dielectric-2025', 'mb-dielectric-2039', 'mb-dielectric-2046', 'mb-dielectric-2056', 'mb-dielectric-2062', 'mb-dielectric-2068', 'mb-dielectric-2071', 'mb-dielectric-2072', 'mb-dielectric-2075', 'mb-dielectric-2076', 'mb-dielectric-2085', 'mb-dielectric-2094', 'mb-dielectric-2095', 'mb-dielectric-2100', 'mb-dielectric-2101', 'mb-dielectric-2106', 'mb-dielectric-2122', 'mb-dielectric-2128', 'mb-dielectric-2129', 'mb-dielectric-2132', 'mb-dielectric-2135', 'mb-dielectric-2137', 'mb-dielectric-2147', 'mb-dielectric-2151', 'mb-dielectric-2152', 'mb-dielectric-2158', 'mb-dielectric-2164', 'mb-dielectric-2167', 'mb-dielectric-2168', 'mb-dielectric-2173', 'mb-dielectric-2174', 'mb-dielectric-2185', 'mb-dielectric-2187', 'mb-dielectric-2189', 'mb-dielectric-2190', 'mb-dielectric-2196', 'mb-dielectric-2197', 'mb-dielectric-2203', 'mb-dielectric-2204', 'mb-dielectric-2207', 'mb-dielectric-2216', 'mb-dielectric-2221', 'mb-dielectric-2222', 'mb-dielectric-2225', 'mb-dielectric-2230', 'mb-dielectric-2236', 'mb-dielectric-2237', 'mb-dielectric-2240', 'mb-dielectric-2245', 'mb-dielectric-2248', 'mb-dielectric-2261', 'mb-dielectric-2268', 'mb-dielectric-2273', 'mb-dielectric-2280', 'mb-dielectric-2283', 'mb-dielectric-2284', 'mb-dielectric-2301', 'mb-dielectric-2302', 'mb-dielectric-2304', 'mb-dielectric-2313', 'mb-dielectric-2319', 'mb-dielectric-2321', 'mb-dielectric-2322', 'mb-dielectric-2328', 'mb-dielectric-2344', 'mb-dielectric-2355', 'mb-dielectric-2357', 'mb-dielectric-2364', 'mb-dielectric-2366', 'mb-dielectric-2368', 'mb-dielectric-2369', 'mb-dielectric-2372', 'mb-dielectric-2373', 'mb-dielectric-2380', 'mb-dielectric-2383', 'mb-dielectric-2387', 'mb-dielectric-2389', 'mb-dielectric-2392', 'mb-dielectric-2395', 'mb-dielectric-2397', 'mb-dielectric-2401', 'mb-dielectric-2404', 'mb-dielectric-2412', 'mb-dielectric-2415', 'mb-dielectric-2419', 'mb-dielectric-2423', 'mb-dielectric-2425', 'mb-dielectric-2434', 'mb-dielectric-2435', 'mb-dielectric-2437', 'mb-dielectric-2439', 'mb-dielectric-2449', 'mb-dielectric-2450', 'mb-dielectric-2454', 'mb-dielectric-2455', 'mb-dielectric-2466', 'mb-dielectric-2467', 'mb-dielectric-2470', 'mb-dielectric-2471', 'mb-dielectric-2473', 'mb-dielectric-2474', 'mb-dielectric-2479', 'mb-dielectric-2480', 'mb-dielectric-2482', 'mb-dielectric-2485', 'mb-dielectric-2486', 'mb-dielectric-2492', 'mb-dielectric-2495', 'mb-dielectric-2503', 'mb-dielectric-2506', 'mb-dielectric-2509', 'mb-dielectric-2518', 'mb-dielectric-2524', 'mb-dielectric-2528', 'mb-dielectric-2531', 'mb-dielectric-2532', 'mb-dielectric-2533', 'mb-dielectric-2535', 'mb-dielectric-2537', 'mb-dielectric-2552', 'mb-dielectric-2553', 'mb-dielectric-2554', 'mb-dielectric-2555', 'mb-dielectric-2556', 'mb-dielectric-2558', 'mb-dielectric-2562', 'mb-dielectric-2567', 'mb-dielectric-2571', 'mb-dielectric-2584', 'mb-dielectric-2586', 'mb-dielectric-2591', 'mb-dielectric-2592', 'mb-dielectric-2593', 'mb-dielectric-2595', 'mb-dielectric-2601', 'mb-dielectric-2606', 'mb-dielectric-2608', 'mb-dielectric-2624', 'mb-dielectric-2630', 'mb-dielectric-2637', 'mb-dielectric-2640', 'mb-dielectric-2641', 'mb-dielectric-2644', 'mb-dielectric-2651', 'mb-dielectric-2655', 'mb-dielectric-2658', 'mb-dielectric-2680', 'mb-dielectric-2681', 'mb-dielectric-2686', 'mb-dielectric-2691', 'mb-dielectric-2693', 'mb-dielectric-2696', 'mb-dielectric-2697', 'mb-dielectric-2702', 'mb-dielectric-2712', 'mb-dielectric-2722', 'mb-dielectric-2732', 'mb-dielectric-2733', 'mb-dielectric-2736', 'mb-dielectric-2743', 'mb-dielectric-2750', 'mb-dielectric-2751', 'mb-dielectric-2754', 'mb-dielectric-2755', 'mb-dielectric-2756', 'mb-dielectric-2758', 'mb-dielectric-2760', 'mb-dielectric-2768', 'mb-dielectric-2770', 'mb-dielectric-2776', 'mb-dielectric-2779', 'mb-dielectric-2786', 'mb-dielectric-2789', 'mb-dielectric-2794', 'mb-dielectric-2797', 'mb-dielectric-2806', 'mb-dielectric-2817', 'mb-dielectric-2818', 'mb-dielectric-2820', 'mb-dielectric-2823', 'mb-dielectric-2825', 'mb-dielectric-2826', 'mb-dielectric-2833', 'mb-dielectric-2834', 'mb-dielectric-2836', 'mb-dielectric-2839', 'mb-dielectric-2842', 'mb-dielectric-2844', 'mb-dielectric-2846', 'mb-dielectric-2860', 'mb-dielectric-2879', 'mb-dielectric-2882', 'mb-dielectric-2883', 'mb-dielectric-2885', 'mb-dielectric-2886', 'mb-dielectric-2892', 'mb-dielectric-2893', 'mb-dielectric-2894', 'mb-dielectric-2901', 'mb-dielectric-2902', 'mb-dielectric-2909', 'mb-dielectric-2913', 'mb-dielectric-2914', 'mb-dielectric-2922', 'mb-dielectric-2925', 'mb-dielectric-2927', 'mb-dielectric-2930', 'mb-dielectric-2941', 'mb-dielectric-2942', 'mb-dielectric-2952', 'mb-dielectric-2955', 'mb-dielectric-2958', 'mb-dielectric-2961', 'mb-dielectric-2968', 'mb-dielectric-2971', 'mb-dielectric-2985', 'mb-dielectric-2986', 'mb-dielectric-2989', 'mb-dielectric-2991', 'mb-dielectric-3001', 'mb-dielectric-3007', 'mb-dielectric-3008', 'mb-dielectric-3038', 'mb-dielectric-3039', 'mb-dielectric-3041', 'mb-dielectric-3056', 'mb-dielectric-3060', 'mb-dielectric-3067', 'mb-dielectric-3073', 'mb-dielectric-3074', 'mb-dielectric-3077', 'mb-dielectric-3079', 'mb-dielectric-3092', 'mb-dielectric-3095', 'mb-dielectric-3096', 'mb-dielectric-3099', 'mb-dielectric-3104', 'mb-dielectric-3107', 'mb-dielectric-3108', 'mb-dielectric-3115', 'mb-dielectric-3122', 'mb-dielectric-3126', 'mb-dielectric-3128', 'mb-dielectric-3132', 'mb-dielectric-3133', 'mb-dielectric-3134', 'mb-dielectric-3139', 'mb-dielectric-3141', 'mb-dielectric-3143', 'mb-dielectric-3146', 'mb-dielectric-3147', 'mb-dielectric-3155', 'mb-dielectric-3157', 'mb-dielectric-3163', 'mb-dielectric-3166', 'mb-dielectric-3176', 'mb-dielectric-3178', 'mb-dielectric-3186', 'mb-dielectric-3187', 'mb-dielectric-3209', 'mb-dielectric-3210', 'mb-dielectric-3213', 'mb-dielectric-3221', 'mb-dielectric-3230', 'mb-dielectric-3232', 'mb-dielectric-3242', 'mb-dielectric-3247', 'mb-dielectric-3254', 'mb-dielectric-3256', 'mb-dielectric-3261', 'mb-dielectric-3264', 'mb-dielectric-3266', 'mb-dielectric-3274', 'mb-dielectric-3284', 'mb-dielectric-3287', 'mb-dielectric-3288', 'mb-dielectric-3294', 'mb-dielectric-3296', 'mb-dielectric-3303', 'mb-dielectric-3313', 'mb-dielectric-3317', 'mb-dielectric-3318', 'mb-dielectric-3332', 'mb-dielectric-3333', 'mb-dielectric-3341', 'mb-dielectric-3347', 'mb-dielectric-3354', 'mb-dielectric-3363', 'mb-dielectric-3370', 'mb-dielectric-3375', 'mb-dielectric-3380', 'mb-dielectric-3389', 'mb-dielectric-3390', 'mb-dielectric-3404', 'mb-dielectric-3407', 'mb-dielectric-3416', 'mb-dielectric-3417', 'mb-dielectric-3418', 'mb-dielectric-3421', 'mb-dielectric-3433', 'mb-dielectric-3439', 'mb-dielectric-3440', 'mb-dielectric-3442', 'mb-dielectric-3444', 'mb-dielectric-3450', 'mb-dielectric-3452', 'mb-dielectric-3454', 'mb-dielectric-3470', 'mb-dielectric-3482', 'mb-dielectric-3486', 'mb-dielectric-3492', 'mb-dielectric-3493', 'mb-dielectric-3506', 'mb-dielectric-3507', 'mb-dielectric-3508', 'mb-dielectric-3509', 'mb-dielectric-3513', 'mb-dielectric-3514', 'mb-dielectric-3516', 'mb-dielectric-3518', 'mb-dielectric-3526', 'mb-dielectric-3528', 'mb-dielectric-3533', 'mb-dielectric-3541', 'mb-dielectric-3543', 'mb-dielectric-3545', 'mb-dielectric-3552', 'mb-dielectric-3554', 'mb-dielectric-3556', 'mb-dielectric-3567', 'mb-dielectric-3574', 'mb-dielectric-3579', 'mb-dielectric-3591', 'mb-dielectric-3594', 'mb-dielectric-3597', 'mb-dielectric-3611', 'mb-dielectric-3621', 'mb-dielectric-3636', 'mb-dielectric-3647', 'mb-dielectric-3648', 'mb-dielectric-3649', 'mb-dielectric-3650', 'mb-dielectric-3654', 'mb-dielectric-3656', 'mb-dielectric-3662', 'mb-dielectric-3664', 'mb-dielectric-3671', 'mb-dielectric-3673', 'mb-dielectric-3680', 'mb-dielectric-3684', 'mb-dielectric-3687', 'mb-dielectric-3688', 'mb-dielectric-3690', 'mb-dielectric-3694', 'mb-dielectric-3696', 'mb-dielectric-3697', 'mb-dielectric-3703', 'mb-dielectric-3707', 'mb-dielectric-3711', 'mb-dielectric-3716', 'mb-dielectric-3719', 'mb-dielectric-3720', 'mb-dielectric-3725', 'mb-dielectric-3742', 'mb-dielectric-3743', 'mb-dielectric-3745', 'mb-dielectric-3750', 'mb-dielectric-3757', 'mb-dielectric-3767', 'mb-dielectric-3771', 'mb-dielectric-3774', 'mb-dielectric-3775', 'mb-dielectric-3778', 'mb-dielectric-3786', 'mb-dielectric-3790', 'mb-dielectric-3791', 'mb-dielectric-3793', 'mb-dielectric-3795', 'mb-dielectric-3797', 'mb-dielectric-3799', 'mb-dielectric-3806', 'mb-dielectric-3807', 'mb-dielectric-3810', 'mb-dielectric-3812', 'mb-dielectric-3818', 'mb-dielectric-3820', 'mb-dielectric-3821', 'mb-dielectric-3831', 'mb-dielectric-3848', 'mb-dielectric-3852', 'mb-dielectric-3855', 'mb-dielectric-3863', 'mb-dielectric-3867', 'mb-dielectric-3868', 'mb-dielectric-3869', 'mb-dielectric-3870', 'mb-dielectric-3871', 'mb-dielectric-3876', 'mb-dielectric-3879', 'mb-dielectric-3881', 'mb-dielectric-3889', 'mb-dielectric-3897', 'mb-dielectric-3906', 'mb-dielectric-3908', 'mb-dielectric-3915', 'mb-dielectric-3917', 'mb-dielectric-3922', 'mb-dielectric-3929', 'mb-dielectric-3930', 'mb-dielectric-3933', 'mb-dielectric-3934', 'mb-dielectric-3941', 'mb-dielectric-3944', 'mb-dielectric-3963', 'mb-dielectric-3972', 'mb-dielectric-3982', 'mb-dielectric-3983', 'mb-dielectric-3985', 'mb-dielectric-3988', 'mb-dielectric-3989', 'mb-dielectric-3995', 'mb-dielectric-4005', 'mb-dielectric-4011', 'mb-dielectric-4014', 'mb-dielectric-4017', 'mb-dielectric-4026', 'mb-dielectric-4041', 'mb-dielectric-4042', 'mb-dielectric-4060', 'mb-dielectric-4062', 'mb-dielectric-4063', 'mb-dielectric-4073', 'mb-dielectric-4075', 'mb-dielectric-4076', 'mb-dielectric-4081', 'mb-dielectric-4087', 'mb-dielectric-4091', 'mb-dielectric-4101', 'mb-dielectric-4106', 'mb-dielectric-4109', 'mb-dielectric-4114', 'mb-dielectric-4118', 'mb-dielectric-4126', 'mb-dielectric-4133', 'mb-dielectric-4141', 'mb-dielectric-4154', 'mb-dielectric-4157', 'mb-dielectric-4161', 'mb-dielectric-4162', 'mb-dielectric-4163', 'mb-dielectric-4188', 'mb-dielectric-4195', 'mb-dielectric-4209', 'mb-dielectric-4212', 'mb-dielectric-4217', 'mb-dielectric-4219', 'mb-dielectric-4221', 'mb-dielectric-4228', 'mb-dielectric-4229', 'mb-dielectric-4230', 'mb-dielectric-4235', 'mb-dielectric-4238', 'mb-dielectric-4240', 'mb-dielectric-4246', 'mb-dielectric-4256', 'mb-dielectric-4262', 'mb-dielectric-4267', 'mb-dielectric-4270', 'mb-dielectric-4286', 'mb-dielectric-4295', 'mb-dielectric-4303', 'mb-dielectric-4308', 'mb-dielectric-4315', 'mb-dielectric-4318', 'mb-dielectric-4319', 'mb-dielectric-4324', 'mb-dielectric-4327', 'mb-dielectric-4336', 'mb-dielectric-4338', 'mb-dielectric-4340', 'mb-dielectric-4341', 'mb-dielectric-4343', 'mb-dielectric-4349', 'mb-dielectric-4353', 'mb-dielectric-4357', 'mb-dielectric-4358', 'mb-dielectric-4360', 'mb-dielectric-4361', 'mb-dielectric-4366', 'mb-dielectric-4367', 'mb-dielectric-4368', 'mb-dielectric-4372', 'mb-dielectric-4375', 'mb-dielectric-4376', 'mb-dielectric-4377', 'mb-dielectric-4380', 'mb-dielectric-4388', 'mb-dielectric-4390', 'mb-dielectric-4403', 'mb-dielectric-4405', 'mb-dielectric-4411', 'mb-dielectric-4416', 'mb-dielectric-4417', 'mb-dielectric-4424', 'mb-dielectric-4427', 'mb-dielectric-4433', 'mb-dielectric-4434', 'mb-dielectric-4437', 'mb-dielectric-4439', 'mb-dielectric-4442', 'mb-dielectric-4446', 'mb-dielectric-4448', 'mb-dielectric-4449', 'mb-dielectric-4450', 'mb-dielectric-4453', 'mb-dielectric-4455', 'mb-dielectric-4479', 'mb-dielectric-4485', 'mb-dielectric-4493', 'mb-dielectric-4509', 'mb-dielectric-4510', 'mb-dielectric-4512', 'mb-dielectric-4525', 'mb-dielectric-4531', 'mb-dielectric-4532', 'mb-dielectric-4540', 'mb-dielectric-4541', 'mb-dielectric-4549', 'mb-dielectric-4551', 'mb-dielectric-4555', 'mb-dielectric-4556', 'mb-dielectric-4565', 'mb-dielectric-4566', 'mb-dielectric-4570', 'mb-dielectric-4577', 'mb-dielectric-4578', 'mb-dielectric-4590', 'mb-dielectric-4591', 'mb-dielectric-4593', 'mb-dielectric-4595', 'mb-dielectric-4596', 'mb-dielectric-4604', 'mb-dielectric-4606', 'mb-dielectric-4607', 'mb-dielectric-4609', 'mb-dielectric-4610', 'mb-dielectric-4616', 'mb-dielectric-4620', 'mb-dielectric-4625', 'mb-dielectric-4626', 'mb-dielectric-4627', 'mb-dielectric-4632', 'mb-dielectric-4634', 'mb-dielectric-4635', 'mb-dielectric-4638', 'mb-dielectric-4641', 'mb-dielectric-4643', 'mb-dielectric-4644', 'mb-dielectric-4646', 'mb-dielectric-4652', 'mb-dielectric-4653', 'mb-dielectric-4655', 'mb-dielectric-4657', 'mb-dielectric-4664', 'mb-dielectric-4676', 'mb-dielectric-4679', 'mb-dielectric-4685', 'mb-dielectric-4711', 'mb-dielectric-4713', 'mb-dielectric-4725', 'mb-dielectric-4726', 'mb-dielectric-4729', 'mb-dielectric-4741', 'mb-dielectric-4744', 'mb-dielectric-4748', 'mb-dielectric-4749', 'mb-dielectric-4750', 'mb-dielectric-4753', 'mb-dielectric-4757', 'mb-dielectric-4760', 'mb-dielectric-4763']
data_sample [('mb-dielectric-0008', 2.4569770107667264), ('mb-dielectric-0010', 2.4569770107667264), ('mb-dielectric-0019', 2.4569770107667264)]
```

### 2026-07-03 07:31 UTC — paper003 Matbench import probe

```
$ .venv\Scripts\python.exe -c import sys; sys.path.insert(0, 'vendor/matbench'); import matbench; from matbench.bench import MatbenchBenchmark; print(matbench.__version__)
```

- exit code: **1**  | duration: 0.2s  | raw log: `logs/cmd-20260703-073133.log`

output tail:
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\Users\07013\Desktop\0702fable\reprolab\vendor/matbench\matbench\__init__.py", line 1, in <module>
    from matbench.bench import MatbenchBenchmark
  File "C:\Users\07013\Desktop\0702fable\reprolab\vendor/matbench\matbench\bench.py", line 20, in <module>
    from matbench.metadata import mbv01_metadata
  File "C:\Users\07013\Desktop\0702fable\reprolab\vendor/matbench\matbench\metadata.py", line 5, in <module>
    from matminer.datasets.utils import _load_dataset_dict
ModuleNotFoundError: No module named 'matminer'
```

### 2026-07-03 07:32 UTC — paper003 inspect rf result tasks and prediction types

```
$ env\jarvis\Scripts\python.exe -c import gzip,json; p='vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz'; d=json.load(gzip.open(p,'rt',encoding='utf-8')); print('tasks', list(d['tasks']));
for task in ['matbench_steels','matbench_expt_is_metal','matbench_glass','matbench_mp_is_metal']:
 f=d['tasks'][task]['results']['fold_0']; vals=list(f['data'].values())[:10]; print(task, type(vals[0]).__name__, vals[:5], f['scores'])
```

- exit code: **0**  | duration: 0.3s  | raw log: `logs/cmd-20260703-073227.log`

output tail:
```
tasks ['matbench_dielectric', 'matbench_expt_gap', 'matbench_expt_is_metal', 'matbench_glass', 'matbench_jdft2d', 'matbench_log_gvrh', 'matbench_log_kvrh', 'matbench_mp_e_form', 'matbench_mp_gap', 'matbench_mp_is_metal', 'matbench_perovskites', 'matbench_phonons', 'matbench_steels']
matbench_steels float [1676.480799999998, 2425.994400000005, 1251.199, 1322.6159999999993, 1701.7760000000103] {'mae': 114.63311746031721, 'mape': 0.07312546746289522, 'max_error': 1121.1276000000016, 'rmse': 196.35857062928474}
matbench_expt_is_metal bool [False, True, True, True, False] {'accuracy': 0.9248730964467005, 'balanced_accuracy': 0.9248291102187554, 'f1': 0.9235537190082644, 'rocauc': 0.9248291102187554}
matbench_glass bool [False, True, False, True, False] {'accuracy': 0.9198943661971831, 'balanced_accuracy': 0.8860069377747144, 'f1': 0.9448818897637795, 'rocauc': 0.8860069377747144}
matbench_mp_is_metal bool [False, False, True, True, True] {'accuracy': 0.9079771945530792, 'balanced_accuracy': 0.9025154931926253, 'f1': 0.890520769101407, 'rocauc': 0.9025154931926253}
```

### 2026-07-03 07:32 UTC — paper003 matminer small dataset load probe

```
$ env\jarvis\Scripts\python.exe -c from matminer.datasets import load_dataset; 
for name in ['matbench_steels','matbench_expt_is_metal']:
 df=load_dataset(name); print(name, df.shape, list(df.columns), df.head(2).to_dict('records'))
```

- exit code: **0**  | duration: 1.6s  | raw log: `logs/cmd-20260703-073227.log`

output tail:
```
Fetching matbench_steels.json.gz from https://ml.materialsproject.org/projects/matbench_steels.json.gz to C:\Users\07013\Desktop\0702fable\reprolab\env\jarvis\Lib\site-packages\matminer\datasets\matbench_steels.json.gz
matbench_steels (312, 2) ['composition', 'yield strength'] [{'composition': 'Fe0.620C0.000953Mn0.000521Si0.00102Cr0.000110Ni0.192Mo0.0176V0.000112Nb0.0000616Co0.146Al0.00318Ti0.0185', 'yield strength': 2411.5}, {'composition': 'Fe0.623C0.00854Mn0.000104Si0.000203Cr0.147Ni0.0000971Mo0.0179V0.00515N0.00163Nb0.0000614Co0.188W0.00729Al0.000845', 'yield strength': 1123.1}]
Fetching matbench_expt_is_metal.json.gz from https://ml.materialsproject.org/projects/matbench_expt_is_metal.json.gz to C:\Users\07013\Desktop\0702fable\reprolab\env\jarvis\Lib\site-packages\matminer\datasets\matbench_expt_is_metal.json.gz
matbench_expt_is_metal (4921, 2) ['composition', 'is_metal'] [{'composition': 'Ag(AuS)2', 'is_metal': True}, {'composition': 'Ag(W3Br7)2', 'is_metal': True}]

Fetching https://ml.materialsproject.org/projects/matbench_steels.json.gz in MB:   0%|          | 0.0/0.008836 [00:00<?, ?MB/s]
Fetching https://ml.materialsproject.org/projects/matbench_steels.json.gz in MB: 0.010239999999999999MB [00:00, 10.24MB/s]     

Fetching https://ml.materialsproject.org/projects/matbench_expt_is_metal.json.gz in MB:   0%|          | 0.0/0.034623 [00:00<?, ?MB/s]
Fetching https://ml.materialsproject.org/projects/matbench_expt_is_metal.json.gz in MB: 0.034816MB [00:00, 22.54MB/s]                 
```

### 2026-07-03 07:32 UTC — paper003 inspect rf result tasks and prediction types rerun after log-name fix

```
$ env\jarvis\Scripts\python.exe -c import gzip,json; p='vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz'; d=json.load(gzip.open(p,'rt',encoding='utf-8')); print('tasks', list(d['tasks']));
for task in ['matbench_steels','matbench_expt_is_metal','matbench_glass','matbench_mp_is_metal']:
 f=d['tasks'][task]['results']['fold_0']; vals=list(f['data'].values())[:10]; print(task, type(vals[0]).__name__, vals[:5], f['scores'])
```

- exit code: **0**  | duration: 0.3s  | raw log: `logs/cmd-20260703-073245-169530.log`

output tail:
```
tasks ['matbench_dielectric', 'matbench_expt_gap', 'matbench_expt_is_metal', 'matbench_glass', 'matbench_jdft2d', 'matbench_log_gvrh', 'matbench_log_kvrh', 'matbench_mp_e_form', 'matbench_mp_gap', 'matbench_mp_is_metal', 'matbench_perovskites', 'matbench_phonons', 'matbench_steels']
matbench_steels float [1676.480799999998, 2425.994400000005, 1251.199, 1322.6159999999993, 1701.7760000000103] {'mae': 114.63311746031721, 'mape': 0.07312546746289522, 'max_error': 1121.1276000000016, 'rmse': 196.35857062928474}
matbench_expt_is_metal bool [False, True, True, True, False] {'accuracy': 0.9248730964467005, 'balanced_accuracy': 0.9248291102187554, 'f1': 0.9235537190082644, 'rocauc': 0.9248291102187554}
matbench_glass bool [False, True, False, True, False] {'accuracy': 0.9198943661971831, 'balanced_accuracy': 0.8860069377747144, 'f1': 0.9448818897637795, 'rocauc': 0.8860069377747144}
matbench_mp_is_metal bool [False, False, True, True, True] {'accuracy': 0.9079771945530792, 'balanced_accuracy': 0.9025154931926253, 'f1': 0.890520769101407, 'rocauc': 0.9025154931926253}
```

### 2026-07-03 07:32 UTC — paper003 matminer small dataset load probe rerun after log-name fix

```
$ env\jarvis\Scripts\python.exe -c from matminer.datasets import load_dataset; 
for name in ['matbench_steels','matbench_expt_is_metal']:
 df=load_dataset(name); print(name, df.shape, list(df.columns), df.head(2).to_dict('records'))
```

- exit code: **0**  | duration: 0.5s  | raw log: `logs/cmd-20260703-073249-935210.log`

output tail:
```
matbench_steels (312, 2) ['composition', 'yield strength'] [{'composition': 'Fe0.620C0.000953Mn0.000521Si0.00102Cr0.000110Ni0.192Mo0.0176V0.000112Nb0.0000616Co0.146Al0.00318Ti0.0185', 'yield strength': 2411.5}, {'composition': 'Fe0.623C0.00854Mn0.000104Si0.000203Cr0.147Ni0.0000971Mo0.0179V0.00515N0.00163Nb0.0000614Co0.188W0.00729Al0.000845', 'yield strength': 1123.1}]
matbench_expt_is_metal (4921, 2) ['composition', 'is_metal'] [{'composition': 'Ag(AuS)2', 'is_metal': True}, {'composition': 'Ag(W3Br7)2', 'is_metal': True}]
```

### 2026-07-03 07:33 UTC — paper003 recompute Matbench RF scores for steels and expt_is_metal

```
$ env\jarvis\Scripts\python.exe scripts\matbench_score.py --results vendor\matbench\benchmarks\matbench_v0.1_rf\results.json.gz --tasks matbench_steels matbench_expt_is_metal --report papers\matbench\layer_a_score_recompute.md
```

- exit code: **0**  | duration: 1.6s  | raw log: `logs/cmd-20260703-073345-928436.log`

output tail:
```
{
  "folds_checked": 10,
  "max_abs_delta": 1.1102230246251565e-16,
  "report": "papers\\matbench\\layer_a_score_recompute.md",
  "results": "vendor\\matbench\\benchmarks\\matbench_v0.1_rf\\results.json.gz",
  "tasks": [
    "matbench_steels",
    "matbench_expt_is_metal"
  ]
}
```

### 2026-07-03 07:34 UTC — paper003 record Matbench upstream clone commit

```
$ git -C vendor\matbench rev-parse HEAD
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-073437-691964.log`

output tail:
```
936176db18ca4cd7b38cbd957c017a5bac770c6b
```

### 2026-07-03 07:35 UTC — paper003 verify scaffold docs and score script

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_score.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); report=Path('papers/matbench/layer_a_score_recompute.md').read_text(encoding='utf-8'); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); checks=[meta['layer_a_seed']['folds_checked']==10, abs(meta['layer_a_seed']['max_abs_stored_vs_recomputed_delta']-1.1102230246251565e-16)<1e-30, 'Max absolute stored-vs-recomputed score delta: 1.110e-16' in report, 'Matbench v0.1 Paper-003 Candidate' in summary, 'Paper-003 Candidate' in readme, 'scripts/run_command.py' in Path('papers/matbench/candidate_screen.md').read_text(encoding='utf-8')]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-073553-083947.log`

output tail:
```
{'checks': [True, True, True, True, True, True]}
```

### 2026-07-03 07:35 UTC — paper003 git diff whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-073557-807471.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'scripts/run_command.py', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 07:37 UTC — paper003 scan classification prediction value types

```
$ .venv\Scripts\python.exe scripts\matbench_classification_scan.py --report papers\matbench\classification_prediction_scan.md
```

- exit code: **0**  | duration: 4.4s  | raw log: `logs/cmd-20260703-073710-821082.log`

output tail:
```
{
  "all_bool": 16,
  "all_float": 11,
  "mixed": 0,
  "records": 27,
  "rocauc_differs_from_balacc": 0
}
```

### 2026-07-03 07:37 UTC — paper003 recompute MODNet 0.1.10 classification scores with probability AUC probe

```
$ env\jarvis\Scripts\python.exe scripts\matbench_score.py --results vendor\matbench\benchmarks\matbench_v0.1_modnet_v0.1.10\results.json.gz --tasks matbench_expt_is_metal matbench_glass --report papers\matbench\layer_a_modnet_0_1_10_probability_auc_probe.md
```

- exit code: **0**  | duration: 2.7s  | raw log: `logs/cmd-20260703-073735-074125.log`

output tail:
```
Fetching matbench_glass.json.gz from https://ml.materialsproject.org/projects/matbench_glass.json.gz to C:\Users\07013\Desktop\0702fable\reprolab\env\jarvis\Lib\site-packages\matminer\datasets\matbench_glass.json.gz
{
  "folds_checked": 10,
  "max_abs_delta": 1.1102230246251565e-16,
  "report": "papers\\matbench\\layer_a_modnet_0_1_10_probability_auc_probe.md",
  "results": "vendor\\matbench\\benchmarks\\matbench_v0.1_modnet_v0.1.10\\results.json.gz",
  "tasks": [
    "matbench_expt_is_metal",
    "matbench_glass"
  ]
}

Fetching https://ml.materialsproject.org/projects/matbench_glass.json.gz in MB:   0%|          | 0.0/0.039729 [00:00<?, ?MB/s]
Fetching https://ml.materialsproject.org/projects/matbench_glass.json.gz in MB: 0.040959999999999996MB [00:00, ?MB/s]
```

### 2026-07-03 07:37 UTC — paper003 recompute MODNet 0.1.12 classification scores with probability AUC probe

```
$ env\jarvis\Scripts\python.exe scripts\matbench_score.py --results vendor\matbench\benchmarks\matbench_v0.1_modnet_v0.1.12\results.json.gz --tasks matbench_expt_is_metal matbench_glass --report papers\matbench\layer_a_modnet_0_1_12_probability_auc_probe.md
```

- exit code: **0**  | duration: 2.3s  | raw log: `logs/cmd-20260703-073742-706595.log`

output tail:
```
{
  "folds_checked": 10,
  "max_abs_delta": 1.1102230246251565e-16,
  "report": "papers\\matbench\\layer_a_modnet_0_1_12_probability_auc_probe.md",
  "results": "vendor\\matbench\\benchmarks\\matbench_v0.1_modnet_v0.1.12\\results.json.gz",
  "tasks": [
    "matbench_expt_is_metal",
    "matbench_glass"
  ]
}
```

### 2026-07-03 07:38 UTC — paper003 summarize MODNet probability AUC gaps

```
$ .venv\Scripts\python.exe -c import re, statistics as st; from pathlib import Path
for path in ['papers/matbench/layer_a_modnet_0_1_10_probability_auc_probe.md','papers/matbench/layer_a_modnet_0_1_12_probability_auc_probe.md']:
 txt=Path(path).read_text(encoding='utf-8').splitlines(); rows=[]
 for line in txt:
  if line.startswith('| matbench_'):
   parts=[p.strip() for p in line.strip('|').split('|')]
   rows.append((parts[0], float(parts[5]), float(parts[6])))
 print(path)
 for task in sorted(set(r[0] for r in rows)):
  vals=[(stored, proba) for t, stored, proba in rows if t==task]
  print(task, {'stored_mean': st.mean(v[0] for v in vals), 'proba_mean': st.mean(v[1] for v in vals), 'gap_mean': st.mean(v[1]-v[0] for v in vals), 'gap_min': min(v[1]-v[0] for v in vals), 'gap_max': max(v[1]-v[0] for v in vals)})
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-073803-782167.log`

output tail:
```
papers/matbench/layer_a_modnet_0_1_10_probability_auc_probe.md
matbench_expt_is_metal {'stored_mean': 0.9160515032798, 'proba_mean': 0.9725462640508, 'gap_mean': 0.05649476077099998, 'gap_min': 0.04937457225999997, 'gap_max': 0.06093117408899995}
matbench_glass {'stored_mean': 0.810676338874, 'proba_mean': 0.9329484035962, 'gap_mean': 0.12227206472219998, 'gap_min': 0.09534732187499995, 'gap_max': 0.14420176043199995}
papers/matbench/layer_a_modnet_0_1_12_probability_auc_probe.md
matbench_expt_is_metal {'stored_mean': 0.9160515032798, 'proba_mean': 0.9725462640508, 'gap_mean': 0.05649476077099998, 'gap_min': 0.04937457225999997, 'gap_max': 0.06093117408899995}
matbench_glass {'stored_mean': 0.9603111829242, 'proba_mean': 0.9898761972560001, 'gap_mean': 0.02956501433180001, 'gap_min': 0.02086605424400001, 'gap_max': 0.033387570009000056}
```

### 2026-07-03 07:39 UTC — paper003 verify classification AUC probe docs

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_score.py', doraise=True); py_compile.compile('scripts/matbench_classification_scan.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); auc=Path('papers/matbench/classification_auc_probe.md').read_text(encoding='utf-8'); scan=Path('papers/matbench/classification_prediction_scan.md').read_text(encoding='utf-8'); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); checks=[meta['classification_auc_probe']['all_float_records']==11, meta['classification_auc_probe']['all_bool_records']==16, '0.122272' in auc, 'Submission/task records scanned: 27' in scan, 'classification_auc_probe.md' in summary]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-073912-032068.log`

output tail:
```
{'checks': [True, True, True, True, True]}
```

### 2026-07-03 07:39 UTC — paper003 classification AUC probe git diff whitespace check

```
$ git diff --check
```

- exit code: **2**  | duration: 0.0s  | raw log: `logs/cmd-20260703-073917-368693.log`

output tail:
```
papers/matbench/run_log.md:258: trailing whitespace.
+Fetching https://ml.materialsproject.org/projects/matbench_glass.json.gz in MB: 0.040959999999999996MB [00:00, ?MB/s]
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 07:39 UTC — paper003 classification AUC probe git diff whitespace check rerun

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-073939-713892.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/run_log.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 07:39 UTC — paper003 final classification AUC probe git diff whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-073959-113925.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/run_log.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 07:41 UTC — paper003 scan classification leaderboard displayed metrics

```
$ .venv\Scripts\python.exe scripts\matbench_leaderboard_metric_scan.py --report papers\matbench\classification_leaderboard_metric_scan.md
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-074135-020342.log`

output tail:
```
{
  "displayed_rocauc_differs_from_balacc": 0,
  "rows": 27,
  "tasks": 3
}
```

### 2026-07-03 07:42 UTC — paper003 verify classification leaderboard metric scan docs

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; [py_compile.compile(p, doraise=True) for p in ['scripts/matbench_score.py','scripts/matbench_classification_scan.py','scripts/matbench_leaderboard_metric_scan.py']]; meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); auc=Path('papers/matbench/classification_auc_probe.md').read_text(encoding='utf-8'); lb=Path('papers/matbench/classification_leaderboard_metric_scan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); checks=[meta['classification_auc_probe']['classification_leaderboard_rows']==27, meta['classification_auc_probe']['displayed_rocauc_rows_differing_from_balanced_accuracy']==0, 'Leaderboard display scan' in auc, 'Displayed algorithm rows scanned: 27' in lb, 'matbench_leaderboard_metric_scan.py' in readme]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-074211-109770.log`

output tail:
```
{'checks': [True, True, True, True, True]}
```

### 2026-07-03 07:42 UTC — paper003 classification leaderboard metric scan git diff whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-074215-092055.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/classification_auc_probe.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/run_log.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 07:43 UTC — paper003 verify upstream issue draft wiring

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import sys, yaml; meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); draft=Path('reports/paper-003_upstream_issue_draft.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); checks=[meta['classification_auc_probe']['upstream_issue_draft']=='reports/paper-003_upstream_issue_draft.md', 'Status: draft only; not posted.' in draft, 'Do not post until the user explicitly asks' in draft, '0.122272' in draft, 'paper-003_upstream_issue_draft.md' in readme, 'paper-003_upstream_issue_draft.md' in summary]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-074304-675654.log`

output tail:
```
{'checks': [True, True, True, True, True, True]}
```

### 2026-07-03 07:43 UTC — paper003 upstream issue draft git diff whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-074308-699446.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/run_log.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```
