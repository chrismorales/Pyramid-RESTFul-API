from models import (
    Users,
    DBSession,
)

GROUPS = {
    'editor': ['group:editors']
}


def groupfinder(userid, request):
    USERS = DBSession.query(Users).filter_by(username=userid).first()
    if userid in USERS.username:
        return GROUPS.get(userid, [])
