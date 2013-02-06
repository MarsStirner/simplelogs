from helpers import url

url('/api/', 'views.index', methods=["GET",])
url('/api/level/', 'views.get_levels_list', methods=["GET",])
url('/api/entry/', 'views.add_logentry', methods=["POST",])