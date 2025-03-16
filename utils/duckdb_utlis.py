import duckdb
from typing import Any
from pathlib import Path
from random import choice
from string import ascii_uppercase
import pyarrow as pa
import structlog
from typing import Optional, Literal

log = structlog.stdlib.get_logger()

# %%


def _random_string(length: int):
    return "".join(choice(ascii_uppercase) for i in range(length))


def query_result_to_parquet_file(result: duckdb.DuckDBPyRelation, file_path: Path):
    file_path = file_path.absolute()
    # https://csatlas.com/python-create-directory/
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # arrow_table = result.arrow()
    # pq.write_table(arrow_table, "example.parquet", compression="lz4")
    result.to_parquet(file_name=file_path.absolute().as_posix(), compression="zstd")


def query_result_to_csv_file(
    result: duckdb.DuckDBPyRelation,
    file_path: Path,
    sep: str | None = None,
    na_rep: Literal[",", ";"] | str | None = None,
    header: bool | None = True,
    quotechar: Literal['"'] | str | None = None,
    escapechar: str | None = None,
    date_format: Literal["%Y-%m-%dT%H:%M:%S"] | str | None = None,
    timestamp_format: Literal["%Y-%m-%dT%H:%M:%S"] | str | None = None,
    quoting: str | int | None = None,
    encoding: str | None = None,
    compression: Optional[Literal["zstd", "gzip"]] = None,
) -> None:
    """_summary_

    Args:
        result (duckdb.DuckDBPyRelation): _description_
        file_path (Path): _description_
        sep (str | None, optional): _description_. Defaults to None.
        na_rep (Literal[",", , optional): _description_. Defaults to None.
        header (bool | None, optional): _description_. Defaults to True.
        quotechar (Literal['"'] | str | None, optional): _description_. Defaults to None.
        escapechar (str | None, optional): _description_. Defaults to None.
        date_format (_type_, optional): _description_. Defaults to None.
        timestamp_format (_type_, optional): _description_. Defaults to None.
        quoting (str | int | None, optional): _description_. Defaults to None.
        encoding (str | None, optional): _description_. Defaults to None.
        compression (Optional[Literal["zstd", "gzip"]], optional): _description_. Defaults to None.
    """
    file_path = file_path.absolute()
    # https://csatlas.com/python-create-directory/
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # https://duckdb.org/docs/sql/statements/copy.html#csv-options
    # https://duckdb.org/docs/sql/functions/dateformat.html
    # https://duckdb.org/docs/sql/functions/dateformat.html#format-specifiers
    result.to_csv(
        file_name=file_path.absolute().as_posix(),
        sep=sep,
        na_rep=na_rep,
        header=header,
        quotechar=quotechar,
        escapechar=escapechar,
        date_format=date_format,
        timestamp_format=timestamp_format,
        quoting=quoting,
        encoding=encoding,
        compression=compression,
    )


def register_python_object_as_view(con: duckdb.DuckDBPyConnection, python_object: Any):
    view_name = f"python_object_{_random_string(length=5)}"
    con.register(view_name=view_name, python_object=python_object)
    return view_name


def export_database(con: duckdb.DuckDBPyConnection, export_directory_path: Path):
    export_directory_path = export_directory_path.absolute()
    export_directory_path.parent.mkdir(parents=True, exist_ok=True)
    query = rf"""
    EXPORT DATABASE '{export_directory_path.as_posix()}' (
        FORMAT PARQUET,
        COMPRESSION ZSTD
    );
    """
    con.sql(query=query)
    log.info("exported duckdb database", path=export_directory_path.as_posix())


def copy_database_to_file(
    con: duckdb.DuckDBPyConnection, file_path: Path, database_name: str = "memory"
):
    file_path = file_path.resolve()
    if file_path.is_file():
        log.error("cannot copy database to this path. file already exists")
        raise FileExistsError(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # https://stackoverflow.com/a/78930283
    query_attach_export_file = f"attach '{file_path.as_posix()}' as copy_db_file;"
    query_copy_db = f"copy from database {database_name} to copy_db_file;"
    query_detach_file = "detach database copy_db_file;"
    for q in [query_attach_export_file, query_copy_db, query_detach_file]:
        con.sql(query=q)


def copy_file_to_database(
    con: duckdb.DuckDBPyConnection, file_path: Path, database_name: str = "memory"
):
    file_path = file_path.resolve()
    if not file_path.is_file():
        log.error("cannot copy database from this file. file does not exist")
        raise FileNotFoundError(file_path)
    # https://stackoverflow.com/a/78930283
    query_attach_export_file = (
        f"attach '{file_path.as_posix()}' as copy_db_file (READ_ONLY);"
    )
    query_copy_db = f"copy from database copy_db_file to {database_name};"
    query_detach_file = "detach database copy_db_file;"
    for q in [query_attach_export_file, query_copy_db, query_detach_file]:
        con.sql(query=q)


def create_table_from_schema(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    schema: pa.Schema,
    replace_existing=True,
):
    empty_table = schema.empty_table()
    view_name = register_python_object_as_view(con=con, python_object=empty_table)
    query = ""
    if replace_existing:
        query += "create or replace table "
    else:
        query += "create table if not exists "

    query += f"{table_name} as (select * from {view_name})"
    con.sql(query=query)
    con.unregister(view_name=view_name)
