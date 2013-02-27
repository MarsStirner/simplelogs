import unittest
from bson import ObjectId
import json

from app import app
from app.helpers import config, url
from app.connectors import MongoDBConnection
from app.models import LogEntry
from app.views import get_levels_list, index
from app.views import VERSION


class ConfigFileTestCase(unittest.TestCase):
    def test_config_file(self):
        """Test for app.helpers.config"""
        result = config()
        first_level_keys = ['mongo', 'level']
        second_level_keys = ['host', 'user', 'database', 'password', 'port', 'collection']
        for key in first_level_keys:
            if not key in result:
                self.assertTrue(False, "Key '%s' is missing." % key)
        for key in second_level_keys:
            if not key in result['mongo']:
                self.assertTrue(False, "Key '%s' is missing." % key)


class URLTestCase(unittest.TestCase):
    def test_add_new_url(self):
        """Test for app.helpers.url"""
        new_url = '/test_url/'
        url(new_url, '')
        self.assertTrue(new_url in [rule.__str__() for rule in app.url_map.iter_rules()],
                        msg="New URL wasn't added to known URLs-list.")


class ConnectionTestCase(unittest.TestCase):
    def test_connection(self):
        """Test for app.connectors.MongoDBConnection.connect"""
        configs = config()
        db = MongoDBConnection.connect(configs)
        new_collection = 'testcollection'

        try:
            db.create_collection(new_collection)
        except:
            self.assertTrue(False, msg="Can't create collection.")

        try:
            db[new_collection].insert({'message': "Test message"})
        except:
            self.assertTrue(False, msg="Can't insert records to collection.")

        if not db[new_collection].find_one({'message': "Test message"}):
            self.assertTrue(False, msg="Can't find inserted record.")

        try:
            db.drop_collection(new_collection)
        except:
            self.assertTrue(False, msg="Can't drop collection.")


class LogEntryModelTestCase(unittest.TestCase):
    """Tests for app.models.LogEntry"""
    def test_create_instance(self):
        """Test for app.models.LogEntry.__init__"""
        level = 'test level'
        owner = 'test owner'
        data = 'test data'
        tags = 'test tags'
        logentry = LogEntry(level, owner, data, tags)
        self.assertTrue(logentry.level == level and
                        logentry.owner == owner and
                        logentry.data == data and
                        logentry.tags == tags,
                        msg="Can't create or check some field in LogEntry constructor.")

    def test_insert_into_db(self):
        """Test for app.models.LogEntry.save"""
        logentry = LogEntry('test level', 'test owner', 'test data', 'test tags')
        logentry_id = logentry.save()
        configs = config()
        db = MongoDBConnection.connect(configs)
        collection = unicode(configs['mongo']['collection'])
        logentry_from_db = db[collection].find_one({'_id': ObjectId(logentry_id)})
        db[collection].remove({'_id': ObjectId(logentry_id)})
        self.assertTrue(logentry_from_db['level'] == 'test level' and
                        logentry_from_db['owner'] == 'test owner' and
                        logentry_from_db['data'] == 'test data' and
                        logentry_from_db['tags'] == 'test tags',
                        msg="New entry does not match the expected or does not exist.")


class GetLevelsListViewTestCase(unittest.TestCase):
    def test_get_levels_list(self):
        """Test for app.views.get_levels_list"""
        with app.test_request_context():
            self.assertTrue('level' in json.loads(get_levels_list().data),
                            msg="Can't get levels list.")


class IndexViewTestCase(unittest.TestCase):
    def test_main_api_page(self):
        """Test for app.views.index"""
        with app.test_request_context():
            server_info = dict(json.loads(index().data))
            self.assertTrue('name' in server_info and
                            'type' in server_info and
                            'status' in server_info and
                            'version' in server_info and
                            server_info['version'] == VERSION,
                            msg="Can't get basic server info.")


class AddLogEntryViewTestCase(unittest.TestCase):
    def test_add_logentry(self):
        """Test for app.views.add_logentry"""
        with app.test_client() as logentry_view:
            data = {'level': 'info',
                    'owner': 'test owner',
                    'data': 'test data',
                    'tags': ['tag1', 'tag2']}
            json_data = json.dumps(data)
            response = logentry_view.post('/api/entry/', content_type='application/json', data=json_data)
            resp = json.loads(response.data)

            configs = config()
            db = MongoDBConnection.connect(configs)
            collection = unicode(configs['mongo']['collection'])
            entry_from_db = db[collection].find_one({'_id': ObjectId(resp['id'])})
            db[collection].remove({'_id': ObjectId(resp['id'])})

            self.assertTrue('OK' in resp and
                            resp['OK'] and
                            entry_from_db['level'] == 'info' and
                            entry_from_db['owner'] == 'test owner' and
                            entry_from_db['data'] == 'test data' and
                            entry_from_db['tags'] == ['tag1', 'tag2'],
                            msg="Server response is not the same as entry in DB.")




