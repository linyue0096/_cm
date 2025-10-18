import math

class FiniteFieldElement:
    
    def __init__(self, field, value, prime):
        if not isinstance(value, int) or not isinstance(prime, int):
            raise TypeError("Value and prime must be integers.")
        if prime <= 1:
            raise ValueError("Prime must be greater than 1.")
        self.field = field
        self.prime = prime
        self.value = value % prime

    def __add__(self, a, b):
        if a.prime !=b.prime:
            raise ValueError("Cannot operate on numbers from different fields.")
        new_value = (a.value +b.value)% a.prime
        return FiniteFieldElement(self.field, new_value, a.prime)
    
    def __sub__(self, a, b):
        if a.prime !=b.prime:
            raise ValueError("Cannot operate on numbers from different fields.")
        new_value = (a.value - b.value)% self.field
        return FiniteFieldElement(new_value, self.field)
    
    def __mul__(self, a, b):
        if a.prime !=b.prime:
            raise ValueError("Cannot operate on numbers from different fields. ")
        new_value = (a.value - b.value)% self.field
        return FiniteFieldElement(new_value, self.field)
    
    def __neg__ (self, a):
        return FiniteFieldElement(self. field,(-a.value)%a.prime, a.prime)
    
    def __repr__(self):
        return f"{self.value} in {self.field}"
