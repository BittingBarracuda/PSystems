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
        # The rules of each membrane generate "blocks", the first block contains the rules with the higher
        # level of priority, and so on.
        self.__rule_blocks_shape = self.__rule_blocks()
        # We create a matrix of rules with the same shape of self.__rule_blocks_shape
        self.__rules_matrix = self.__compute_rule_matrix()
        # Matrix that contains the number of objects that each rule uses. If an object is not present
        # in the LHS of a rule, that number gets set to 0.
        self.__rules_np = np.array([rule.get(key, 0) for rule in self.rules for key in self.contents.keys()])
        # Matrix that contains a replicated array with the contents present in the membrane. If an object
        # of the universe is not present in the membrane, then it's number gets set to 0. This matrix needs
        # to be computed at each step.
        self.__np_matrix = self.__compute_np_matrix
        #self.__num_applications = np.zeros(shape = (len(self.rules, )))
    
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

    def __compute_np_matrix(self):
        return np.tile(np.array([self.contents.get(key, 0) for key in self.universe]), (len(self.rules), 1))

    def __compute_application(self):
        # We iterate over the rule blocks
        i = 0
        for block in self.__rules_np:
            keep_block = True
            while keep_block:
                # For each block we select a rule using certain algorithm
                rule_index, rule_to_apply = algorithms.random_selection(block)
                # We "apply" the rule saving an auxiliary matrix
                aux = self.__np_matrix - rule_to_apply
                # Checking if the rule can be applied. If any value gets below 0 
                # then the rule cannot be applied
                if np.all(aux[rule_index] >= 0):
                    self.__np_matrix = self.__np_matrix - rule_to_apply
                    self.__apply_rule(self.__rules_matrix[i][rule_index])
                # Checking if we can still apply some rule in the current block. In case that it's not possible
                # then we skip to the next block
                if not np.any(np.array([self.__is_applicable(rule) for rule in self.__rules_matrix[i]])):
                    keep_block = False
                    i += 1
              
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
        pass




    