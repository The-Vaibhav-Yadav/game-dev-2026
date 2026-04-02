import random


class Camera:
    def __init__(self):
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.shake_timer = 0.0
        self.shake_intensity = 0

    def trigger_shake(self, intensity=4, duration=0.15):
        self.shake_intensity = intensity
        self.shake_timer = duration

    def update(self, dt):
        if self.shake_timer > 0:
            self.shake_timer -= dt
            self.shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0
