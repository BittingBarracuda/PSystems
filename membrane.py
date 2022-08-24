from multiset import Multiset
import numpy as np

class Membrane:
    def __init__(self, id, contents, rules, parent = None):
        self.id = id
        self.contents = contents
        self.rules = Membrane.__sort_rules_by_priority(rules)
        self.parent = parent
        self.universe = list(set([rule.lhs.keys() for rule in self.rules]))
        self.__new_contents = Multiset()
        self.__np_matrix = self.__compute_np_matrix()
        self.num_applications = np.zeros(shape = (len(self.rules, )))
    
    ################# PRIVATE METHODS ###################
    def __compute_np_matrix(self):
        return np.array([Multiset.compute_np_vector(rule.lhs, self.universe) for rule in self.rules])

    def __get_applicable_rules(self):
        return [(rule, Multiset.how_many_times_included(rule, self.contents)) for rule in self.rules]
    
    def __is_applicable(self, rule):
        return Multiset.included(rule.lhs, self.contents)

    # TODO: Implement a correct way of computing num_applications
    def __compute_num_applications(self):
        contents_vector = Multiset.compute_np_vector(self.contents, self.universe)
        temp_matrix = self.__np_matrix - contents_vector
        self.num_applications = np.min(temp_matrix, axis = 1)

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
    
    def __get_rule_blocks(self):
        rules_priority = Membrane.__sort_rules_by_priority(self.__get_applicable_rules)
        if len(rules_priority) > 0:
            res = [[rules_priority[0]]]
            current_priority = rules_priority[0].priority
            for i in range(1, len(rules_priority)):
                current_rule = rules_priority[i]
                if current_rule.priority != current_priority:
                    res.append([])
                res[-1].append(current_rule)
            return res
        else:
            return []
    
    #################### PUBLIC METHODS #########################

    def compute_step(self):
        pass




    