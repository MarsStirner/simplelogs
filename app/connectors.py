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
        host = unicode(config['mongo']['host'])
        port = unicode(config['mongo']['port'])
        user = unicode(config['mongo']['user'])
        password = unicode(config['mongo']['password'])
        database = unicode(config['mongo']['database'])
        collection = unicode(config['mongo']['collection'])

        if host not in ('localhost', '127.0.0.1'):
            connection_uri = "mongodb://" + user + ":" + password + "@" + host + ":" + port + '/' + database
            db = MongoClient(host=connection_uri, tz_aware=True, w=1, j=True)
        else:
            db = MongoClient(host, port, tz_aware=True, w=1, j=True)[database]

        return db
