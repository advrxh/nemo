import typer

from pathlib import Path
import os

from typing_extensions import Annotated
from typing import Optional

from utils import Utils


nemo = typer.Typer()

TELEGRAM_API_KEY = os.getenv("NEMO_API_KEY")
TELEGRAM_USER_ID = os.getenv("NEMO_USER_ID")
ZIPS_DIR = os.getenv("NEMO_ZIPS_DIR", Path("./"))


@nemo.command(name="ping", help="PING.", short_help="ping.")
def ping():
    typer.secho(f"Pong 🏓", fg=typer.colors.BRIGHT_CYAN)


@nemo.command(
    help="This is a file upload utility.",
    short_help="file. upload. happy.",
)
def upload(
    path: Annotated[Optional[Path], typer.Option()],
    compress: bool = False,
):

    if TELEGRAM_API_KEY is None:
        typer.secho(
            f"No API KEY found. ($NEMO_API_KEY)", bold=True, fg=typer.colors.RED
        )
        raise typer.Abort()

    if TELEGRAM_USER_ID is None:
        typer.secho(
            f"No USER ID found. ($NEMO_USER_ID)", bold=True, fg=typer.colors.RED
        )
        raise typer.Abort()

    utils = Utils(TELEGRAM_API_KEY, TELEGRAM_USER_ID, ZIPS_DIR)

    if path.is_dir():

        if not compress:
            files = list(path.iterdir())

            with typer.progressbar(files, label="Uploading files...") as progress:
                for file in progress:
                    utils.upload_to_telegram(file)

            typer.secho(f"Done ✅", fg=typer.colors.BRIGHT_GREEN)

        else:
            zipped_dir = utils.zip_a_dir(path)

            with typer.progressbar(
                label="Uploading zip archive...", length=100
            ) as progress:
                utils.upload_to_telegram(zipped_dir)
                progress.update(100)

            typer.secho(f"Done ✅", fg=typer.colors.BRIGHT_GREEN)
    else:
        with typer.progressbar(
            label=f"Uploading {path.name}...", length=100
        ) as progress:
            utils.upload_to_telegram(path)
            progress.update(100)

        typer.secho(f"Done ✅", fg=typer.colors.BRIGHT_GREEN)


if __name__ == "__main__":
    nemo()
