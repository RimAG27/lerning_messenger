import csv
import os
from datetime import datetime
from uuid import uuid4
import json

class Correspondence:
    def __init__(self, creator: str, participants: tuple[str, ...] | None = None):
        self.identifier = uuid4()
        self.filename = f"{str(self.identifier)}.csv"
        self.meta = f"{str(self.identifier)}.json"
        self.creator = creator
        self.created_at = datetime.now().isoformat()
        self.participants: list[str] = list({creator, *(participants or ())})
        self._file_exists()
        self._save_meta()

    def _file_exists(self) -> None:
        file_exists = os.path.isfile(self.filename)
        if not file_exists:
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer =  csv.writer(file)
                writer.writerow(["timestamp", "sender", "recipients", "message"])

    def _save_meta(self) -> None:
        meta = {
            "identifier": str(self.identifier),
            "creator": self.creator,
            "created_at":self.created_at,
            "participants": self.participants,
        }
        with open(self.meta, mode="w", encoding="utf-8") as file:
            json.dump(meta, file, ensure_ascii=False, indent=2)

    def _load_meta(self) -> dict:
        with open(self.meta, mode="r", encoding="utf-8") as file:
            return json.load(file)

    def send_message(self, message: str, sender: str, recipients: tuple[str, ...
    ]) -> None:
        if not message.strip():
            raise ValueError("Сообщение не может быть пустым")
        meta = self._load_meta()
        participants = set(meta["participants"])
        if sender not in participants:
            raise ValueError(f"Отправитель '{sender}' не участвует в переписке")
        unknown = [r for r in recipients if r not in participants]
        if unknown:
            raise ValueError(
                f"Получатели не участвуют в переписке: {', '.join(unknown)}"
            )

        timestamp = datetime.now().isoformat()

        with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, sender, ";".join(recipients), message])

    def get_messages(self) ->None:
        meta = self._load_meta()
        print("=" * 60)
        print(f"Переписка {meta['identifier']}")
        print(f"Создатель: {meta['creator']}")
        print(f"Создана:   {meta['created_at']}")
        print(f"Участники: {', '.join(meta['participants'])}")
        print("=" * 60)

        if not os.path.isfile(self.filename):
            print("Сообщений нет.")
            return

        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if not row:
                    continue
                timestamp, sender, recipients, message = row
                print(f"[{timestamp}] {sender} {recipients}: {message}")
