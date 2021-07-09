import pymongo

class MailModel:
    def __init__(self,  db:str, collection:str):
        # conn_dsn = f'mongodb://{env.USERNAME}:{env.PASSWORD}@localhost:27017'
        conn_dsn =f'mongodb://localhost:27017'
        self.client = pymongo.MongoClient(conn_dsn)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def run(self, data):
        for d in data:
            self._save(d)

    def _save(self, data):
        update_data,filter ={},{}

        filter['link']={'$eq':data['link']}
        update_data['$set'] = data
        self.collection.update_one(filter, update_data, upsert=True)

    def get_client(self):
        return self.client


if __name__=="__main__":
    pass