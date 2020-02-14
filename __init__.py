from .challenge_events import challenges
from .hint_events import hints


def load(app):
    challenges()
    hints()
