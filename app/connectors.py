from pymongo import MongoClient

#TODO Not a very beautiful connector. Rewrite/refactor it.
class MongoDBConnection:
    def __init__(self, host, port, user = None, password = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        """
        tz_aware - if True, datetime instances returned as values in a document by this MongoClient will
        be timezone aware (otherwise they will be naive).

        w: (integer or string) If this is a replica set, write operations will block until they have been
        replicated to the specified number or tagged set of servers. w=<int> always includes the replica
        set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries).

        j: If True block until write operations have been committed to the journal. Ignored if the server
        is running without journaling.
        """
        return MongoClient(self.host, self.port, tz_aware = True, w = 1, j = True)

#TODO Add validator for config-file.
def config():
    pass

#TODO add configuration as a db() func parameter.
def connect():
    connection = MongoDBConnection(config['host'], config['port']).connect()
    return connection[config['database']]
