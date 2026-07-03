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

### 2026-07-03 06:41 UTC — paper002 sparse checkout baseline run scripts

```
$ git -C vendor\jarvis_leaderboard sparse-checkout add --skip-checks jarvis_leaderboard/contributions/matminer_rf/run.py jarvis_leaderboard/contributions/matminer_rf/run.bash jarvis_leaderboard/contributions/matminer_xgboost/run.py jarvis_leaderboard/contributions/matminer_xgboost/run.bash jarvis_leaderboard/contributions/cfid/run.py jarvis_leaderboard/contributions/cfid/run.sh jarvis_leaderboard/contributions/cfid/zipit.py jarvis_leaderboard/contributions/cfid_chem/run.py jarvis_leaderboard/contributions/cfid_chem/run_chem.py
```

- exit code: **0**  | duration: 0.6s  | raw log: `logs/cmd-20260703-064123.log`

output tail:
```

```

### 2026-07-03 06:42 UTC — verify jarvis_score mae acc support py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\jarvis_sparse.py scripts\run_command.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064217.log`

output tail:
```

```

### 2026-07-03 06:42 UTC — verify existing six JARVIS MAE reports after acc support

```
$ .venv\Scripts\python.exe -c import subprocess,sys; benches=['AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae','AI-SinglePropertyPrediction-ehull-dft_3d-test-mae','AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae','AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae','AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae','AI-SinglePropertyPrediction-slme-dft_3d-test-mae']; outs=['metric_check.md','metric_check-ehull.md','metric_check-optb88vdw_bandgap.md','metric_check-optb88vdw_total_energy.md','metric_check-bulk_modulus_kv.md','metric_check-slme.md']; [subprocess.run([sys.executable,'scripts/jarvis_score.py','--vendor','vendor/jarvis_leaderboard','--benchmark',b,'--models','all','--out','papers/jarvis-leaderboard/'+o], check=True) for b,o in zip(benches,outs)]
```

- exit code: **0**  | duration: 1.2s  | raw log: `logs/cmd-20260703-064224.log`

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

### 2026-07-03 06:42 UTC — paper002 sparse checkout JARVIS classification tasks

```
$ .venv\Scripts\python.exe scripts\jarvis_sparse.py --vendor vendor\jarvis_leaderboard --benchmarks AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc AI-SinglePropertyClass-mbj_bandgap-dft_3d-test-acc AI-SinglePropertyClass-n_powerfact-dft_3d-test-acc AI-SinglePropertyClass-optb88vdw_bandgap-dft_3d-test-acc AI-SinglePropertyClass-p_Seebeck-dft_3d-test-acc AI-SinglePropertyClass-slme-dft_3d-test-acc AI-SinglePropertyClass-spillage-dft_3d-test-acc
```

- exit code: **0**  | duration: 1.1s  | raw log: `logs/cmd-20260703-064233.log`

output tail:
```
AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc: 12 paths (3 contribution CSVs)
AI-SinglePropertyClass-mbj_bandgap-dft_3d-test-acc: 12 paths (3 contribution CSVs)
AI-SinglePropertyClass-n_powerfact-dft_3d-test-acc: 12 paths (3 contribution CSVs)
AI-SinglePropertyClass-optb88vdw_bandgap-dft_3d-test-acc: 12 paths (3 contribution CSVs)
AI-SinglePropertyClass-p_Seebeck-dft_3d-test-acc: 12 paths (3 contribution CSVs)
AI-SinglePropertyClass-slme-dft_3d-test-acc: 12 paths (3 contribution CSVs)
AI-SinglePropertyClass-spillage-dft_3d-test-acc: 12 paths (3 contribution CSVs)
added 42 sparse-checkout paths
```

### 2026-07-03 06:42 UTC — paper002 layerA JARVIS classification tasks

```
$ .venv\Scripts\python.exe -c import subprocess,sys; benches=['AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc','AI-SinglePropertyClass-mbj_bandgap-dft_3d-test-acc','AI-SinglePropertyClass-n_powerfact-dft_3d-test-acc','AI-SinglePropertyClass-optb88vdw_bandgap-dft_3d-test-acc','AI-SinglePropertyClass-p_Seebeck-dft_3d-test-acc','AI-SinglePropertyClass-slme-dft_3d-test-acc','AI-SinglePropertyClass-spillage-dft_3d-test-acc']; [subprocess.run([sys.executable,'scripts/jarvis_score.py','--vendor','vendor/jarvis_leaderboard','--benchmark',b,'--models','all','--out','papers/jarvis-leaderboard/metric_check-'+b.split('-')[2]+'.md'], check=True) for b in benches]
```

- exit code: **1**  | duration: 0.3s  | raw log: `logs/cmd-20260703-064240.log`

output tail:
```
  File "C:\Users\07013\Desktop\0702fable\reprolab\scripts\jarvis_score.py", line 194, in main
    result = score_model(root, model, args.benchmark, truth, bench.metric)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\scripts\jarvis_score.py", line 126, in score_model
    rows = load_predictions(root, model, bench_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\scripts\jarvis_score.py", line 79, in load_predictions
    raise ValueError(f"expected {expected_name} inside {rel}, found {csv_name}")
ValueError: expected AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc.csv inside contributions\matminer_rf\AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc.csv.zip, found AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-mae.csv
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<string>", line 1, in <listcomp>
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['C:\\Users\\07013\\Desktop\\0702fable\\reprolab\\.venv\\Scripts\\python.exe', 'scripts/jarvis_score.py', '--vendor', 'vendor/jarvis_leaderboard', '--benchmark', 'AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc', '--models', 'all', '--out', 'papers/jarvis-leaderboard/metric_check-magmom_oszicar.md']' returned non-zero exit status 1.
```

### 2026-07-03 06:43 UTC — verify jarvis classification zip-name tolerance py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\jarvis_sparse.py scripts\run_command.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064302.log`

output tail:
```

```

### 2026-07-03 06:43 UTC — paper002 layerA JARVIS classification tasks after zip-name tolerance

```
$ .venv\Scripts\python.exe -c import subprocess,sys; benches=['AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc','AI-SinglePropertyClass-mbj_bandgap-dft_3d-test-acc','AI-SinglePropertyClass-n_powerfact-dft_3d-test-acc','AI-SinglePropertyClass-optb88vdw_bandgap-dft_3d-test-acc','AI-SinglePropertyClass-p_Seebeck-dft_3d-test-acc','AI-SinglePropertyClass-slme-dft_3d-test-acc','AI-SinglePropertyClass-spillage-dft_3d-test-acc']; [subprocess.run([sys.executable,'scripts/jarvis_score.py','--vendor','vendor/jarvis_leaderboard','--benchmark',b,'--models','all','--out','papers/jarvis-leaderboard/metric_check-class-'+b.split('-')[2]+'.md'], check=True) for b in benches]
```

- exit code: **0**  | duration: 1.3s  | raw log: `logs/cmd-20260703-064308.log`

output tail:
```
|---|---:|---:|
| matminer_rf to matminer_xgboost | 0.0053 | 0.00527704 |
| alignn_model to matminer_rf | 0.0176 | 0.01759015 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-class-spillage.md
```

### 2026-07-03 06:43 UTC — paper002 verify classification reports and zip inner names

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import re, zipfile; reports=sorted(Path('papers/jarvis-leaderboard').glob('metric_check-class-*.md')); texts=[p.read_text(encoding='utf-8') for p in reports]; counts=[int(re.search('Models scored: ([0-9]+)', t).group(1)) for t in texts]; bad=[str(p) for p,t in zip(reports,texts) if '| no |' in t or 'missing=' in t or 'extra=' in t]; vendor=Path('vendor/jarvis_leaderboard/jarvis_leaderboard/contributions'); zips=sorted(vendor.glob('*/AI-SinglePropertyClass-*-dft_3d-test-acc.csv.zip')); mismatches=[]; [mismatches.append((str(p), zipfile.ZipFile(p).namelist()[0])) for p in zips if zipfile.ZipFile(p).namelist()[0] != p.name[:-4]]; print('classification_reports', len(reports)); print('counts', counts, 'total', sum(counts)); print('bad', bad); print('class_csv_zips', len(zips), 'inner_name_mismatches', len(mismatches)); print('example_mismatch', mismatches[0] if mismatches else None); raise SystemExit(0 if len(reports)==7 and sum(counts)==21 and not bad else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064328.log`

output tail:
```
classification_reports 7
counts [3, 3, 3, 3, 3, 3, 3] total 21
bad []
class_csv_zips 21 inner_name_mismatches 14
example_mismatch ('vendor\\jarvis_leaderboard\\jarvis_leaderboard\\contributions\\matminer_rf\\AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc.csv.zip', 'AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-mae.csv')
```

### 2026-07-03 06:44 UTC — verify paper002 regression plus classification summary

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import re; files=sorted(Path('papers/jarvis-leaderboard').glob('metric_check*.md')); texts=[p.read_text(encoding='utf-8') for p in files]; counts=[int(re.search('Models scored: ([0-9]+)', t).group(1)) for t in texts]; bad=[str(p) for p,t in zip(files,texts) if '| no |' in t or 'missing=' in t or 'extra=' in t]; summary=Path('papers/jarvis-leaderboard/summary.md').read_text(encoding='utf-8'); print('files', len(files)); print('counts', counts, 'total', sum(counts)); print('bad', bad); print('summary_has_100', '100 checked submissions' in summary); raise SystemExit(0 if len(files)==13 and sum(counts)==100 and not bad and '100 checked submissions' in summary else 1)
```

- exit code: **0**  | duration: 0.2s  | raw log: `logs/cmd-20260703-064404.log`

output tail:
```
files 13
counts [12, 3, 3, 3, 3, 3, 3, 3, 11, 14, 14, 13, 15] total 100
bad []
summary_has_100 True
```

### 2026-07-03 06:44 UTC — verify paper002 summary tables after classification update

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import re; summary=Path('papers/jarvis-leaderboard/summary.md').read_text(encoding='utf-8'); files=sorted(Path('papers/jarvis-leaderboard').glob('metric_check*.md')); counts=[int(re.search('Models scored: ([0-9]+)', p.read_text(encoding='utf-8')).group(1)) for p in files]; bad=[str(p) for p in files if '| no |' in p.read_text(encoding='utf-8') or 'missing=' in p.read_text(encoding='utf-8') or 'extra=' in p.read_text(encoding='utf-8')]; print('files', len(files), 'total', sum(counts), 'bad', bad); print('summary_tables_ok', '|---|---:|---:|---:|---|' in summary); raise SystemExit(0 if len(files)==13 and sum(counts)==100 and not bad and '|---|---:|---:|---:|---|' in summary else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064425.log`

output tail:
```
files 13 total 100 bad []
summary_tables_ok True
```

### 2026-07-03 06:45 UTC — verify jarvis multimae support py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\jarvis_sparse.py scripts\run_command.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064500.log`

output tail:
```

```

### 2026-07-03 06:45 UTC — paper002 sparse checkout JARVIS spectra task

```
$ .venv\Scripts\python.exe scripts\jarvis_sparse.py --vendor vendor\jarvis_leaderboard --benchmarks AI-Spectra-ph_dos-edos_pdos-test-multimae
```

- exit code: **0**  | duration: 1.3s  | raw log: `logs/cmd-20260703-064504.log`

output tail:
```
AI-Spectra-ph_dos-edos_pdos-test-multimae: 8 paths (1 contribution CSVs)
added 8 sparse-checkout paths
```

### 2026-07-03 06:45 UTC — paper002 layerA JARVIS spectra multimae

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark AI-Spectra-ph_dos-edos_pdos-test-multimae --models all --out papers\jarvis-leaderboard\metric_check-spectra-ph_dos.md
```

- exit code: **1**  | duration: 0.3s  | raw log: `logs/cmd-20260703-064510.log`

output tail:
```
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.05772635693310998 | 0.00000000 | 1424 | exact | no |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-spectra-ph_dos.md
failures: alignn_model: official 0.05772635693310998, reproduced 0.00000000
```

### 2026-07-03 06:45 UTC — inspect JARVIS spectra CSV target prediction columns

```
$ .venv\Scripts\python.exe -c import zipfile,csv,json; from pathlib import Path; root=Path('vendor/jarvis_leaderboard/jarvis_leaderboard'); pred=root/'contributions/alignn_model/AI-Spectra-ph_dos-edos_pdos-test-multimae.csv.zip'; z=zipfile.ZipFile(pred); rows=list(csv.DictReader(z.read(z.namelist()[0]).decode().splitlines())); r=rows[0]; vec=lambda s:[float(x) for x in s.split(';') if x]; truth=json.loads(zipfile.ZipFile(root/'benchmarks/AI/Spectra/edos_pdos_ph_dos.json.zip').read('edos_pdos_ph_dos.json'))['test']; print('cols', list(r)); print('id', r['id']); print('target_eq_prediction', r['target']==r['prediction']); print('row_target_pred_mae', sum(abs(a-b) for a,b in zip(vec(r['target']),vec(r['prediction'])))/len(vec(r['target']))); print('json_eq_target', truth[r['id']]==r['target']); print('json_eq_prediction', truth[r['id']]==r['prediction'])
```

- exit code: **0**  | duration: 0.2s  | raw log: `logs/cmd-20260703-064540.log`

output tail:
```
cols ['id', 'target', 'prediction']
id JVASP-10558
target_eq_prediction False
row_target_pred_mae 0.03450392009709056
json_eq_target False
json_eq_prediction False
```

### 2026-07-03 06:46 UTC — inspect spectra json prediction numeric diff

```
$ .venv\Scripts\python.exe -c import zipfile,csv,json; from pathlib import Path; root=Path('vendor/jarvis_leaderboard/jarvis_leaderboard'); pred=root/'contributions/alignn_model/AI-Spectra-ph_dos-edos_pdos-test-multimae.csv.zip'; z=zipfile.ZipFile(pred); rows=list(csv.DictReader(z.read(z.namelist()[0]).decode().splitlines())); r=rows[0]; vec=lambda s:[float(x) for x in s.split(';') if x]; truth=json.loads(zipfile.ZipFile(root/'benchmarks/AI/Spectra/edos_pdos_ph_dos.json.zip').read('edos_pdos_ph_dos.json'))['test']; j=vec(truth[r['id']]); p=vec(r['prediction']); t=vec(r['target']); print('len', len(j), len(p), len(t)); print('json_pred_mae', sum(abs(a-b) for a,b in zip(j,p))/len(j)); print('json_target_mae', sum(abs(a-b) for a,b in zip(j,t))/len(j)); print('target_pred_mae', sum(abs(a-b) for a,b in zip(t,p))/len(t))
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064602.log`

output tail:
```
len 66 66 66
json_pred_mae 0.034503920015128316
json_target_mae 2.7136197334255363e-09
target_pred_mae 0.03450392009709056
```

### 2026-07-03 06:46 UTC — verify jarvis multimae score aggregation py_compile

```
$ .venv\Scripts\python.exe -m py_compile scripts\jarvis_score.py scripts\jarvis_sparse.py scripts\run_command.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064624.log`

output tail:
```

```

### 2026-07-03 06:46 UTC — paper002 layerA JARVIS spectra multimae after aggregation fix

```
$ .venv\Scripts\python.exe scripts\jarvis_score.py --vendor vendor\jarvis_leaderboard --benchmark AI-Spectra-ph_dos-edos_pdos-test-multimae --models all --out papers\jarvis-leaderboard\metric_check-spectra-ph_dos.md
```

- exit code: **0**  | duration: 0.2s  | raw log: `logs/cmd-20260703-064629.log`

output tail:
```
| model | team | official MULTIMAE | reproduced MULTIMAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.05772635693310998 | 0.05772636 | 1424 | exact | yes |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.

wrote papers\jarvis-leaderboard\metric_check-spectra-ph_dos.md
```

### 2026-07-03 06:47 UTC — verify paper002 spectra plus scalar summary

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import re; files=sorted(Path('papers/jarvis-leaderboard').glob('metric_check*.md')); texts=[p.read_text(encoding='utf-8') for p in files]; counts=[int(re.search('Models scored: ([0-9]+)', t).group(1)) for t in texts]; bad=[str(p) for p,t in zip(files,texts) if '| no |' in t or 'missing=' in t or 'extra=' in t]; summary=Path('papers/jarvis-leaderboard/summary.md').read_text(encoding='utf-8'); meta=Path('papers/jarvis-leaderboard/metadata.yaml').read_text(encoding='utf-8'); print('files', len(files)); print('total', sum(counts)); print('bad', bad); print('summary_has_101', '101 checked submissions' in summary); print('metadata_has_101', 'total_submissions: 101' in meta); raise SystemExit(0 if len(files)==14 and sum(counts)==101 and not bad and '101 checked submissions' in summary and 'total_submissions: 101' in meta else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064702.log`

output tail:
```
files 14
total 101
bad []
summary_has_101 True
metadata_has_101 True
```

### 2026-07-03 06:47 UTC — verify paper002 final spectra summary counts

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import re; files=sorted(Path('papers/jarvis-leaderboard').glob('metric_check*.md')); texts=[p.read_text(encoding='utf-8') for p in files]; counts=[int(re.search('Models scored: ([0-9]+)', t).group(1)) for t in texts]; bad=[str(p) for p,t in zip(files,texts) if '| no |' in t or 'missing=' in t or 'extra=' in t]; summary=Path('papers/jarvis-leaderboard/summary.md').read_text(encoding='utf-8'); meta=Path('papers/jarvis-leaderboard/metadata.yaml').read_text(encoding='utf-8'); print('files', len(files)); print('total', sum(counts)); print('bad', bad); print('metadata_has_14', 'total_benchmarks: 14' in meta); raise SystemExit(0 if len(files)==14 and sum(counts)==101 and not bad and '101 checked submissions' in summary and 'total_benchmarks: 14' in meta else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-064722.log`

output tail:
```
files 14
total 101
bad []
metadata_has_14 True
```
