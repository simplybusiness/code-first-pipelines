Code-First Pipelines
====================

A framework built on top of [Ploomber](https://ploomber.io/) that allows code-first definition of pipelines. 
**No YAML needed!**  

## Installation

To get the minimum code needed to use the pipelines, install it from PyPI:

```shell
pip install code-first-pipelines
```

## Usage

### Pipelines

```python
import pandas as pd
from sklearn import datasets
from cf_pipelines import Pipeline

iris_pipeline = Pipeline("My Cool Pipeline")

@iris_pipeline.step("Data ingestion")
def data_ingestion():
    d = datasets.load_iris()
    df = pd.DataFrame(d["data"])
    df.columns = d["feature_names"]
    df["target"] = d["target"]
    return {"raw_data.csv": df}

iris_pipeline.run()
```

See the [tutorial notebook](tutorials/Introduction%20to%20Pipelines.ipynb) for a more comprehensive example.

### ML Pipelines

```python
import pandas as pd
from sklearn import datasets
from cf_pipelines.ml import MLPipeline

iris_pipeline = MLPipeline("My Cool Pipeline")

@iris_pipeline.data_ingestion
def data_ingestion():
    d = datasets.load_iris()
    df = pd.DataFrame(d["data"])
    df.columns = d["feature_names"]
    df["target"] = d["target"]
    return {"raw_data.csv": df}

iris_pipeline.run()
```

See the [tutorial notebook](tutorials/Introduction%20to%20ML%20Pipelines.ipynb) for a more comprehensive example.

## Getting started with a template 

Once installed, you can create a new pipeline template by running:

```shell
pipelines new [pipeline name]
```
