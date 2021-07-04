import pymongo
import env

class HHMongoModel:
    def __init__(self,  db:str, collection:str):
        conn_dsn = f'mongodb://{env.USERNAME}:{env.PASSWORD}@localhost:27017'
        self.client = pymongo.MongoClient(conn_dsn)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def save(self, data):

        update_data ={}

        for d in data:
            filter = {}
            for key in d:
                filter[key]={'$eq':d[key]}
            update_data['$set'] = d
            self.collection.update_many(filter, update_data, upsert=True)

    def get_client(self):
        return self.client

    def find_salary(self, amt, op):
        try:
            return self.collection.find({'salary':{ op : amt }})
        except Exception:
            return False

if __name__=="__main__":
    pass