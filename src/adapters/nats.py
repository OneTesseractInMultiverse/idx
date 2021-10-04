import json


class NATSMessage:

    def __init__(self, nats_message: any):
        self.__subject = nats_message.subject
        self.__message_data = nats_message.data

    @staticmethod
    def __cant_be_uuid(text):
        for character in text.lower():
            if ord(character) > 102:
                return True
        return False

    @property
    def dict(self) -> dict:
        return json.loads(
            self.__message_data.decode()
        )

    @property
    def action(self) -> str or None:
        subject_parts = self.__subject.split('.')
        if self.__cant_be_uuid(subject_parts[-1]):
            return subject_parts[-1]
        return subject_parts[-2]

    def has_uid_in_subject(self) -> bool:
        subject_parts = self.__subject.split('.')
        if not self.__cant_be_uuid(subject_parts[-1]):
            return True
        return False