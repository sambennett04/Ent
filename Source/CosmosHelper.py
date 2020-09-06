from azure.cosmos import exceptions, CosmosClient, PartitionKey
from json import load, dumps

import uuid
import os.path

CONFIGURATION_PATH = os.path.join("Configuration", "CosmosConfiguration.json")

class CosmosHelper(object):

    def __init__(self, endpoint: str = None, key: str = None, database: str = None, container: str = None, partKey = None):
        
        jsonObj = self.__get_config()

        self.__endpoint = endpoint or self.__get_endpoint(jsonObj)
        self.__key = key or self.__get_key(jsonObj)
        self.__defaultDatabase = database or self.__get_database(jsonObj)
        self.__defaultContainer = container or self.__get_container(jsonObj)
        self.__defaultPartitionKey = partKey or self.__get_partition_key(jsonObj)

        self.__client = CosmosClient(self.__endpoint, self.__key)
        
    def __str__(self) -> str:

        return dumps(str(self.__dict__))
    
    def __get_config(self):

        jsonFile = open(CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj
    
    def __get_endpoint(self, jsonObj):

        endpoint = jsonObj["endpoint"]

        return endpoint

    def __get_key(self, jsonObj):

        key = jsonObj["key"]

        return key

    def __get_database(self, jsonObj):

        database = jsonObj["database"]

        return database

    def __get_container(self, jsonObj):

        container = jsonObj["container"]

        return container

    def __get_partition_key(self, jsonObj):

        partKey = jsonObj["partition_key"]

        return partKey

    def write_document(self, document: dict, databaseName: str = None, containerName: str = None, partitionKey: str = None) -> bool:

        databaseName = databaseName or self.__defaultDatabase
        containerName = containerName or self.__defaultContainer

        idKey = "id"
        partitionKey = partitionKey or self.__defaultPartitionKey

        if not idKey in document.keys():
            document[idKey] = str(uuid.uuid4())
        
        if not partitionKey in document.keys():
            document[partitionKey] = str(uuid.uuid4())

        database = self.__client.get_database_client(databaseName)
        container = database.get_container_client(containerName)
        result = container.create_item(document)

        if type(result) != dict:
            return False
        
        return True
    
if __name__ == "__main__":
    
    doc = {"msg": "we are writing documents..."}

    helper = CosmosHelper()

    print(str(helper))

    res = helper.write_document(doc)

    print(str(res))