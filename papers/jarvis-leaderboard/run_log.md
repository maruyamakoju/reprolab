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
