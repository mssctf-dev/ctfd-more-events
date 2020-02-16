from CTFd.api.v1.hints import Hint, Hints, HintList, HintSchema, db
from flask import request, current_app
from .wrapper import wrap


def hints():
    def publish(data):
        current_app.events_manager.publish(
            data=data, type='hint'
        )

    HintList.post = wrap(
        HintList.post,
        lambda ret: publish({
            'type': 'hint_created',
            'hint': Hint.get(
                None, hint_id=ret['data']['id']
            )['data']
        })
    )

    Hint.patch = wrap(
        Hint.patch,
        lambda ret: publish({
            'type': 'hint_updated',
            'hint': Hint.get(
                None, hint_id=ret['data']['id']
            )['data']
        })
    )
