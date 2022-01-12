import time
from datetime import date
from train_ticket_system.db_system.db_worker import DBWorker
from train_ticket_system.providers_system.providers_facade import Facade


class TrainTicketSystem:
    def __init__(self):
        self.providers = Facade()
        self.db = DBWorker()

    def get_all(self):
        start = time.time()
        db_res = self.db.get_all()
        print("get_all, db:", time.time() - start)

        start = time.time()
        res_providers = self.providers.get_all()
        print("get_all, providers:", time.time() - start)

        booked = self.db.get_provider_sold()
        for index, row in booked.iterrows():
            res_providers = res_providers[((res_providers["provider_id"] != row["provider_id"])
                                           | (res_providers["id"] != row["id"]))]

        return db_res.append(res_providers, ignore_index=True)

    def set_status(self, id, status):
        self.db.set_status(id, status)

    def delete_ticket(self, id):
        self.db.delete_ticket(id)

    def insert_ticket(self, trip_id, seat_type, seat_num):
        self.db.insert_ticket(trip_id, seat_type, seat_num)

    def book_ticket(self, id, provider_id, first_name, last_name, card):
        _date = date.today()
        _time = time.strftime("%H:%M:%S", time.localtime())
        if provider_id == "0":
            self.db.book_our_ticket(id, _date, _time, first_name, last_name, card)
        else:
            self.db.book_provider_ticket(id, provider_id, _date, _time, first_name, last_name, card)
