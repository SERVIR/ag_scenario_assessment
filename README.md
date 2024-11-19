# ag_scenario_assessment
This repo collects a series of scripts and notebooks to do Agricultural management scenario assessment using the DSSAT model. This scenario assessment aims to evaluate the effectiveness of various crop management interventions, such as irrigation or nitrogen fertilization. The data and scripts explore one study case in selected districts of Zimbabwe. All the data used in the scripts is in the data folder. All the requirements for this project are in the requirements file. The [spatialDSSAT](https://github.com/daquinterop/spatialDSSAT) package is installed directly from the spatialDSSAT repository using this command:

```
pip install git+https://github.com/daquinterop/spatialDSSAT
```

## Contents of the repo
### Scripts
 - **dssat_run.py**: contains the `run_district` function that wraps the DSSAT run for the selected districts.
### Notebooks
 - **baseline_verification.ipynb**: explore the results of the previously generated validation runs. It generates a file that contains the model error metrics for each district.
 - **dssat_run_example.ipynb**: one example of how to simulate different management scenarios using the `run_district` function.
