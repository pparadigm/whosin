import json
import logging

class db:
    def __init__(self, datastore):
        self.t3file = datastore
        logging.debug("Loading 't3'->'t1'")
        t3data=open(self.t3file)
        self.db=json.load(t3data)
        t3data.close()

    def addkey(self, key, user, auth, upsert=False):
        logging.info("Adding new key to system")
        if key in self.db: #check if key exists
            if upsert:
                self.db[key]={"user":user, "auth":auth}
                logging.warning("User '%s' already exists with key %s",user,key) 
                return 0
            else:
                logging.error("User '%s' already exists with key %s; (is upsert set?)",user,key) 
                return 1
        else:
            self.db[key]={"user":user, "auth": auth}
            logging.info("Added user %s with key %s to database", user, key)
            self._save()
            return 0

    def delkey(self, key):
        logging.info("Removing key from system")
        if key in self.db: #check if key exists
            del self.db[key]
            logging.info("Key id %s removed", key)
            self._save()
            return 0
        else:
            logging.warning("Key does not exist")
            return 1
        
    def keylookup(self, key):
        logging.info("Looking up key %s")
        if key in self.db: #check if key exists
            logging.info("Key found")
            logging.debug("Returned data %s", self.db[key])
            return self.db[key]["user"], self.db[key]["auth"]
        else:
            logging.warning("Key not found")
            logging.debug("Key hash was %s", key)
            return None

    def _save(self):
        logging.info("Syncing 't1'->'t3'")
        t3data=open(self.t3file, 'w')
        #sync t1data to t3data
        json.dump(self.db, t3data, indent=2)
        t3data.close()
