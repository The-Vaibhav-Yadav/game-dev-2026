class BaseState:
    def __init__(self, game_state, assets, audio):
        self.game_state = game_state
        self.assets = assets
        self.audio = audio

    def enter(self):
        """Called once when we transition INTO this state."""
        pass

    def exit(self):
        """Called once when we transition OUT of this state."""
        pass

    def update(self, dt, events):
        """Called every frame. Returns None to stay, or a state name string to transition.
        dt = time since last frame in seconds.
        events = list of pygame events this frame."""
        return None

    def draw(self, screen):
        """Called every frame after update. Draw everything."""
        pass
