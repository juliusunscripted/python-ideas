## example code for duckdb github issue: https://github.com/duckdb/duckdb/issues/18152

# %%

from pathlib import Path
import duckdb

# %%

data_dir = Path() / "data"


# %%

# Create some test data using DuckDB
con = duckdb.connect()

# Create a sample table
con.execute(
    """
    CREATE TABLE test_data AS
    SELECT 
        i AS id,
        'name_' || i AS name,
        i % 3 AS category
    FROM range(10) AS t(i)
"""
)

# # single parqut test (works as expected)
# for e in ["a-hive-value", "b-hive-value", "c-hive-value"]:
#     # Export the table as a Parquet file
#     parquet_path = data_dir / f"single-parquet/hive_test={e}/test_data.parquet"

#     # Ensure parquet parent directory exists
#     parquet_path.parent.mkdir(parents=True, exist_ok=True)

#     con.execute(f"COPY test_data TO '{parquet_path}' (FORMAT 'parquet')")


# %%


# query = f"""
# select
#   *
# from read_parquet('{data_dir.as_posix()}/single-parquet/**/*.parquet', hive_partitioning = true)
# """

# result = con.sql(query=query)
# result.show()

# %%
db_export_base_dir = data_dir / "db_export"


for e in ["a-hive-value", "b-hive-value", "c-hive-value"]:
    # Export the table as a Parquet file
    db_export_dir = db_export_base_dir / f"hive_test={e}/a"

    # Ensure parquet parent directory exists
    db_export_dir.mkdir(parents=True, exist_ok=True)
    db_export_dir.parent.mkdir(parents=True, exist_ok=True)
    con.sql(
        f"EXPORT DATABASE '{db_export_dir.as_posix()}' (FORMAT parquet, COMPRESSION zstd)"
    )


# %%
con.close()
# %%


con = duckdb.connect()

# %%

# this works
query = f"""
select
  *
from read_parquet('{db_export_base_dir.as_posix()}/**/*.parquet', hive_partitioning = true)
"""

result = con.sql(query=query)
result.show()

# %%

# this fails (but should work in my opinion)
query = f"""
IMPORT DATABASE '{db_export_dir}';
"""

con.sql(query=query)

# %%
