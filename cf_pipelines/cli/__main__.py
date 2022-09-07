import pkg_resources
import typer
from cookiecutter.main import cookiecutter

app = typer.Typer()


@app.command()
def new():
    template_path = pkg_resources.resource_filename("cf_pipelines", "ml/project_template")
    cookiecutter(template_path)


# TODO: remove when/if we add more commands
# https://typer.tiangolo.com/tutorial/commands/one-or-multiple/#one-command-and-one-callback
@app.callback()
def callback():
    pass


def main():
    app()
