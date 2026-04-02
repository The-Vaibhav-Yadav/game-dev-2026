class Pickup:
    def __init__(self, gx, gy, pickup_type):
        self.gx = gx
        self.gy = gy
        self.pickup_type = pickup_type  # "coin" or "key"
        self.collected = False
        self.anim_timer = 0.0

    def update(self, dt):
        self.anim_timer += dt
