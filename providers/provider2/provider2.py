import pandas as pd
from flask import Flask
from flask_restful import Resource, Api

df_trips = pd.read_csv("data/trips.csv", dtype=str)
df_tickets = pd.read_csv("data/tickets.csv", dtype=str)


class Provider2TripResources(Resource):
    def get(self):
        return df_trips.to_dict(orient="records")


class Provider2TicketResources(Resource):
    def get(self, trip_id):
        temp = df_tickets[df_tickets["trip_id"] == str(trip_id)]
        return temp.to_dict(orient="records")


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Provider2TripResources, "/trips")
    api.add_resource(Provider2TicketResources, "/tickets/<int:trip_id>")
    app.run(port=8082, debug=True)
