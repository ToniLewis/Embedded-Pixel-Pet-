class PowerManager:
    """
    Simulated power management for the Pixel Pet device.

    - Tracks a simple battery level.
    - Supports a low-power sleep mode flag.
    - Lets other modules query battery and mode state.
    """

    def __init__(self):
        self.battery_level = 100.0      # percentage
        self.low_power_mode = False

    def update(self):
        """
        Called every frame/tick to model battery drain.
        """
        # Simple fake drain rate: slower in low power mode.
        drain_rate = 0.01 if self.low_power_mode else 0.05
        self.battery_level = max(0.0, self.battery_level - drain_rate)

    def enter_low_power(self):
        """
        Put the system into a low power mode (sleep).
        """
        self.low_power_mode = True

    def exit_low_power(self):
        """
        Resume normal power mode.
        """
        self.low_power_mode = False

    def is_low_battery(self) -> bool:
        """
        For cute notifications like:
        \"I'm getting sleepy... 🌙\"
        """
        return self.battery_level < 20.0