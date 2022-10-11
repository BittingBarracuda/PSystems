import random

def random_selection(rule_list):
    index = random.choice(range(len(rule_list)))
    return index, rule_list[index]