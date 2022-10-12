from membrane import Membrane
from multiset import Multiset, MultisetDestination
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
            Rule(Multiset({"b":1}), MultisetDestination(destinations = {"b":(1, 2)}), 1.0),
            Rule(Multiset({"b":1}), MultisetDestination(destinations = {"b":(1, "out")}), 1.0)]
    rules2 = [Rule(Multiset({"b":1}), MultisetDestination(destinations = {"c":(1, "out")}), 1.0)]
    membrane1 = Membrane(1, Multiset({"a":1}), rules1)
    membrane2 = Membrane(2, Multiset(), rules2, membrane1, adjacents = [1])
    psys = PSystem(membrane1, [membrane1, membrane2])
    psys.start()