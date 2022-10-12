from multiset import Multiset, MultisetDestination
import algorithms
import numpy as np
from itertools import compress, chain

class Membrane:
    def __init__(self, id, contents, rules, parent = None, adjacents = []):
        # ID identifing the Membrane
        self.id = id
        # Dictionary with the contents of the membrane
        self.contents = contents
        # Rules sorted by their priority value
        self.rules = Membrane.__sort_rules_by_priority(rules)
        # Reference to its parent object. If the membrane is the root membrane then parent = None
        self.parent = parent
        # List of references to the membranes contained in the current membrane
        self.adjacents = adjacents
        # "Universe" of objects, meaning objects present in the LHS of the rules
        aux = list(chain.from_iterable([list(rule.lhs.keys()) for rule in self.rules]))
        self.universe = list(set(aux))
        # New contents is just a multiset that stores the new objects generated in each computation step
        # At the end of each step, these contents get dumped in self.contents
        self.__new_contents = Multiset()
        # Shape of the rules by block. The first block contains the rules with higher priority, and so on
        self.__rule_blocks_shape = self.__rule_blocks()
        self.__rule_blocks = self.__compute_rule_matrix()
        # Numpy array with the amount of each object in the membrane's contents. This array needs to be updated
        # after the application of each rule.
        self.__np_contents = np.array([self.contents.get(obj, -np.inf) for obj in self.universe])
        # List of numpy matrices that contain de number of objects that each rule uses.
        self.__np_rule_matrix = self.__get_np_rule_matrix()

        
    
    ################# PRIVATE METHODS ###################
    
    def __get_adjacent_ids(self):
        return [mem.id for mem in self.adjacents]
    
    def __get_applicable_rules(self):
        return [(rule, Multiset.how_many_times_included(rule, self.contents)) for rule in self.rules]
    
    def __is_applicable(self, rule):
        return Multiset.included(rule.lhs, self.contents)
    
    def __compute_rule_matrix(self):
        matrix, k = [], 0
        for i in range(self.__rule_blocks_shape[0]):
            matrix.append([])
            for j in range(self.__rule_blocks_shape[1]):
                matrix[i].append(self.rules[k])
                k += 1
        return matrix
    
    def __rule_blocks(self):
        priority_list = [x.priority for x in self.rules]
        current_priority = priority_list[0]
        temp_array = [[0]]
        for i in range(1, len(priority_list)):
            if priority_list[i] != current_priority:
                current_priority = priority_list[i]
                temp_array.append([])
            temp_array[-1].append(0)
        return np.array(temp_array).shape
    
    def __get_np_rule_matrix(self):
        matrix = []
        for rule_block in self.__rule_blocks:
            aux_arr = []
            for rule in rule_block:
                aux_arr.append(np.array([rule.lhs.get(obj, -np.inf) for obj in self.universe]))
            matrix.append(np.row_stack(tuple((arr for arr in aux_arr))))
        return matrix

    def __compute_step(self):
        print(f'Contents in {self.id}: {self.contents}')
        # Iterate over blocks of rules
        for rule_block in self.__rule_blocks:
            # Get only the applicable rules in the current block
            filter_applicable = [self.__is_applicable(rule) for rule in rule_block]
            rule_block_f = list(compress(rule_block, filter_applicable))
            keep_block = any(filter_applicable)
            while keep_block:
                # Select the rule to apply using some algorithm from algorithms.py
                _, rule_to_apply = algorithms.random_selection(rule_block_f)
                # Create an auxiliary array that simulates the application of the rule
                self.__apply_rule(rule_to_apply)
                # Check if we can keep applying some rule of the current block. In case that we don't
                # we skip to the next block
                filter_applicable = [self.__is_applicable(rule) for rule in rule_block_f]
                rule_block_f = list(compress(rule_block_f, filter_applicable))
                keep_block = any(filter_applicable)

    def __dump_contents(self, cont):
        self.__new_contents = self.__new_contents + cont

    def __apply_rule(self, rule):
        self.contents = self.contents - rule.lhs
        self.__new_contents = self.__new_contents + rule.rhs
        if type(rule.rhs) == MultisetDestination:
            adj_ids = self.__get_adjacent_ids()
            for (obj, elem) in rule.rhs.destinations.items():
                destination = elem[1]
                if destination == "out":
                    if self.parent != None:
                        self.parent.__dump_contents(Multiset({obj:elem[0]}))
                else:
                    try:
                        index = adj_ids.index(destination)
                        self.adjacents[index].__dump_contents(Multiset({obj:elem[0]}))
                    except ValueError:
                        pass
    
    #def __apply_rule(self, rule, amount):
    #    self.contents = self.contents - (amount * rule.lhs)
    #    self.__new_contents = self.__new_contents + (amount * rule.rhs)
    
    def __add_new_contents(self):
        self.contents = self.contents + self.__new_contents
        self.__new_contents = Multiset()
    
    @staticmethod
    def __sort_rules_by_priority(rule_list):
        return sorted(rule_list, key = lambda x: x.priority)
    
    #################### PUBLIC METHODS #########################

    def compute_step(self):
        bool_ret = any([self.__is_applicable(rule) for rule in self.rules])
        self.__compute_step()
        self.__add_new_contents()
        return bool_ret




    