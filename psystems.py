from calendar import TUESDAY
from membrane import Membrane
from multiset import Multiset
from rule import Rule
import numpy as np

class PSystem:
    def __init__(self, root, membranes):
        self.root = root
        self.membranes = membranes
    
    def start(self):
        keep = True
        while keep:
            aux = []
            for membrane in self.membranes:
                aux.append(membrane.compute_step())
                print(membrane.contents)
            keep = any(aux)



if __name__ == "__main__":
    rules1 = [Rule(Multiset({"a":1}), Multiset({"b":1}), 1.0), 
            Rule(Multiset({"b":1}), Multiset({"b":1}), 1.0),
            Rule(Multiset({"b":1}), Multiset({"b":1}), 1.0)]
    rules2 = [Rule(Multiset({"b":1}), Multiset({"c":1}), 1.0)]
    membrane1 = Membrane(1, Multiset({"a":1}), rules1)
    membrane2 = Membrane(2, Multiset(), rules2, membrane1)
