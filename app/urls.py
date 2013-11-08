from helpers import url

url('/api/', 'views.index', methods=["GET", ])  # main, status page
url('/api/level/', 'views.get_levels_list', methods=["GET", ])  # returns levels list
url('/api/entry/', 'views.add_logentry', methods=["POST", ]) # creating new log entry in DB