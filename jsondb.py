import json
import logging

class db:
    def __init__(self, datastore):
        self.t3file = datastore
        logging.debug("Loading 't3'->'t1'")
        t3data=open(self.t3file)
        self.db=json.load(t3data)
        #self.db{key: {"user":user, "auth": auth}} #load the data
        t3data.close()

    def addkey(self, key, user, auth):
        logging.info("Adding new key to system")
        if key in self.db: #check if key exists
            logging.warning("User already exists with key {0}",key) 
            return(1)
        else:
            self.db[key]={"user":user, "auth": auth}
            logging.info("Added user {0} with key {1} to database", user, key)
            self._dbsync()
            return(0)

    def delkey(self, key):
        logging.info("Removing key from system")
        if key in self.db: #check if key exists
            del self.db[key]
            logging.info("Key id {0} removed", key)
            self._dbsync()
            return(0)
        else:
            logging.warning("Key does not exist")
            return(1)
        
    def keylookup(self, key):
        logging.info("Looking up key {0}")
        if key in self.db: #check if key exists
            logging.info("Key found")
            logging.debug("Returned data {0}", self.db[key])
            return self.db[key]["user"], self.db[key]["auth"]
        else:
            logging.warning("Key not found")
            logging.debug("Key hash was {0}", key)
            return(None)
    def forcedbsave(self):
        logging.info("DB sync was forced")
        self._dbsync()

    def _dbsync(self):
            logging.info("Syncing 't1'->'t3'")
            t3data=open(self.t3file, 'w')
            #sync t1data to t3data
            json.dump(self.db, t3data, indent=2)
            t3data.close()
