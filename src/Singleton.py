"""
Implémentation du design pattern Singleton en Python.
Permet de rendre une classe "singleton" par simple héritage de celle-ci.

ref: https://deepnote.com/@rmi-ppin/Faie-un-singleton-en-python-0d187a73-2f24-4c49-b2aa-bbbf4a45ace6
"""


class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

