from .module import NuzlockeModule


def initialize(event_pool, rules, secret):
    return NuzlockeModule(event_pool, rules, secret)
