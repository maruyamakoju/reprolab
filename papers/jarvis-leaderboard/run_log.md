# Run Log - JARVIS-Leaderboard Paper-002 candidate

Commands below are appended by `scripts/run_command.py --paper jarvis-leaderboard`.

### 2026-07-03 05:52 UTC — verify paper002 scripts py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\run_command.py scripts\jarvis_score.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-055244.log`

output tail:
```

```

### 2026-07-03 05:52 UTC — paper002 layerA JARVIS formation energy seed models

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --out papers\jarvis-leaderboard\metric_check.md
```

- exit code: **0**  | duration: 0.2s  | raw log: `logs/cmd-20260703-055248.log`

output tail:
```
| kgcnn_coGN | kgcnn | 0.0271 | 0.02711760 | 5572 | exact | yes |
| alignn_model | ALIGNN | 0.0331 | 0.03311989 | 5572 | exact | yes |
| matminer_rf | UofT | 0.096 | 0.09595936 | 5572 | exact | yes |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target is a small Paper-002 candidate slice chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

If this preflight remains clean, extend to all submissions on this benchmark, then decide whether a Layer B model-execution smoke is feasible.

wrote papers\jarvis-leaderboard\metric_check.md
```

### 2026-07-03 05:53 UTC — paper002 sparse checkout all formation-energy submissions

```
$ git -C vendor\jarvis_leaderboard sparse-checkout add --skip-checks jarvis_leaderboard/contributions/kgcnn_coNGN/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/kgcnn_coNGN/metadata.json jarvis_leaderboard/contributions/cgcnn_model/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/cgcnn_model/metadata.json jarvis_leaderboard/contributions/potnet/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/potnet/metadata.json jarvis_leaderboard/contributions/kgcnn_schnet/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/kgcnn_schnet/metadata.json jarvis_leaderboard/contributions/matminer_lgbm/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/matminer_lgbm/metadata.json jarvis_leaderboard/contributions/kgcnn_megnet/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/kgcnn_megnet/metadata.json jarvis_leaderboard/contributions/kgcnn_dimenetPP/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/kgcnn_dimenetPP/metadata.json jarvis_leaderboard/contributions/cfid_chem/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/cfid_chem/metadata.json jarvis_leaderboard/contributions/matformer_256/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/matformer_256/metadata.json jarvis_leaderboard/contributions/cfid/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/cfid/metadata.json jarvis_leaderboard/contributions/matminer_xgboost/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/matminer_xgboost/metadata.json jarvis_leaderboard/contributions/kgcnn_cgcnn/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip jarvis_leaderboard/contributions/kgcnn_cgcnn/metadata.json
```

- exit code: **0**  | duration: 0.7s  | raw log: `logs/cmd-20260703-055355.log`

output tail:
```

```

### 2026-07-03 05:54 UTC — verify paper002 all-model option py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\run_command.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-055401.log`

output tail:
```

```

### 2026-07-03 05:54 UTC — paper002 layerA JARVIS formation energy all submissions

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --models all --out papers\jarvis-leaderboard\metric_check.md
```

- exit code: **0**  | duration: 0.4s  | raw log: `logs/cmd-20260703-055405.log`

output tail:
```
| matminer_rf | UofT | 0.096 | 0.09595936 | 5572 | exact | yes |
| matminer_xgboost | UofT | 0.0734 | 0.07339676 | 5572 | exact | yes |
| kgcnn_cgcnn | kgcnn | 0.0551 | 0.05508731 | 5572 | exact | yes |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target is a small Paper-002 candidate slice chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

If this preflight remains clean, extend to all submissions on this benchmark, then decide whether a Layer B model-execution smoke is feasible.

wrote papers\jarvis-leaderboard\metric_check.md
```

### 2026-07-03 05:54 UTC — verify paper002 report update py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\run_command.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-055444.log`

output tail:
```

```

### 2026-07-03 05:54 UTC — paper002 regenerate JARVIS formation energy all submissions report

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --models all --out papers\jarvis-leaderboard\metric_check.md
```

- exit code: **0**  | duration: 0.2s  | raw log: `logs/cmd-20260703-055449.log`

output tail:
```
| kgcnn_coGN to kgcnn_coNGN | 0.0020 | 0.00198041 |
| kgcnn_dimenetPP to kgcnn_cgcnn | 0.0023 | 0.00226462 |
| potnet to matformer_256 | 0.0029 | 0.00292089 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check.md
```

### 2026-07-03 05:55 UTC — paper002 verify JARVIS vendor pin and artifacts

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import subprocess,re; vendor=Path('vendor/jarvis_leaderboard'); commit=subprocess.check_output(['git','-C',str(vendor),'rev-parse','--short','HEAD'], text=True).strip(); doc=vendor/'docs/AI/SinglePropertyPrediction/dft_3d_formation_energy_peratom.md'; scores=re.findall(r'<tr><td><a [^>]*>([^<]+)</a></td><td>dft_3d</td><td>([^<]+)</td>', doc.read_text(encoding='utf-8')); csvs=list((vendor/'jarvis_leaderboard/contributions').glob('*/AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae.csv.zip')); print('commit', commit); print('official_rows', len(scores)); print('local_csvs', len(csvs)); print('models', ','.join(name for name,_ in scores))
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-055554.log`

output tail:
```
commit 57afc55
official_rows 15
local_csvs 15
models kgcnn_coNGN,kgcnn_coGN,cgcnn_model,potnet,kgcnn_schnet,matminer_lgbm,kgcnn_megnet,kgcnn_dimenetPP,cfid_chem,matformer_256,cfid,alignn_model,matminer_rf,matminer_xgboost,kgcnn_cgcnn
```

### 2026-07-03 05:56 UTC — verify paper002 final scripts py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\run_command.py scripts\jarvis_score.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-055613.log`

output tail:
```

```

### 2026-07-03 05:59 UTC — verify jarvis sparse helper py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\jarvis_sparse.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-055907.log`

output tail:
```

```

### 2026-07-03 05:59 UTC — paper002 sparse checkout five additional JARVIS tasks

```
$ .venv\Scripts\python.exe scripts\jarvis_sparse.py --vendor vendor\jarvis_leaderboard --benchmarks AI-SinglePropertyPrediction-ehull-dft_3d-test-mae AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae AI-SinglePropertyPrediction-slme-dft_3d-test-mae
```

- exit code: **0**  | duration: 1.3s  | raw log: `logs/cmd-20260703-055912.log`

output tail:
```
AI-SinglePropertyPrediction-ehull-dft_3d-test-mae: 28 paths (11 contribution CSVs)
AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae: 36 paths (15 contribution CSVs)
AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae: 34 paths (14 contribution CSVs)
AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae: 30 paths (12 contribution CSVs)
AI-SinglePropertyPrediction-slme-dft_3d-test-mae: 32 paths (13 contribution CSVs)
added 94 sparse-checkout paths
```

### 2026-07-03 05:59 UTC — paper002 layerA five additional JARVIS tasks

```
$ powershell -NoProfile -Command  = @('AI-SinglePropertyPrediction-ehull-dft_3d-test-mae','AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae','AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae','AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae','AI-SinglePropertyPrediction-slme-dft_3d-test-mae'); foreach ( in ) {  =  -replace '^AI-SinglePropertyPrediction-','' -replace '-dft_3d-test-mae$',''; & .\.venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark  --models all --out \ papers\jarvis-leaderboard\metric_check-.md\; if ( -ne 0) { exit  } }
```

- exit code: **1**  | duration: 0.8s  | raw log: `logs/cmd-20260703-055927.log`

output tail:
```
t-mae'); foreach ( in ) {  ...
+                                                
                  ~
Missing variable name after foreach.
At line:1 char:319
+ ... nglePropertyPrediction-slme-dft_3d-test-mae
'); foreach ( in ) {  =  - ...
+                                                
                 ~
Unexpected token ')' in expression or statement.
    + CategoryInfo          : ParserError: (:) [ 
   ], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : MissingVariableNam 
   eAfterForeach
 
```

### 2026-07-03 05:59 UTC — paper002 layerA JARVIS ehull

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark AI-SinglePropertyPrediction-ehull-dft_3d-test-mae --models all --out papers\jarvis-leaderboard\metric_check-ehull.md
```

- exit code: **0**  | duration: 0.3s  | raw log: `logs/cmd-20260703-055942.log`

output tail:
```
| kgcnn_megnet to kgcnn_cgcnn | 0.0021 | 0.00210703 |
| kgcnn_coNGN to potnet | 0.0037 | 0.00362190 |
| potnet to kgcnn_megnet | 0.0047 | 0.00475822 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-ehull.md
```

### 2026-07-03 05:59 UTC — paper002 layerA JARVIS optb88vdw bandgap

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae --models all --out papers\jarvis-leaderboard\metric_check-optb88vdw_bandgap.md
```

- exit code: **0**  | duration: 0.4s  | raw log: `logs/cmd-20260703-055947.log`

output tail:
```
| potnet to kgcnn_coNGN | 0.0021 | 0.00205851 |
| matminer_xgboost to matminer_rf | 0.0022 | 0.00213012 |
| kgcnn_coGN to potnet | 0.0027 | 0.00274677 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-optb88vdw_bandgap.md
```

### 2026-07-03 05:59 UTC — paper002 layerA JARVIS optb88vdw total energy

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae --models all --out papers\jarvis-leaderboard\metric_check-optb88vdw_total_energy.md
```

- exit code: **0**  | duration: 0.4s  | raw log: `logs/cmd-20260703-055952.log`

output tail:
```
| kgcnn_schnet to kgcnn_megnet | 0.0019 | 0.00190516 |
| matminer_lgbm to matminer_rf | 0.0035 | 0.00343703 |
| potnet to alignn_model | 0.0046 | 0.00455005 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-optb88vdw_total_energy.md
```

### 2026-07-03 06:00 UTC — paper002 layerA JARVIS bulk modulus

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae --models all --out papers\jarvis-leaderboard\metric_check-bulk_modulus_kv.md
```

- exit code: **0**  | duration: 0.3s  | raw log: `logs/cmd-20260703-060001.log`

output tail:
```
| kgcnn_coNGN to kgcnn_coGN | 0.2898 | 0.28984601 |
| kgcnn_schnet to kgcnn_cgcnn | 0.3043 | 0.30436306 |
| alignn_model to kgcnn_schnet | 0.3117 | 0.31163507 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-bulk_modulus_kv.md
```

### 2026-07-03 06:00 UTC — paper002 layerA JARVIS slme

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark AI-SinglePropertyPrediction-slme-dft_3d-test-mae --models all --out papers\jarvis-leaderboard\metric_check-slme.md
```

- exit code: **0**  | duration: 0.3s  | raw log: `logs/cmd-20260703-060006.log`

output tail:
```
| kgcnn_cgcnn to kgcnn_megnet | 0.0475 | 0.04741627 |
| kgcnn_megnet to matminer_rf | 0.0621 | 0.06209388 |
| kgcnn_coGN to alignn_model | 0.0700 | 0.06997936 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-slme.md
```

### 2026-07-03 06:00 UTC — paper002 regenerate six JARVIS metric reports after target fix

```
$ .venv\Scripts\python.exe -c import subprocess,sys; benches=['AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae','AI-SinglePropertyPrediction-ehull-dft_3d-test-mae','AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae','AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae','AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae','AI-SinglePropertyPrediction-slme-dft_3d-test-mae']; outs=['metric_check.md','metric_check-ehull.md','metric_check-optb88vdw_bandgap.md','metric_check-optb88vdw_total_energy.md','metric_check-bulk_modulus_kv.md','metric_check-slme.md']; [subprocess.run([sys.executable,'scripts/jarvis_score.py','--vendor','vendor/jarvis_leaderboard','--benchmark',b,'--models','all','--out','papers/jarvis-leaderboard/'+o], check=True) for b,o in zip(benches,outs)]
```

- exit code: **0**  | duration: 1.2s  | raw log: `logs/cmd-20260703-060030.log`

output tail:
```
| kgcnn_cgcnn to kgcnn_megnet | 0.0475 | 0.04741627 |
| kgcnn_megnet to matminer_rf | 0.0621 | 0.06209388 |
| kgcnn_coGN to alignn_model | 0.0700 | 0.06997936 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-slme.md
```

### 2026-07-03 06:00 UTC — verify jarvis scripts after multi-task run

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\jarvis_sparse.py scripts\run_command.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-060035.log`

output tail:
```

```

### 2026-07-03 06:01 UTC — verify paper002 six-task summary

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import re; files=sorted(Path('papers/jarvis-leaderboard').glob('metric_check*.md')); texts=[p.read_text(encoding='utf-8') for p in files]; counts=[int(re.search(r'Models scored: (\\d+)', t).group(1)) for t in texts]; bad=[str(p) for p,t in zip(files,texts) if '| no |' in t or 'missing=' in t or 'extra=' in t]; targets=[re.search(r'^Target: (.*)', t, re.M).group(1) for t in texts]; print('files', len(files)); print('counts', counts, 'total', sum(counts)); print('bad', bad); print('targets', targets); raise SystemExit(0 if len(files)==6 and sum(counts)==79 and not bad else 1)
```

- exit code: **1**  | duration: 0.1s  | raw log: `logs/cmd-20260703-060125.log`

output tail:
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<string>", line 1, in <listcomp>
AttributeError: 'NoneType' object has no attribute 'group'
```

### 2026-07-03 06:01 UTC — verify paper002 six-task summary after regex fix

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import re; files=sorted(Path('papers/jarvis-leaderboard').glob('metric_check*.md')); texts=[p.read_text(encoding='utf-8') for p in files]; counts=[int(re.search('Models scored: ([0-9]+)', t).group(1)) for t in texts]; bad=[str(p) for p,t in zip(files,texts) if '| no |' in t or 'missing=' in t or 'extra=' in t]; targets=[re.search('^Target: (.*)', t, re.M).group(1) for t in texts]; print('files', len(files)); print('counts', counts, 'total', sum(counts)); print('bad', bad); print('targets', targets); raise SystemExit(0 if len(files)==6 and sum(counts)==79 and not bad else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-060137.log`

output tail:
```
files 6
counts [12, 11, 14, 14, 13, 15] total 79
bad []
targets ['`AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae`', '`AI-SinglePropertyPrediction-ehull-dft_3d-test-mae`', '`AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae`', '`AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae`', '`AI-SinglePropertyPrediction-slme-dft_3d-test-mae`', '`AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae`']
```
