"""
Create singleton class to check if there is only one instance of the class
"""

class Singleton:
    __instance = None
    def __new__(cls):
        if Singleton.__instance == None:
            Singleton.__instance = object.__new__(cls)
        return Singleton.__instance

    @classmethod
    def getInstance(cls):
        return cls()

# Example usage
if __name__ == "__main__":

    s1 = Singleton()
    s2 = Singleton()
    print(s1 == s2) # True