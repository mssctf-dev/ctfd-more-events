from CTFd.api.v1.hints import Hint, Hints, HintList, HintSchema, db
from flask import request, current_app


def hints():
    orig_post = HintList.post
    def new_post(self):
        ret = orig_post(self)
        current_app.events_manager.publish(
            data={
                'type': 'new_hint',
                'hint': Hint.get(
                    None, hint_id=ret['data']['id']
                )['data']
            },
            type='hint'
        )
        return ret
    HintList.post = new_post
