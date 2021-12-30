from train_ticket_system.providers_system.p1_worker import Provider1Worker
from train_ticket_system.providers_system.p2_worker import Provider2Worker


class Facade:
    def __init__(self):
        self.p1 = Provider1Worker()
        self.p2 = Provider2Worker()

    def get_all(self):
        res1 = self.p1.get_all()
        res2 = self.p2.get_all()

        return res1.append(res2, ignore_index=True)

    def get_by(self, args):
        res1 = self.p1.get_by(args)
        res2 = self.p2.get_by(args)

        return res1.append(res2, ignore_index=True)
