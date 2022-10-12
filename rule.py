from multiset import Multiset

class Rule:
    def __init__(self, lhs, rhs, priority, dissolve = False):
        self.lhs = lhs
        self.rhs = rhs
        self.priority = priority
        self.dissolve = dissolve
    