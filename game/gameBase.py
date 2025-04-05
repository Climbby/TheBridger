class GameBase:
    def __init__(self, state=None, **kwargs):
        super().__init__(**kwargs)
        self.state = state