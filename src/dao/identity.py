from dao.mongodb import GenericMongoCRUD
from generators import IdentityGenerator
from log_management.interfaces import MicroserviceLogger


class Identities(GenericMongoCRUD):

    def __init__(
            self,
            db_connection,
            id_generator: IdentityGenerator,
            logger: MicroserviceLogger):
        super().__init__(db_connection, id_generator, logger)
        self.collection = self.db['identities']

    def create(self, entity_state: dict) -> dict or None:
        entity_state['type'] = 'x-type-appsec-identity'
        return super().create(entity_state)

    def query(self, match_criteria: dict) -> list:
        selector = {
            "type": "x-type-appsec-identity"
        }
        if 'org_id' in match_criteria:
            selector['org_id'] = match_criteria['org_id']
        return super().query(selector)