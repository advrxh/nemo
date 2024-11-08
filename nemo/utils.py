import telebot

import os
from pathlib import Path
import zipfile


class Utils:
    def __init__(self, api_key, user_id, zips_dir) -> None:
        self.user_id = user_id
        self.bot = telebot.TeleBot(api_key)

        if isinstance(zips_dir, str):
            self.zips_dir = Path(zips_dir)
        else:
            self.zips_dir = zips_dir

    def upload_to_telegram(self, file_path: Path):
        self.bot.send_document(
            self.user_id, telebot.types.InputFile(file_path), timeout=200
        )

    def zip_a_dir(self, dir_path: Path):

        zip_path = self.zips_dir.joinpath(dir_path.absolute().name + ".zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(
                            os.path.join(root, file), os.path.join(dir_path, "..")
                        ),
                    )

        return zip_path
