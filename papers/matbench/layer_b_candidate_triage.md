# Matbench v0.1 Layer B candidate triage

This ranks public Matbench v0.1 submission artifacts for the next bounded source replay after the TPOT-Mat smoke. The score is a triage heuristic, not a claim about scientific quality.

- Submissions checked: 28
- High-priority candidates: 1
- Medium-priority candidates: 1
- Low-priority candidates: 24
- Already replayed: 1
- Positive-control candidates: 1

## Decision

`matbench_v0.1_RFLR` is the best next nontrivial bounded CPU replay target. It has one small `matbench_steels` task, simple scikit-learn/numpy/matbench requirements, a notebook source path, and seed/fit/predict signals. It has no saved fold-level model artifact, so prediction identity is not guaranteed, but it is the cleanest next source-execution probe.

`matbench_v0.1_dummy` is the best positive-control replay target if an exact source-path check is needed, but it has low novelty. `matbench_v0.1_lattice_xgboost` is a plausible later one-task baseline, but it targets the large `matbench_mp_e_form` task and is notebook-only.

## Next candidates

| Rank | Submission | Tasks | Score | Priority | Evidence | Recommendation |
|---:|---|---|---:|---|---|---|
| 1 | matbench_v0.1_RFLR | matbench_steels | 78 | high | one task, all low-cost tasks, notebook, seed signal, fit/predict path, CPU deps | Best next nontrivial CPU replay target: one steels task, simple deps, seed signal. |
| 2 | matbench_v0.1_dummy | matbench_dielectric, matbench_expt_gap, matbench_expt_is_metal, +10 more | 0 | positive-control candidate | 13 tasks, some low-cost tasks, large MP task, notebook, fit/predict path, CPU deps | Use as an exact-source positive control if a low-novelty replay is useful. |

## Full ranking

| Submission | Algorithm | Tasks | Source | Saved models | Score | Priority | Recommendation |
|---|---|---:|---|---|---:|---|---|
| matbench_v0.1_TPOT | TPOT-Mat | 1 | Matbench_steel_TPOT.ipynb, utils.py | tpot_best_pipeline.pkl | 93 | already replayed | Already used for the first bounded Layer B replay. |
| matbench_v0.1_RFLR | RF-Regex Steels | 1 | Matbench_Steels_RFLR.ipynb |  | 78 | high | Best next nontrivial CPU replay target: one steels task, simple deps, seed signal. |
| matbench_v0.1_Auto-sklearn | AutoML-Mat | 1 | environment.yml, notebook.ipynb |  | 46 | medium | Defer for now; Auto-sklearn environment conflicts make this a poor next smoke. |
| matbench_v0.1_lattice_xgboost | Lattice-XGBoost | 1 | notebook.ipynb |  | 28 | low | Bounded one-task baseline, but large MP e_form data and notebook-only source. |
| matbench_v0.1_gptchem | gptchem | 4 | run_experiments_classification.py, run_experiments_regression.py |  | 21 | low | Defer for now; source path depends on external repository or service state. |
| matbench_v0.1_Ax_10_90_CrabNet_v1.2.7 | Ax(10/90)+CrabNet v1.2.7 | 1 | gpei_submitit.py, notebook.ipynb, utils/extraordinary.py, utils/fractional.py, +6 more |  | 16 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_Ax_CrabNet_v1.2.1 | Ax+CrabNet v1.2.1 | 1 | notebook.ipynb |  | 16 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | Ax/SAASBO CrabNet v1.2.7 | 1 | notebook.ipynb, saas_submitit.py, utils/matbench.py, utils/metrics.py, +3 more |  | 16 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_darwin | Darwin | 4 | preprocessing.py, run.py |  | 8 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_rf | RF-SCM/Magpie | 13 | run.py |  | 7 | low | Useful reference runner, but all 13 tasks and unseeded RF make exact replay unlikely. |
| matbench_v0.1_CrabNet_v1.2.1 | CrabNet v1.2.1 | 1 | notebook.ipynb |  | 6 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_alignn | ALIGNN | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_automatminer_expressv2020 | AMMExpress v2020 | 13 | notebook.ipynb |  | 0 | low | Defer for now; source path depends on external repository or service state. |
| matbench_v0.1_cgcnnv2019 | CGCNN v2019 | 9 | run.py |  | 0 | low | Defer for now; source path depends on external repository or service state. |
| matbench_v0.1_coGN | coGN | 9 | preprocessing.py, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_coNGN | coNGN | 9 | preprocess_crystal.py, processing.py, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_CrabNet | CrabNet | 10 | notebook.ipynb |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_DeeperGATGNN | DeeperGATGNN | 8 | config.yml, deep_gatgnn.py, main.py, training.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | DimeNet++ (kgcnn v2.1.0) | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_dummy | Dummy | 13 | notebook.ipynb |  | 0 | positive-control candidate | Use as an exact-source positive control if a low-novelty replay is useful. |
| matbench_v0.1_Finder_v1.2_composition | Finder_v1.2 composition-only version | 8 | matbench_test.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_Finder_v1.2_structure | Finder_v1.2 structure-based version | 8 | matbench_test.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_GN-OA | GN-OA v1 | 1 | GN_OA.ipynb |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_matformer | Matformer | 1 | config.py, data.py, train.py, train_matbench.py, +1 more |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | MegNet (kgcnn v2.1.0) | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_modnet_v0.1.10 | MODNet (v0.1.10) | 13 | benchmarks.ipynb, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_modnet_v0.1.12 | MODNet (v0.1.12) | 13 | benchmarks.ipynb, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_SchNet_kgcnn_v2.1.0 | SchNet (kgcnn v2.1.0) | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |

## Scoring notes

The heuristic rewards one-task scope, low-cost tasks, direct source runners, notebooks, saved model artifacts, seed signals, fit/predict signals, and simple CPU dependencies. It penalizes large MP tasks, heavy neural stacks, external repository/service paths, many-task submissions, and missing source.
