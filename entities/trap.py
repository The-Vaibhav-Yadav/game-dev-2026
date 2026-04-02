from constants import SPIKE_CYCLE_TIME


class Trap:
    def __init__(self, gx, gy, trap_type):
        self.gx = gx
        self.gy = gy
        self.trap_type = trap_type  # "spike" or "tax_zone"
        self.timer = 0.0
        self.active = True  # for spikes: toggles on/off

    def update(self, dt):
        if self.trap_type == "spike":
            self.timer += dt
            cycle_pos = self.timer % SPIKE_CYCLE_TIME
            self.active = cycle_pos < (SPIKE_CYCLE_TIME / 2)
        # tax_zone is always active
