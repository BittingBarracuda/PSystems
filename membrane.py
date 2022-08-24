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
        self.__num_applications = np.zeros(shape = (len(self.rules, )))
        self.__rule_blocks_shape = self.__rule_blocks()
    
    ################# PRIVATE METHODS ###################
    
    def __compute_np_matrix(self):
        return np.array([Multiset.compute_np_vector(rule.lhs, self.universe) for rule in self.rules])

    def __get_applicable_rules(self):
        return [(rule, Multiset.how_many_times_included(rule, self.contents)) for rule in self.rules]
    
    def __is_applicable(self, rule):
        return Multiset.included(rule.lhs, self.contents)

    def __compute_num_applications(self):
        contents_vector = Multiset.compute_np_vector(self.contents, self.universe)
        aux = contents_vector // self.__np_matrix
        temp_matrix = np.where(aux == np.nan, np.inf, aux)
        self.__num_applications = np.min(temp_matrix, axis = 1).astype(int).reshape(self.__rule_blocks_shape)
    
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
    
    # def __get_rule_blocks(self):
    #     rules_priority = Membrane.__sort_rules_by_priority(self.__get_applicable_rules)
    #     if len(rules_priority) > 0:
    #         res = [[rules_priority[0]]]
    #         current_priority = rules_priority[0].priority
    #         for i in range(1, len(rules_priority)):
    #             current_rule = rules_priority[i]
    #             if current_rule.priority != current_priority:
    #                 res.append([])
    #             res[-1].append(current_rule)
    #         return res
    #     else:
    #         return []
    
    #################### PUBLIC METHODS #########################

    def compute_step(self):
        pass




    