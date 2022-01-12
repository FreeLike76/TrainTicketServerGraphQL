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

    def set_status(self, ticket_id, ticket_status):
        self.query_builder.query_update("[status]", ticket_status)
        self.query_builder.add_where_arg("[id]", ticket_id)
        SingletonDB().conn.cursor().execute(self.query_builder.get_query()).commit()

    def delete_ticket(self, ticket_id):
        self.query_builder.query_delete()
        self.query_builder.add_where_arg("[id]", ticket_id)
        SingletonDB().conn.cursor().execute(self.query_builder.get_query()).commit()

    def insert_ticket(self, trip_id, seat_type, seat_num):
        self.query_builder.query_insert(trip_id, seat_type, seat_num)
        SingletonDB().conn.cursor().execute(self.query_builder.get_query()).commit()

    def book_our_ticket(self, id, book_date, book_time, first_name, last_name, card):
        temp_query = """
update [Tickets]
set
[book_date] = '{}',
[book_time] = '{}',
[first_name] = '{}',
[last_name] = '{}',
[card] = '{}',
[status] = '2'
where [id] = '{}'
        """.format(book_date, book_time, first_name, last_name, card, id)
        print(temp_query)
        SingletonDB().conn.cursor().execute(temp_query).commit()

    def book_provider_ticket(self, id, provider_id, book_date, book_time, first_name, last_name, card):
        temp_query = """
insert into [SoldProviderTickets]
([id], [provider_id], [book_date], [book_time], [first_name], [last_name], [card])
values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(id, provider_id, book_date, book_time, first_name, last_name, card)
        print(temp_query)
        SingletonDB().conn.cursor().execute(temp_query).commit()

    def get_provider_sold(self):
        temp = pd.read_sql("select [id], [provider_id] from SoldProviderTickets",
                           SingletonDB().conn)
        temp = temp.applymap(str)
        return temp
