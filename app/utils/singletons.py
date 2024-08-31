
"""
Create a singleton wrapper for a class. by using __new__ method.
"""
from typing import TypeVar, Type
T = TypeVar('T')
def singleton(wrapped_class: Type[T]) -> Type[T]:
    """
    A decorator to create a singleton wrapper for a class.



    :param cls: The class to be wrapped.
    :return: The singleton wrapper class.
    """
    setattr(wrapped_class, '_instance', None)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(wrapped_class, cls).__new__(cls)
        return cls._instance

    setattr(wrapped_class, '__new__', __new__)
    return wrapped_class