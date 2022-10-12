from multiset import Multiset
import algorithms
import numpy as np

class Membrane:
    def __init__(self, id, contents, rules, parent = None):
        # ID identifing the Membrane
        self.id = id
        # Dictionary with the contents of the membrane
        self.contents = contents
        # Rules sorted by their priority value
        self.rules = Membrane.__sort_rules_by_priority(rules)
        # Reference to its parent object. If the membrane is the root membrane then parent = None
        self.parent = parent
        # "Universe" of objects, meaning objects present in the LHS of the rules
        self.universe = list(set([rule.lhs.keys() for rule in self.rules]))
        # New contents is just a multiset that stores the new objects generated in each computation step
        # At the end of each step, these contents get dumped in self.contents
        self.__new_contents = Multiset()
        # Shape of the rules by block. The first block contains the rules with higher priority, and so on
        self.__rule_blocks_shape = self.__rule_blocks()
        self.__rule_blocks = self.__compute_rule_matrix()
        # Numpy array with the amount of each object in the membrane's contents. This array needs to be updated
        # after the application of each rule.
        self.__np_contents = np.array([self.contents.get(obj, -np.inf) for obj in self.universe.keys()])
        # List of numpy matrices that contain de number of objects that each rule uses.
        self.__np_rule_matrix = self.__get_np_rule_matrix()

        
    
    ################# PRIVATE METHODS ###################
    
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
            if priority_list[i].priority != current_priority:
                current_priority = priority_list[i].priority
                temp_array.append([])
            temp_array[-1].append(0)
        return np.array(temp_array).shape
    
    def __get_np_rule_matrix(self):
        matrix = []
        for rule_block in self.__rule_blocks:
            aux_arr = []
            for rule in rule_block:
                aux_arr.append(np.array([rule.lhs.get(obj, -np.inf) for obj in self.universe.keys()]))
            matrix.append(np.row_stack((arr for arr in aux_arr)))
        return matrix

    def __compute_step(self):
        # Iterate over blocks of rules
        for rule_block, matrix in zip(self.__rule_blocks, self.__np_rule_matrix):
            keep_block = True
            while keep_block:
                # Select the rule to apply using some algorithm from algorithms.py
                rule_index, rule_to_apply = algorithms.random_selection(rule_block)
                # Obtain de numpy array of that rule
                np_rule = matrix[rule_index, :]
                # Create an auxiliary array that simulates the application of the rule
                aux_arr = self.__np_contents - np_rule
                aux_arr[aux_arr == np.nan] = np.inf
                # If all the elements of auxiliary array are non-negative, then the rule can be applied
                if np.all(aux_arr >= 0):
                    self.__np_contents = self.__np_contents - np_rule
                    self.__apply_rule(rule_to_apply)
                # Check if we can keep applying some rule of the current block. In case that we don't
                # we skip to the next block
                if not any([self.__is_applicable(rule) for rule in rule_block]):
                    keep_block = False

    def __apply_rule(self, rule):
        self.contents = self.contents - rule.lhs
        self.__new_contents = self.__new_contents + rule.rhs
    
    def __apply_rule(self, rule, amount):
        self.contents = self.contents - (amount * rule.lhs)
        self.__new_contents = self.__new_contents + (amount * rule.rhs)
    
    def __add_new_contents(self):
        self.contents = self.contents + self.__new_contents
        self.__new_contents = Multiset()
    
    @staticmethod
    def __sort_rules_by_priority(rule_list):
        return sorted(rule_list, key = lambda x: x.priority)
    
    #################### PUBLIC METHODS #########################

    def compute_step(self):
        self.__compute_step()
        self.__add_new_contents()




    