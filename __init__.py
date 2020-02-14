from CTFd.plugins.more_events.challenge_events import challenges
from CTFd.plugins.more_events.hint_events import hints


def load(app):
    challenges()
    hints()
