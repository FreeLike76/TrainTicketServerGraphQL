import pandas as pd
from train_ticket_system.db_system.db_singleton import SingletonDB
from train_ticket_system.db_system.query_builder import QueryBuilder


class DBWorker:
    def __init__(self):
        self.query_builder = QueryBuilder()
        SingletonDB()

    def get_all(self):
        # query select preset
        self.query_builder.query_select()

        temp = pd.read_sql(self.query_builder.get_query(),
                           SingletonDB().conn)
        temp = temp.applymap(str)
        temp["provider_id"] = "0"
        return temp

    def get_by(self, args):
        # query select preset
        self.query_builder.query_select()

        # add args
        for key, value in args.items():
            self.query_builder.add_where_arg(key, value)

        # do sql
        temp = pd.read_sql(self.query_builder.get_query(),
                           SingletonDB().conn)
        # to str
        temp = temp.applymap(str)
        temp["provider_id"] = "0"
        return temp

    def set_status(self, ticket_id, ticket_status):
        self.query_builder.query_update("[status]", ticket_status)
        self.query_builder.add_where_arg("[id]", ticket_id)
        SingletonDB().conn.cursor().execute(self.query_builder.get_query())

    def delete_ticket(self, ticket_id):
        self.query_builder.query_delete()
        self.query_builder.add_where_arg("[id]", ticket_id)
        SingletonDB().conn.cursor().execute(self.query_builder.get_query())

    def insert_ticket(self, trip_id, seat_type, seat_num):
        self.query_builder.query_insert(trip_id, seat_type, seat_num)
        SingletonDB().conn.cursor().execute(self.query_builder.get_query())
