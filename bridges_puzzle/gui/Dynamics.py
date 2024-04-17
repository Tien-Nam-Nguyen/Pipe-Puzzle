from math import pi


class DynamicsConfig:
    def __init__(self, response=1, dampen=1, eager=1):
        self.response = response
        self.dampen = dampen
        self.eager = eager


class Dynamics:
    def __init__(self, xi: float, config: DynamicsConfig):
        self.k1 = self.calc_k1(config)
        self.k2 = self.calc_k2(config)
        self.k3 = self.calc_k3(config)

        self.xp = xi
        self.y = xi
        self.yd: float = 0

    def get_interpolated(self, delta_time: float, target: float, change: float = None):
        if change is None:
            change = (target - self.xp) / delta_time
            self.xp = target

        stable_k2 = max(
            self.k2,
            (delta_time * delta_time) / 2 + (delta_time * self.k1) / 2,
            delta_time * self.k1,
        )

        self.y += delta_time * self.yd

        self.yd += (
            delta_time * (target + self.k3 * change - self.y - self.k1 * self.yd)
        ) / stable_k2

        return self.y

    def config(self, config: DynamicsConfig):
        self.k1 = self.calc_k1(config)
        self.k2 = self.calc_k2(config)
        self.k3 = self.calc_k3(config)

    def reset(self, xi: float):
        self.xp = xi
        self.y = xi
        self.yd = 0

    @staticmethod
    def calc_k1(config: DynamicsConfig):
        return config.dampen / (pi * config.response)

    @staticmethod
    def calc_k2(config: DynamicsConfig):
        return 1 / (2 * pi * config.response * (2 * pi * config.response))

    @staticmethod
    def calc_k3(config: DynamicsConfig):
        return (config.eager * config.dampen) / (2 * pi * config.response)
