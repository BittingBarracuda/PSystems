from multiset import Multiset

class Rule:
    def __init__(self, lhs, rhs, priority):
        self.lhs = lhs
        self.rhs = rhs
        self.priority = priority
    