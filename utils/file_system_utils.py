from pathlib import Path
from io import BytesIO
import structlog

log = structlog.stdlib.get_logger()


def get_path_data() -> Path:
    """return absolute path to data dir of repo (code gets adjusted for every repo)

    Returns:
        Path: absolute file path of data dir
    """
    path_of_this_file = Path(__file__).parent.resolve()
    download_folder = path_of_this_file / "../../data/"
    download_folder = download_folder.resolve()
    log.debug(
        "paths",
        path_of_this_file=path_of_this_file.as_posix(),
        download_folder=download_folder.as_posix(),
    )
    log
    return download_folder


def bytes_to_file(file_bytes: bytes | bytearray | BytesIO, file_path: Path):
    if not file_path.parent.is_dir():
        file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode="wb") as f:
        f.write(file_bytes)
