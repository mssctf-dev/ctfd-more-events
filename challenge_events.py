from flask import current_app, request
from CTFd.plugins.challenges import BaseChallenge
from CTFd.utils.user import get_current_team
from CTFd.utils.user import get_current_user

def get_current_user_json():
    user = get_current_user()
    if user:
        return {
            "id": user.id,
            "name": user.name,
            "hidden": user.hidden,
            "team": user.team_id
        }

def get_current_team_json():
    team = get_current_team()
    if team:
        return {
            "id": team.id,
            "name": team.name,
            "hidden": team.hidden
        }

def challenges():
    for c in BaseChallenge.__subclasses__():
        def wrap(func, data):
            def new_func(*args, **kwargs):
                ret = func(*args, **kwargs)
                current_app.events_manager.publish(data=eval(data), type='challenge')
                return ret
            return new_func
        
        c.create = wrap(c.create, '''
{
    "type": "challenge_create",
    "challenge": ret.id
}
''')
        c.update = wrap(c.update, '''
{
    "type": "challenge_update",
    "challenge": args[0].id if len(args)>=1 else kwargs["challenge"].id
}
''')
        c.solve = wrap(c.solve, '''
{
    "type": "challenge_solved",
    "challenge": (request.form or request.get_json())["challenge_id"],
    "user": get_current_user_json(),
    "team": get_current_team_json()
}
''')