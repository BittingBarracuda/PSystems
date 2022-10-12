from membrane import Membrane
from multiset import Multiset, MultisetDestination
from rule import Rule
import time

class PSystem:
    def __init__(self, root, membranes):
        self.root = root
        self.membranes = membranes
    
    def start(self, max_steps):
        keep, step = True, 1
        while keep and step <= max_steps:
            print(f'STEP {step}')
            step += 1
            aux = []
            for membrane in self.membranes:
                aux.append(membrane.compute_step())
            for membrane in self.membranes:
                membrane.add_new_contents()
            keep = any(aux)



if __name__ == "__main__":
    start_time = time.time()
    rules1 = [Rule(Multiset({"a":1}), Multiset({"b":1}), 1.0), 
            Rule(Multiset({"b":1}), MultisetDestination(destinations = {"b":(1, 2)}), 1.0),
            Rule(Multiset({"b":1}), MultisetDestination(destinations = {"b":(1, "out")}), 0.5)]
    rules2 = [Rule(Multiset({"b":1}), MultisetDestination(destinations = {"c":(1, "out")}), 1.0)]
    membrane2 = Membrane(2, Multiset(), rules2)
    membrane1 = Membrane(1, Multiset({"a":1}), rules1, adjacents = [membrane2])
    membrane2.set_parent(membrane1)
    psys = PSystem(membrane1, [membrane1, membrane2])
    max_steps = 100
    psys.start(max_steps = max_steps)
    print(f'Exectuion time = {time.time() - start_time}')