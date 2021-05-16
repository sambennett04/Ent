from azure.cosmos import exceptions, CosmosClient, PartitionKey
from default_values import CDB_URI, CDB_DATABASE, CDB_CONTAINER, CDB_PKEY, CDB_KEY
import uuid, os

class DataService():
	
	def __init__(self):
		
		__key = os.environ.get("CDB_KEY") or CDB_KEY
		
		self.endpoint = os.environ.get("CDB_URI") or CDB_URI
		self.database = os.environ.get("CDB_DATABASE") or CDB_DATABASE
		self.container = os.environ.get("CDB_CONTAINER") or CDB_CAONTAINER
		self.partitionKey = os.environ.get("CDB_PKEY") or CDB_PKEY
		self.client = CosmosClient(self.endpoint, __key)
	
	def write_document(self, document: object) -> bool:
		
		idKey = "id"
		
		if not idKey in document.keys():
			document[idKey] = str(uuid.uuid4())
		
		if not partitionKey in document.keys():
			document[self.partitionKey] = str(uuid.uuid4())
		
		database = self.client.get_database_client(self.database)
		container = database.get_container_client(self.container)
		result = container.create_item(document)
		
		return type(result) == dict
