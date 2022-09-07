from ploomber.io import serializer, serializer_pickle, unserializer, unserializer_pickle

from cf_pipelines.serializers.custom import (
    read_csv,
    read_parquet,
    read_txt,
    write_csv,
    write_fig,
    write_parquet,
    write_txt,
)


@serializer({".csv": write_csv})
@serializer({".txt": write_txt})
@serializer({".parquet": write_parquet})
@serializer({".png": write_fig})
def file_serializer(obj, product):
    serializer_pickle(obj, product)


@unserializer({".csv": read_csv})
@unserializer({".txt": read_txt})
@unserializer({".parquet": read_parquet})
def file_unserializer(product):
    return unserializer_pickle(product)
