import graphene


class Ticket(graphene.ObjectType):
    id = graphene.String()
    date = graphene.String()
    time = graphene.String()
    from_city = graphene.String()
    to_city = graphene.String()
    travel_time = graphene.String()
    seat_type = graphene.String()
    seat_num = graphene.String()
    cost = graphene.String()
    trip_id = graphene.String()
    provider_id = graphene.String()


class UserInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    card = graphene.String(required=True)
