import logging

logger = logging.getLogger("custom serializers")
try:
    # All the non-standard imports should be wrapped in a try-except blog warning people about
    # missing modules
    import pandas as pd
except ModuleNotFoundError as mnfe:
    logger.warning("Failed to import pandas, make sure it is installed")


def write_csv(obj, product):
    obj.to_csv(product, index=False)


def read_csv(product):
    return pd.read_csv(product)


def write_parquet(obj, product):
    obj.to_parquet(product, index=False)


def read_parquet(product):
    return pd.read_parquet(product)


def write_txt(obj, product):
    with open(product, "w") as w:
        w.write(obj)


def read_txt(product):
    with open(product) as r:
        return r.read()


def write_fig(obj, product):
    obj.savefig(product)
