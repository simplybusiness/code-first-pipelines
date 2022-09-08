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
