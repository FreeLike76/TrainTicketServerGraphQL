import graphene
from train_ticket_system.graphql_objects import Ticket, UserInput
from train_ticket_system.tts_system import TrainTicketSystem

system = TrainTicketSystem()


class Query(graphene.ObjectType):
    get_tickets = graphene.List(Ticket,
                                id=graphene.String(),
                                provider_id=graphene.String(),
                                from_city=graphene.String(),
                                to_city=graphene.String(),
                                date=graphene.String())

    def resolve_get_tickets(self, info, **args):
        print(args)
        temp = system.get_all()
        for key, value in args.items():
            if key in temp.columns:
                temp = temp[temp[key] == value]
        return temp.to_dict(orient="records")


class DeleteTicket(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        system.delete_ticket(id)


class ChangeStatus(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        status = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id, status):
        system.set_status(id, status)


class InsertTicket(graphene.Mutation):
    class Arguments:
        trip_id = graphene.String(required=True)
        seat_type = graphene.String(required=True)
        seat_num = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, trip_id, seat_type, seat_num):
        system.insert_ticket(trip_id, seat_type, seat_num)


class BookTicket(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        provider_id = graphene.String(required=True)
        user_data = UserInput(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id, provider_id, user_data):
        system.book_ticket(id, provider_id, user_data.first_name, user_data.last_name, user_data.card)


class Mutation(graphene.ObjectType):
    delete_ticket = DeleteTicket.Field()
    change_status = ChangeStatus.Field()
    insert_ticket = InsertTicket.Field()
    book_ticket = BookTicket.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
