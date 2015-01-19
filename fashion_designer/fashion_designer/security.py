USERS = {
    'editor': 'editor',
    'viewer': 'viewer',
    'tr_h': 'tr_h'
}
GROUPS = {
    'editor': ['group:editors']
}


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
