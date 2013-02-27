from pymongo import MongoClient
from helpers import config


class MongoDBConnection:
    @staticmethod
    def connect(configs=config()):
        """
        tz_aware - if True, datetime instances returned as values in a document by this MongoClient will
        be timezone aware (otherwise they will be naive).

        w: (integer or string) If this is a replica set, write operations will block until they have been
        replicated to the specified number or tagged set of servers. w=<int> always includes the replica
        set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries).

        j: If True block until write operations have been committed to the journal. Ignored if the server
        is running without journaling.
        """
        host = unicode(configs['mongo']['host'])
        port = configs['mongo']['port']
        user = unicode(configs['mongo']['user'])
        password = unicode(configs['mongo']['password'])
        database = unicode(configs['mongo']['database'])
        collection = unicode(configs['mongo']['collection'])

        if host not in ('localhost', '127.0.0.1'):
            connection_uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port) + '/' + database
            db = MongoClient(host=connection_uri, tz_aware=True, w=1, j=True)[database]
        else:
            db = MongoClient(host, port, tz_aware=True, w=1, j=True)[database]

        return db
