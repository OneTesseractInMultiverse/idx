from generators import IdentityGenerator
from log_management.interfaces import MicroserviceLogger
from dao import DataAccessObject
from bson.objectid import ObjectId
import uuid
import json


class UuidIdentityGenerator(IdentityGenerator):

    # -----------------------------------------------------
    # METHOD NEXT IDENTITY
    # -----------------------------------------------------
    def next(self) -> str:
        return str(uuid.uuid4())


class GenericMongoCRUD(DataAccessObject):

    # -----------------------------------------------------
    # CONSTRUCTOR METHOD
    # -----------------------------------------------------
    def __init__(self,
                 db_connection,
                 id_generator: IdentityGenerator,
                 logger: MicroserviceLogger
                 ):
        self.db = db_connection
        self.logger: MicroserviceLogger = logger
        self.id_generator: IdentityGenerator = id_generator
        self.collection = None

    # ------------------------------------------------------
    # QUERY METHOD
    # ------------------------------------------------------
    def query(self, match_criteria: dict) -> list:
        """
            Performs a query based on keyword arguments
            :param match_criteria: a dictionary with keywords to be matched by
                                result.
            :return: a list of results matching the query or an empty list if
                     no matches found.
        """
        results = []
        for entity in self.collection.find(match_criteria):
            entity["_id"] = str(entity["_id"])
            results.append(entity)
        return results

    # -------------------------------------------------------------------------
    # HAS METHOD
    # -------------------------------------------------------------------------
    def has(self, identifier: str, key: str):
        try:
            entity = self.get(
                identifier=identifier,
                key=key
            )
            if entity:
                return True
            return False
        except Exception as e:
            self.logger.error(str(e))
            return False

    # -------------------------------------------------------------------------
    # GET METHOD
    # -------------------------------------------------------------------------
    def get(self, identifier: str, key: str) -> dict or None:
        try:
            matcher: dict = {}
            if key == '_id':
                matcher['_id'] = ObjectId(identifier)
            else:
                matcher[key] = identifier
            entity = self.collection.find_one(matcher)
            entity["_id"] = str(entity["_id"])
            return entity
        except Exception as e:
            self.logger.error(str(e))
            return None

    # -------------------------------------------------------------------------
    # CREATE METHOD
    # -------------------------------------------------------------------------
    def create(self, entity_state: dict) -> dict or None:
        """
            :param entity_state:
            :return:
        """
        try:
            if "_id" in entity_state:
                del entity_state["_id"]
            if 'uid' not in entity_state:
                entity_state['uid'] = self.id_generator.next()
            entity_id = self.collection.insert_one(entity_state).inserted_id
            self.logger.debug(f'Identity created with id: {entity_id}')
            self.logger.debug(str(entity_state))
            if entity_id:
                return entity_state

            return None
        except Exception as e:
            # TODO refactor for better and not too broad exception handling
            self.logger.error(str(e))
        return None

    # -------------------------------------------------------------------------
    # UPDATE METHOD
    # -------------------------------------------------------------------------
    def update(self, entity_id: str, entity_state: dict) -> bool:
        try:
            fields = {}
            for key in entity_state:
                if key != "_id" and key != "id":
                    fields[key] = entity_state[key]
            self.collection.update_one(
                {"_id": ObjectId(entity_id)},
                {"$set": fields}
            )
            return True
        except Exception as e:
            # TODO refactor for better and not too broad exception handling
            self.logger.error(str(e))
        return False

    # -------------------------------------------------------------------------
    # DELETE METHOD
    # -------------------------------------------------------------------------
    def delete(self, entity_id: str) -> bool:
        try:
            self.collection.delete_many({
                "_id": ObjectId(entity_id)
            })
            return True
        except Exception as e:
            # TODO refactor for better and not too broad exception handling
            self.logger.error(str(e))
        return False
