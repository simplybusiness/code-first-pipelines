Code-First Pipelines
====================

A framework built on top of [Ploomber](https://ploomber.io/) that allows code-first definition of pipelines. 
**No YAML needed!**  

## Installation

TBA

## Usage

### ML Pipelines

```python
import pandas as pd
from cf_pipelines.ml import MLPipeline

my_pipeline = MLPipeline("My Cool Pipeline")

@my_pipeline.data_ingestion
def data_ingestion():
    input_data = pd.read_csv('input_data.csv')
    adult_data = input_data[input_data['age'] > 18]
    return {'adult_data.csv':adult_data}

my_pipeline.run()
```

See the [tutorial notebook](tutorials/Machine%20Learning%20Pipelines.ipynb) for a more comprehensive example.

## Getting started with a template 

Once installed, you can create a new pipeline template by running:

```shell
pipelines new [pipeline name]
```

## Development

### Extra dependencies

This project depends on Graphviz being installed in your system, follow the instructions [here](https://graphviz.org/download/).

We use [Poetry](https://python-poetry.org/) to manage this project's dependencies and virtual environment. 
Once cloned, just run `poetry install` to install them. Any time you want to work on this project, just run 
`poetry shell` to activate the virtual environment, and you will be ready.

We use some tools to enforce code formatting. To make sure your code meets these standards, run `make fmt` (this will 
modify the source files automatically) and then `make lint` to spot potential deficiencies.

Make sure you add tests for any new code contributed to this repo, and make sure you run all the tests with `make test`
before committing or opening a new pull request.
