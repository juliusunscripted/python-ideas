import pyarrow as pa


def table_from_list_dict(list_dict: list[dict], schema: pa.Schema):
    return pa.Table.from_pylist(list_dict, schema=schema)


def batch_from_list_dict(list_dict: list[dict], schema: pa.Schema):
    return pa.RecordBatch.from_pylist(list_dict, schema=schema)
