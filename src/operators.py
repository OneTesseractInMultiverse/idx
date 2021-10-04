

from adapters.nats import NATSMessage
from dao.identity import Identities
from dao.mongodb import UuidIdentityGenerator
from log_management.interfaces import MicroserviceLogger


def wrap_into_appsec_messaging_space(func) -> ():
    def decorator(self):
        try:
            result = func(self)
            if '_id' in result:
                result['_id'] = str(result['_id'])
            return {
                'code': 200,
                'result': result
            }
        except Exception as e:
            return {
                'error': str(e),
                'code': 500
            }
    return decorator


class IdentityOperation:

    def __init__(self, logger: MicroserviceLogger, message: any, db_provider_func):
        self.nats_message: NATSMessage = NATSMessage(message)
        self.db_connection_provider = db_provider_func
        self.identities: Identities = Identities(
            db_connection=self.db_connection_provider(),
            id_generator=UuidIdentityGenerator(),
            logger=logger
        )
        self.handlers: dict = {
            'new': self.__create_identity,
            'update': self.__update_identity,
            'list': self.__query_identity,
            'get': self.__get_identity,
            'delete': None
        }
        self.logger = logger

    @wrap_into_appsec_messaging_space
    def __create_identity(self):
        return self.identities.create(self.nats_message.dict)

    @wrap_into_appsec_messaging_space
    def __query_identity(self):
        return self.identities.query(self.nats_message.dict)

    @wrap_into_appsec_messaging_space
    def __get_identity(self):
        return self.identities.get(
            self.nats_message.dict['uid'],
            'uid'
        )

    @wrap_into_appsec_messaging_space
    def __update_identity(self):
        return self.identities.update(
            self.nats_message.dict['uid'],
            self.nats_message.dict
        )

    def exec(self):
        self.logger.info(f'Executing action: {self.nats_message.action}')
        fn = self.handlers[self.nats_message.action]
        return fn()




