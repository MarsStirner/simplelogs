# coding: utf-8
import math

from flask import request, render_template, session, abort, redirect
from flask_login import current_user

from simplelogs.systemwide import app, cas
from simplelogs.admin.app import module
from simplelogs.admin.auth import create_user_session, destroy_user_session
from simplelogs.app.models import LogEntry

from hitsl_utils.api import api_method
from hitsl_utils.safe import safe_int, parse_json


@module.before_request
def check_auth():
    if current_user.is_anonymous:
        if 'cas_user_id' not in session:
            raise abort(401, 'cannot find `cas_user_id` in session')
        create_user_session(session['cas_user_id'])

    if not current_user.is_admin():
        raise abort(403)


@app.route('/logout/')
@cas.public
def logout():
    destroy_user_session()
    response = redirect(request.args.get('next') or '/')
    token = request.cookies.get(app.config['CASTIEL_AUTH_TOKEN'])
    if token:
        response.delete_cookie(app.config['CASTIEL_AUTH_TOKEN'])
    if 'BEAKER_SESSION' in app.config:
        response.delete_cookie(app.config['BEAKER_SESSION'].get('session.key'))
    return response


@module.route('/')
def jounal_view():
    return render_template('admin/journal_view.html')


@module.route('/api/0/log_entries')
@api_method
def api_0_get_log_entries():
    args = request.args.to_dict()

    sort = args.get('sort')
    limit = safe_int(args.get('limit'))
    skip = safe_int(args.get('skip'))

    flt = parse_json(args.get('flt', {}))
    find = dict()
    for key, value in flt.iteritems():
        if key in ('level', 'owner', 'datetimestamp', 'tags', 'start', 'end', 'data'):
            find[key] = value
    entry = LogEntry()
    result = []
    for res in entry.get_entries(find=find, sort=sort, skip=skip, limit=limit):
        res['_id'] = str(res['_id'])
        result.append(res)

    total = entry.count(find)
    num_of_pages = int(math.ceil(total / float(limit)))
    return {
        'total_pages': num_of_pages,
        'count': total,
        'items': result
    }