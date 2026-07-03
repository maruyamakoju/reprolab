# Matbench v0.1 source artifact inventory

- Submission directories scanned: 28
- Direct `run.py` files: 11
- Notebook sources: 14
- Pickle/joblib model artifacts: 1

## Disposition counts

| Disposition | Count |
|---|---:|
| artifact-only or unclear source path | 1 |
| best bounded replay candidate | 1 |
| dependency-conflicting AutoML runner | 1 |
| external/heavy MODNet path | 2 |
| heavy neural dependency path | 12 |
| notebook-only source | 9 |
| source runner present; inspect manually | 2 |

## Submission inventory

| Submission | Algorithm | Tasks | Source artifacts | Model artifacts | Signals | Disposition |
|---|---|---:|---|---|---|---|
| matbench_v0.1_alignn | ALIGNN | 9 | run.py | config_example.json |  | heavy neural dependency path |
| matbench_v0.1_Auto-sklearn | AutoML-Mat | 1 | environment.yml, notebook.ipynb |  | seed, fit, predict, external_repo | dependency-conflicting AutoML runner |
| matbench_v0.1_automatminer_expressv2020 | AMMExpress v2020 | 13 | notebook.ipynb |  | fit, predict, external_repo | notebook-only source |
| matbench_v0.1_Ax_10_90_CrabNet_v1.2.7 | Ax(10/90)+CrabNet v1.2.7 | 1 | gpei_submitit.py, notebook.ipynb |  | pickle, external_repo | notebook-only source |
| matbench_v0.1_Ax_CrabNet_v1.2.1 | Ax+CrabNet v1.2.1 | 1 | notebook.ipynb |  | seed, predict, external_repo | notebook-only source |
| matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | Ax/SAASBO CrabNet v1.2.7 | 1 | notebook.ipynb, saas_submitit.py |  | pickle, external_repo | notebook-only source |
| matbench_v0.1_cgcnnv2019 | CGCNN v2019 | 9 | run.py |  |  | source runner present; inspect manually |
| matbench_v0.1_coGN | coGN | 9 | preprocessing.py, run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_coNGN | coNGN | 9 | preprocess_crystal.py, processing.py, run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_CrabNet | CrabNet | 10 | notebook.ipynb |  | seed | notebook-only source |
| matbench_v0.1_CrabNet_v1.2.1 | CrabNet v1.2.1 | 1 | notebook.ipynb |  | predict, external_repo | notebook-only source |
| matbench_v0.1_darwin | Darwin | 4 | preprocessing.py, run.py |  | external_repo | heavy neural dependency path |
| matbench_v0.1_DeeperGATGNN | DeeperGATGNN | 8 | config.yml, deep_gatgnn.py, main.py, training.py |  | seed, predict | heavy neural dependency path |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | DimeNet++ (kgcnn v2.1.0) | 9 | run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_dummy | Dummy | 13 | notebook.ipynb |  | fit, predict | notebook-only source |
| matbench_v0.1_Finder_v1.2_composition | Finder_v1.2 composition-only version | 8 | matbench_test.py |  | seed, external_repo | heavy neural dependency path |
| matbench_v0.1_Finder_v1.2_structure | Finder_v1.2 structure-based version | 8 | matbench_test.py |  | seed, external_repo | heavy neural dependency path |
| matbench_v0.1_GN-OA | GN-OA v1 | 1 | GN_OA.ipynb |  |  | heavy neural dependency path |
| matbench_v0.1_gptchem | gptchem | 4 | run_experiments_classification.py, run_experiments_regression.py |  | fit, predict, pickle, external_repo | artifact-only or unclear source path |
| matbench_v0.1_lattice_xgboost | Lattice-XGBoost | 1 | notebook.ipynb |  | predict, external_repo | notebook-only source |
| matbench_v0.1_matformer | Matformer | 1 | config.py, data.py, train.py, train_matbench.py, train_on_folder.py | config_example.json | seed, fit, pickle | heavy neural dependency path |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | MegNet (kgcnn v2.1.0) | 9 | run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_modnet_v0.1.10 | MODNet (v0.1.10) | 13 | benchmarks.ipynb, run.py |  | predict, pickle, external_repo | external/heavy MODNet path |
| matbench_v0.1_modnet_v0.1.12 | MODNet (v0.1.12) | 13 | benchmarks.ipynb, run.py |  | predict, pickle, external_repo | external/heavy MODNet path |
| matbench_v0.1_rf | RF-SCM/Magpie | 13 | run.py |  | fit, predict | source runner present; inspect manually |
| matbench_v0.1_RFLR | RF-Regex Steels | 1 | Matbench_Steels_RFLR.ipynb |  | seed, fit, predict | notebook-only source |
| matbench_v0.1_SchNet_kgcnn_v2.1.0 | SchNet (kgcnn v2.1.0) | 9 | run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_TPOT | TPOT-Mat | 1 | Matbench_steel_TPOT.ipynb, utils.py | tpot_best_pipeline.pkl | fit, predict, pickle | best bounded replay candidate |

## Interpretation

`matbench_v0.1_TPOT` stands out as the best bounded Layer B target because it has one small task, a notebook, a submitted helper, and a pickled pipeline artifact. Many other submissions are either notebook-only without saved fold-level models, full-run AutoML paths, or neural/external repositories with heavier dependencies.
