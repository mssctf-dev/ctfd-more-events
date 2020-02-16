from flask import current_app, request
from CTFd.utils.user import get_current_team
from CTFd.utils.user import get_current_user
from CTFd.api.v1.challenges import (
    ChallengeAttempt, ChallengeList, Challenge
)
from .wrapper import wrap


def challenges():
    def publish(data):
        current_app.events_manager.publish(
            data=data, type='challenge'
        )

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
    
    ChallengeAttempt.post = wrap(
        ChallengeAttempt.post,
        lambda ret: publish({
            "type": "challenge_solved",
            "challenge": (request.form or request.get_json())["challenge_id"],
            "user": get_current_user_json(),
            "team": get_current_team_json()
        }) if (ret['success'] == True) and
        (request.args.get("preview", False) == False) and
        (ret['data']['status'] == 'correct') else None
    )

    ChallengeList.post = wrap(
        ChallengeList.post,
        lambda ret: publish({
            "type": "challenge_created",
            "challenge": ret['data']['id']
        })
    )

    Challenge.patch = wrap(
        Challenge.patch,
        lambda ret: publish({
            "type": "challenge_updated",
            "challenge": ret['data']['id']
        })
    )
