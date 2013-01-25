from helpers import url

url('/', 'views.index', methods=["GET",])
url('/api/entry/', 'views.new_entry', methods=["POST",])