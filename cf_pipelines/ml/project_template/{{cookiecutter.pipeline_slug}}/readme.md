{{cookiecutter.pipeline_name}}
===

{{cookiecutter.project_description}}

## Install dependencies

The file `requirements.txt` contains the functional dependencies for the project, while `requirements-dev.txt` contains
the development dependencies. Install them directly or using the package manager of your choice.

## Running the pipeline

To run the pipeline locally, execute:

```shell
python {{cookiecutter.pipeline_slug}}_pipeline.py 
```

## Testing the pipeline

```shell
pytest test_{{cookiecutter.pipeline_slug}}_pipeline.py 
```
