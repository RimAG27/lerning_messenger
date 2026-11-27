import csv
import json
import os
from datetime import datetime
from uuid import UUID, uuid4


class Correspondence:
    DATA_DIR = "data"
    CORRESPONDENCE_DIR = os.path.join(DATA_DIR, "correspondence")

    def __init__(self, creator: str, participants: tuple[str, ...] | None = None,
                 uuid: str | UUID | None = None) -> None:
        self.identifier = uuid if uuid is not None else uuid4()
        self.identifier = str(self.identifier)
        self.chat_dir = os.path.join(self.CORRESPONDENCE_DIR, self.identifier)
        self.meta = os.path.join(self.chat_dir, "metadata.json")
        self.filename = os.path.join(self.chat_dir, "content.csv")

        self.creator = creator
        self.created_at = datetime.now().isoformat()

        self.participants: list[str] = [creator]
        for participant in (participants or ()):
            if participant not in self.participants:
                self.participants.append(participant)

        self._file_exists()
        self._save_meta()


    def _file_exists(self) -> None:
        os.makedirs(self.chat_dir, exist_ok=True)

        if not os.path.isfile(self.filename):
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "sender", "recipients", "message"])

        if not os.path.isfile(self.meta):
            self._save_meta()

    def _save_meta(self) -> None:
        os.makedirs(self.chat_dir, exist_ok=True)

        meta = {
            "identifier": self.identifier,
            "creator": self.creator,
            "created_at": self.created_at,
            "participants": self.participants,
        }
        with open(self.meta, mode="w", encoding="utf-8") as file:
            json.dump(meta, file, ensure_ascii=False, indent=4)

    def _load_meta(self) -> dict:
        with open(self.meta, mode="r", encoding="utf-8") as file:
            return json.load(file)


    def add_participant(self, participant: str) -> None:
        if not participant.strip():
            raise ValueError("Имя участника не может быть пустым")

        meta = self._load_meta()
        if participant in meta["participants"]:
            raise ValueError(f"'{participant}' уже участвует в переписке")

        meta["participants"].append(participant)
        self.participants = meta["participants"]

        with open(self.meta, mode="w", encoding="utf-8") as file:
            json.dump(meta, file, ensure_ascii=False, indent=4)

    def send_message(self, message: str, sender: str,
                     recipients: tuple[str, ...]) -> None:
        if not message.strip():
            raise ValueError("Сообщение не может быть пустым")

        participants = set(self.participants)

        if sender not in participants:
            raise ValueError(f"Отправитель '{sender}' не участвует в переписке")

        unknown = []
        for recipient in recipients:
            if recipient not in participants:
                unknown.append(recipient)

        if unknown:
            raise ValueError(
                f"Получатели не участвуют в переписке: {', '.join(unknown)}"
            )

        timestamp = datetime.now().isoformat()

        with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, sender, ";".join(recipients), message])

    def get_messages(self) -> str:
        meta = self._load_meta()

        lines = []
        lines.append("=" * 60)
        lines.append(f"Переписка {meta['identifier']}")
        lines.append(f"Создатель: {meta['creator']}")
        lines.append(f"Создана:   {meta['created_at']}")
        lines.append(f"Участники: {', '.join(meta['participants'])}")
        lines.append("=" * 60)

        if not os.path.isfile(self.filename):
            lines.append("Сообщений нет.")
            return "\n".join(lines)

        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # пропускаем заголовок
            for row in reader:
                if not row:
                    continue
                timestamp, sender, recipients, message = row
                recipient_list = [r for r in recipients.split(";") if r]
                recipients_str = ", ".join(recipient_list)
                lines.append(f"[{timestamp}] {sender} → {recipients_str}: {message}")

        return "\n".join(lines)


class Auth:
    """Авторизация."""
    ...
