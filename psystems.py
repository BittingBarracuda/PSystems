from membrane import Membrane
from multiset import Multiset
from rule import Rule
import numpy as np

class PSystem:
    pass


if __name__ == "__main__":
    rules1 = [Rule(Multiset({"a":1}), Multiset({"b":1}), 1.0), 
            Rule(Multiset({"b":1}), Multiset({"b":1}), 1.0, destinations = 2),
            Rule(Multiset({"b":1}), Multiset({"b":1}), 1.0, destination = "out")]
    rules2 = [Rule(Multiset({"b":1}), Multiset({"c":1}), 1.0, destinations = "out")]
    membrane1 = Membrane(1, Multiset({"a":1}), rules1)
    membrane2 = Membrane(2, Multiset(), rules2, membrane1)
