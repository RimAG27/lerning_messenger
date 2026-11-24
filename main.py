import csv
import os
from datetime import datetime
from uuid import uuid4

class Correspondence:
    # TODO: Добавить поле - идентификатор сессии. UUID()
    # TODO: Называть файл не по имени messages.csv, а в формате
    #  идентификатор.csv.
    # TODO: send_message должен получать имена отправителя и список
    #  получателей.
    # TODO: добавить метод get_messages получения переписки. Пока в консоль.
    # TODO: добавить метаданные переписки:
    #  - Список пользователей, которые участвуют в переписке.
    #  - Дата создания переписки.
    #  - Создатель переписки.
    #  Хранить в формате .json. Имя файла - идентификатор.json.
    #  Библиотека json.
    # TODO: send_message должен проверять, что sender и recipients есть в
    #  метаданных.
    def __init__(self, filename: str = "messages.csv"):
        self.identifier = uuid4()
        self.filename = f"{str(self.identifier)}.csv"
        self.meta = f"{str(self.identifier)}.json"
        self._file_exists()

    def _file_exists(self) -> None:
        file_exists = os.path.isfile(self.filename)
        if not file_exists:
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer =  csv.writer(file)
                writer.writerow(["timestamp","message"])

    def send_message(self, message: str, sender: str, recipients: tuple[str, ...
    ]) -> None:
        if not message or not str(message).strip():
            raise ValueError("Сообщение не может быть пустым")

        timestamp = datetime.now()

        with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp,message])
