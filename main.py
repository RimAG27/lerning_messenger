import csv
import os
from datetime import datetime

class Session:
    def __init__(self, filename: str = "messages.csv"):
        self.filename = filename
        self._file_exists()

    def _file_exists(self) -> None:
        file_exists = os.path.isfile(self.filename)
        if not file_exists:
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer =  csv.writer(file)
                writer.writerow(["timestamp","message"])

    def send_message(self, message: str) -> None:
        if not message or not str(message).strip():
            raise ValueError("Сообщение не может быть пустым")

        timestamp = datetime.now()

        with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp,message])
