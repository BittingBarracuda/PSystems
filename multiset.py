import numpy as np

class Multiset:
    def __init__(self, input = None):
        if type(input) == dict:
            # Check if keys are strings and values are integers
            if (not all([type(x) == int for x in input.values()])) or (not all([type(x) == str for x in input.keys()])):
                raise ValueError("Values in the dictionary must be integers and Keys must be Strings")
            self.multiset = {k:v for (k, v) in input.items() if v > 0}
        elif type(input) == str:
            self.multiset = {}
            for char in input:
                self.multiset[char] = self.multiset.get(char, 0) + 1
        elif isinstance(input, Multiset):
            self.multiset = input.multiset.copy()
        elif input == None:
            self.multiset = dict()
        else:
            raise TypeError("Input must be: String, Dictionary or Multiset!")
    
    ############################# PRIVATE METHODS #############################

    @staticmethod
    def __get_all_keys(m1, m2):
        return set(m1.multiset.keys() + m2.multiset.keys())

    @staticmethod
    def __get_intersect_keys(m1, m2):
        return set([key for key in m1.multiset.keys() if key in m2.multiset.keys()])

    ############################ PUBLIC METHODS ################################

    def __repr__(self):
        res = ""
        for key in self.multiset.keys():
            res += res + (key * self.multiset[key])
        return res
    
    ########################### OPERATIONS WITH MULTISETS (INSTANCE METHODS) #######################

    def __add__(self, m1):
        keys = Multiset.__get_all_keys(self, m1)
        res = {key : (self.multiset.get(key, 0) + m1.multiset.get(key, 0)) for key in keys}
        return Multiset(res)

    def __sub__(self, m1):
        keys = Multiset.__get_all_keys(self, m1)
        res = {key : max(self.multiset.get(key, 0) - m1.multiset.get(key, 0), 0) for key in keys}
        return Multiset(res)
    
    def __mul__(self, other):
        if type(other) != int:
            raise TypeError("Multisets can only be multiplied by an integer!")
        res = {key: other * self.multiset[key] for key in self.multiset.keys()}
        return Multiset(res)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def union(self, m1):
        keys = Multiset.__get_all_keys(self, m1)
        res = {key: max(self.multiset.get(key, 0), m1.multiset.get(key, 0)) for key in keys}
        return Multiset(res)

    def intersection(self, m1):
        keys = Multiset.__get_all_keys(self, m1)
        res = {key: min(self.multiset.get(key, 0), m1.multiset.get(key, 0)) for key in keys}
        return Multiset(res)
    
    def included(self, m1):
        keys = Multiset.__get_intersect_keys(self, m1)
        return all([self.multiset[key] <= m1.multiset[key] for key in keys])
    
    def support(self):
        return self.multiset.keys()
    
    def cardinality(self):
        return sum(self.multiset.values())
    
    def compute_np_vector(self, m1):
        return np.array([self.multiset.get(key, np.nan) for key in m1.multiset.keys()])
    
    def keys(self):
        return self.multiset.keys()
    
    def get(self, default = None):
        return self.multiset.get(self, default)
    
    ############################## OPERATIONS WITH MULTISETS (STATIC METHODS) ###########################

    @staticmethod
    def union(m1, m2):
        keys = Multiset.__get_all_keys(m1, m2)
        res = {key: max(m1.multiset.get(key, 0), m2.multiset.get(key, 0)) for key in keys}
        return Multiset(res)
    
    @staticmethod
    def intersection(m1, m2):
        keys = Multiset.__get_all_keys(m1, m2)
        res = {key: min(m1.multiset.get(key, 0), m2.multiset.get(key, 0)) for key in keys}
        return Multiset(res)
    
    @staticmethod
    def included(m1, m2):
        keys = Multiset.__get_intersect_keys(m1, m2)
        return all([m1.multiset[key] <= m2.multiset[key] for key in keys])

    @staticmethod
    def how_many_times_included(m1, m2):
        if Multiset.included(m1, m2):
            res = 1
            temp = m2 - m1
            while(Multiset.included(m1, temp)):
                res += 1
                temp = temp - m1
            return res
        else:
            return 0
    
    @staticmethod
    def support(m1):
        return m1.multiset.keys()
    
    @staticmethod
    def cardinality(m1):
        return sum(m1.multiset.values())
    
    @staticmethod 
    def compute_np_vector(m1, m2):
        return np.array(m1.multiset.get(key, np.nan) for key in m2.multiset.keys())
    
class MultisetDestiation(Multiset):
    def __init__(self, input = None, destinations = None):
        super().__init__(self, input)
        
