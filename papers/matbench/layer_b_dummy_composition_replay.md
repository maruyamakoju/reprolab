# Matbench v0.1 Dummy source replay

- Submission: `matbench_v0.1_dummy` / `Dummy`
- Tasks replayed: 4
- Folds replayed: 20
- Python environment: `env/matbench-tpot`
- scikit-learn version: `1.2.2`
- Audit NumPy seed: `0`
- Exact prediction+score folds: 10 / 20
- Regression exact folds: 10 / 10
- Classification exact folds: 0 / 10
- Max prediction delta / mismatch rate: 5.020e-01
- Max score delta: 4.487e-02

## Method

The replay mirrors the submitted notebook logic on a bounded low-cost task subset: `DummyRegressor(strategy="mean")` for regression and `DummyClassifier(strategy="stratified")` for classification. The notebook does not record a random seed for the stratified classifier, so this audit sets a NumPy seed only to make the replay deterministic.

## Fold comparison

| Task | Fold | Type | Test n | Prediction delta / mismatch rate | Primary stored | Primary replay | Primary delta | Max score delta |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| matbench_expt_gap | 0 | regression | 921 | 0 | 1.09646800468 | 1.09646800468 | 0 | 0 |
| matbench_expt_gap | 1 | regression | 921 | 0 | 1.19221192656 | 1.19221192656 | 0 | 0 |
| matbench_expt_gap | 2 | regression | 921 | 0 | 1.15268817052 | 1.15268817052 | 0 | 0 |
| matbench_expt_gap | 3 | regression | 921 | 0 | 1.1445202552 | 1.1445202552 | 0 | 0 |
| matbench_expt_gap | 4 | regression | 920 | 0 | 1.13174644762 | 1.13174644762 | 0 | 0 |
| matbench_expt_is_metal | 0 | classification | 985 | 0.489340101523 | 0.469965450992 | 0.502477798758 | 0.0325123477659 | 0.0377263494158 |
| matbench_expt_is_metal | 1 | classification | 984 | 0.502032520325 | 0.500074361728 | 0.514302239114 | 0.0142278773858 | 0.0142278773858 |
| matbench_expt_is_metal | 2 | classification | 984 | 0.485772357724 | 0.487812938941 | 0.491861521937 | 0.00404858299595 | 0.00406504065041 |
| matbench_expt_is_metal | 3 | classification | 984 | 0.475609756098 | 0.507167644386 | 0.521222011072 | 0.0140543666859 | 0.0142276422764 |
| matbench_expt_is_metal | 4 | classification | 984 | 0.5 | 0.49693877551 | 0.488742460547 | 0.00819631496323 | 0.016708086854 |
| matbench_glass | 0 | classification | 1136 | 0.397887323944 | 0.521244581041 | 0.496355973379 | 0.0248886076617 | 0.0264084507042 |
| matbench_glass | 1 | classification | 1136 | 0.426936619718 | 0.521747400218 | 0.486115034482 | 0.035632365736 | 0.035632365736 |
| matbench_glass | 2 | classification | 1136 | 0.406690140845 | 0.484759117599 | 0.515048794176 | 0.0302896765762 | 0.0302896765762 |
| matbench_glass | 3 | classification | 1136 | 0.414612676056 | 0.479860867862 | 0.524728534141 | 0.0448676662787 | 0.0448676662787 |
| matbench_glass | 4 | classification | 1136 | 0.399647887324 | 0.495058436251 | 0.500237285454 | 0.00517884920321 | 0.00517884920321 |
| matbench_steels | 0 | regression | 63 | 0 | 241.459074393 | 241.459074393 | 0 | 0 |
| matbench_steels | 1 | regression | 63 | 0 | 219.377031937 | 219.377031937 | 0 | 0 |
| matbench_steels | 2 | regression | 62 | 0 | 225.793225806 | 225.793225806 | 0 | 0 |
| matbench_steels | 3 | regression | 62 | 0 | 241.203522581 | 241.203522581 | 0 | 0 |
| matbench_steels | 4 | regression | 62 | 0 | 220.889793548 | 220.889793548 | 0 | 0 |

## Interpretation

The mean-regression dummy source path is prediction-identical for the checked regression folds. The stratified classification dummy source path is runnable but not prediction-identical under the audit seed, which is expected because the submitted notebook did not persist the RNG state or a classifier `random_state`.
