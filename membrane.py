from multiset import Multiset
import numpy as np

class Membrane:
    def __init__(self, id, contents, rules, parent = None):
        self.id = id
        self.contents = contents
        self.rules = Membrane.__sort_rules_by_priority(rules)
        self.parent = parent
        self.universe = list(set([rule.lhs.keys() for rule in self.rules]))
        self.app_matrix = np.zeros(shape = (len(self.rules), len(self.universe)))
        #self.rule_cardinality = np.array([Multiset.cardinality(rule.lhs) for rule in self.rules])
    
    ################# PRIVATE METHODS ###################

    def __clear_matrix(self):
        self.app_matrix = np.zeros(shape = (len(self.rules), len(self.universe)))

    def __get_applicable_rules(self):
        return [(rule, Multiset.how_many_times_included(rule, self.contents)) for rule in self.rules]
    
    def __is_applicable(self, rule):
        return Multiset.included(rule.lhs, self.contents)

    def __apply_rule(self, rule):
        self.contents = (self.contents - rule.lhs) + rule.rhs
    
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
    
    ################# PUBLIC METHODS ####################

    #def compute_step(self):
    #    rule_blocks = self.__get_rule_blocks()
    #    while len(rule_blocks) > 0:




    