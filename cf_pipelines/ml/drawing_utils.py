import contextlib
import os
import tempfile
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Dict, Set

try:
    import pygraphviz as pgv
except ImportError:
    _has_graphviz = False
else:
    _has_graphviz = True

from IPython.display import Image

from cf_pipelines.ml.machine_learning_step import MachineLearningStep

STEP_2_COLOR = {
    MachineLearningStep.DATA_INGESTION: "darkgreen",
    MachineLearningStep.DATA_VALIDATION: "darkred",
    MachineLearningStep.FEATURE_ENGINEERING: "deepskyblue4",
    MachineLearningStep.MODEL_TRAINING: "orange4",
    MachineLearningStep.MODEL_TESTING: "purple4",
    MachineLearningStep.MODEL_DEPLOYMENT: "teal",
}


def to_title(string):
    return " ".join([t.title() for t in string.split("_")])


STEP_2_TITLE = {k: to_title(k.value) for k in MachineLearningStep}

NODE_PROPERTIES = {"fontcolor": "white", "style": "filled"}

CLUSTER_PROPERTIES = {"style": "dashed", "color": "gray"}


def dict_2_props(thing: Dict) -> str:
    return "[" + (",".join([f"{k}={v}" for k, v in thing.items()])) + "]"


def _generate_graphviz_string(graph) -> str:
    dependencies = graph.solve_dependencies()
    instructions = ["digraph {"]
    instructions.append(f'\trankdir="LR"')

    clusters: Dict[MachineLearningStep, Set[str]] = defaultdict(set)
    function_group: Dict[str, MachineLearningStep] = {}
    for fn, fn_details in graph.function_details.items():
        cluster = MachineLearningStep(fn_details.group)
        function_group[fn] = cluster
        clusters[cluster].add(fn)
        this_node_props = deepcopy(NODE_PROPERTIES)
        this_node_props["fillcolor"] = STEP_2_COLOR[cluster]
        instructions.append(f"\t{fn} {dict_2_props(this_node_props)}")

    instructions.append("")

    for cluster, elements in clusters.items():
        instructions.append(f"\tsubgraph cluster_{cluster.value} {{")
        for element in elements:
            instructions.append(f"\t\t{element};")
        # Subgraph properties
        instructions.append(f"\t\tgraph{dict_2_props(CLUSTER_PROPERTIES)};")
        instructions.append(f'\t\tlabel = "{STEP_2_TITLE[cluster]}";')
        instructions.append("\t}")

    instructions.append("")

    for source, dependencies in dependencies.items():
        for dep in dependencies:
            step = function_group[source]
            step2 = function_group[dep]
            props = {"color": f'"{STEP_2_COLOR[step]};0.5:{STEP_2_COLOR[step2]}"'}
            instructions.append(f"\t{dep}->{source} {dict_2_props(props)}")
    instructions.append("}")

    return "\n".join(instructions)


@contextlib.contextmanager
def _path_for_plot(path_to_plot):
    if path_to_plot == "embed":
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
    else:
        path = str(path_to_plot)

    try:
        yield path
    finally:
        if path_to_plot == "embed":
            Path(path).unlink()


def draw(graph, **kwargs):
    if not _has_graphviz:
        raise ImportError("You need to install pygraphviz")
    graphviz_string = _generate_graphviz_string(graph)
    graph = pgv.AGraph(graphviz_string)
    graph.layout()
    arguments = {
        "-Gsize": kwargs.get("size", "18,30"),
        "-Gdpi": kwargs.get("dpi", "200"),
    }
    program = kwargs.get("program", "dot")

    with _path_for_plot("embed") as path:
        graph.draw(path, prog=program, args=" ".join([f"{k}={v}" for k, v in arguments.items()]))

        return Image(path)
