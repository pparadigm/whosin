'''
Simple JSON database to store key lookup, namename, and authorization values.
Author: Michael Aldridge

Documentation:
__init__: takes datastore as an argument.  Datastore should be the path to the
file where the database will be stored.

addkey: adds a key to the system.  Takes key, name, and auth, and creates a new
entry.  If upsert is set, an existing entry may be updated.  Teturns 0 on
successful completion.

delkey: removes a key from the system.  Takes key and returns status code (1 for
error, 0 for successful completion)

keylookup: looks up a key in the database.  Takes key and returns namename, auth
on success; otherwise, returns None.

namelist: takes no arguments, returns a list of names.

_save: internal function called to save the database.  Called any time that an
action modifies the database stored in RAM.

_verifyt3: checks the t3 file before committing the backup by overwriting the old
data file. Returns nothing on success, prints the db to the screen on error.
'''
import json
import logging


class db:
    def __init__(self, datastore):
        self.t3file = datastore
        logging.debug("Loading 't3'->'t1'")
        t3data=open(self.t3file)
        self.db=json.load(t3data)
        t3data.close()

    def add(self, key, name, auth, upsert=False):
        logging.info("Adding new key to system")
        if key in self.db: #check if key exists
            if upsert:
                self.db[key]={"name":name, "auth":auth}
                return 0
            else:
                logging.error("name '%s' already exists with key %s; (is upsert set?)",name,key) 
                return 1
        else:
            self.db[key]={"name":name, "auth": auth}
            logging.info("Added name %s with key %s to database", name, key)
            self._save()
            return 0

    def remove(self, key):
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
            return self.db[key]["name"], self.db[key]["auth"]
        else:
            logging.warning("Key not found")
            logging.debug("Key hash was %s", key)
            return None

    def namelist(self):
        names=[]
        logging.info("Retrieving list of names")
        for key in self.db.keys():
            names.append(self.db[key]["name"])
        logging.debug("%s", names)
        return names

    def _save(self):
        logging.info("Syncing 't1'->'t3'")
        t3data=open(self.t3file, 'w')
        #sync t1data to t3data
        json.dump(self.db, t3data, indent=2)
        t3data.close()
