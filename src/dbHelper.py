import redis

class database:
    "a wrapper class using redis API"
    def __init__(self):
            self.db = redis.StrictRedis()
        
    def dbQuery(self,key):
        "query the database"
        return self.db.get(hash(key))
    
    def dbStore(self,key,value):
        "store the key-value pair"
        return self.db.set(hash(key),value)
    
    def dbDelete(self,key):
        "delete the entry keyed by key"
        return self.db.delete(hash(key))




