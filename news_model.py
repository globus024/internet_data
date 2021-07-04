import pymongo
import env

class NewsModel:
    def __init__(self,  db:str, collection:str):
        # conn_dsn = f'mongodb://{env.USERNAME}:{env.PASSWORD}@localhost:27017'
        conn_dsn =f'mongodb://localhost:27017'
        self.client = pymongo.MongoClient(conn_dsn)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def save(self, data):
        update_data ={}

        filter = {}
        for key in data:
            filter[key]={'$eq':data[key]}
        update_data['$set'] = data
        self.collection.update_one(filter, update_data, upsert=True)

    def get_client(self):
        return self.client

    def find_salary(self, amt, op):
        try:
            return self.collection.find({'salary':{ op : amt }})
        except Exception:
            return False

if __name__=="__main__":
    pass