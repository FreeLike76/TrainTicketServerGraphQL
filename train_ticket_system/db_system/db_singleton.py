import pyodbc


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonDB(metaclass=Singleton):
    def __init__(self):
        self.conn = pyodbc.connect("Driver={SQL Server};Server=DESKTOP-L5ATCHA;Database="
                                   + "TrainTickets"
                                   + ";Trusted_Connection=yes;")
