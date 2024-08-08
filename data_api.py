import requests

class MongoDB:
    def __init__(self, dbkey, appid, datasource):
        self.dbk = dbkey
        self.aid = appid
        self.ds = datasource
    
    
    def find_doc(self, collection, database, filters, sortby=None, limit=None):
        headers = {
        'Content-Type': 'application/ejson',
        'Accept': 'application/json',
        'api-key': self.dbk,
        }

        json_data = {
            'collection': collection,
            'database': database,
            'dataSource': self.ds,
            'filter': {i for i in filters},
        }
        if sortby != None:
            json_data["sort"] = {i for i in sortby}
        if limit != None:
            json_data["limit"] = limit

        response = requests.post(
            self.aid+'/action/find',
            headers=headers,
            json=json_data,
        )
        return response

    def insert_docs(self, collection, database, documents, many=False):
        headers = {
        'Content-Type': 'application/ejson',
        'Accept': 'application/json',
        'api-key': self.dbk,
        }

        json_data = {
            'collection': collection,
            'database': database,
            'dataSource': self.ds,
            'documents': documents,
        }

        action = "/action"
        
        if many:
            action += '/insertMany'
        else:
            action += '/insertOne'
        
        response = requests.post(
            self.aid+action,
            headers=headers,
            json=json_data,
        )
        return response

    def update_docs(self, collection, database, filters, to_update, many=False):
        headers = {
        'Content-Type': 'application/ejson',
        'Accept': 'application/json',
        'api-key': self.dbk,
        }

        json_data = {
            'collection': collection,
            'database': database,
            'dataSource': self.ds,
            'filter': {i for i in filters},
            'update': {'$set': {i for i in to_update}}
        }
        action = "/action"
        if many:
            action += '/updateMany'
        else:
            action += '/updateOne'
            
        response = requests.post(
            self.aid+action,
            headers=headers,
            json=json_data,
        )
        return response

    def replace_docs(self, collection, database, filters, replacement, many=False):
        headers = {
        'Content-Type': 'application/ejson',
        'Accept': 'application/json',
        'api-key': self.dbk,
        }

        json_data = {
            'collection': collection,
            'database': database,
            'dataSource': self.ds,
            'filter': {i for i in filters},
            'replacement': replacement
        }

        action = "/action"
        if many:
            action += '/replaceMany'
        else:
            action += '/replaceOne'    
        
        response = requests.post(
            self.aid+action,
            headers=headers,
            json=json_data,
        )
        return response

    def delete_docs(self, collection, database, filters, replacement, many=False):
        headers = {
        'Content-Type': 'application/ejson',
        'Accept': 'application/json',
        'api-key': self.dbk,
        }

        json_data = {
            'collection': collection,
            'database': database,
            'dataSource': self.ds,
            'filter': {i for i in filters},
            'replacement': replacement
        }

        action = "/action"
        if many:
            action += '/deleteMany'
        else:
            action += '/deleteOne'
        
        response = requests.post(
            self.aid+action,
            headers=headers,
            json=json_data,
        )
        return response