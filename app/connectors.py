from pymongo import MongoClient
from helpers import config

config = config()

class MongoDBConnection:
    @staticmethod
    def connect():
        """
        tz_aware - if True, datetime instances returned as values in a document by this MongoClient will
        be timezone aware (otherwise they will be naive).

        w: (integer or string) If this is a replica set, write operations will block until they have been
        replicated to the specified number or tagged set of servers. w=<int> always includes the replica
        set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries).

        j: If True block until write operations have been committed to the journal. Ignored if the server
        is running without journaling.
        """
        host = config['mongo']['host']
        port = config['mongo']['port']
        user = config['mongo']['user']
        password = config['mongo']['password']
        database = config['mongo']['database']
        collection = config['mongo']['collection']

        #TODO add authorization mechanism for MongoDB
        connection = MongoClient(host, port, tz_aware = True, w = 1, j = True)
        return connection[database]
