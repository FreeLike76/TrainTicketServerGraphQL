import requests
import pandas as pd


class Provider2Worker:
    def __init__(self):
        self.endpoint_trips = "http://127.0.0.1:8082/trips"
        self.endpoint_tickets = "http://127.0.0.1:8082/tickets/"

    def get_all(self):
        response = requests.get(self.endpoint_trips)
        df_trips = pd.DataFrame(response.json(), dtype=str)
        df_tickets = pd.DataFrame(columns=["trip_id", "seat_type", "seat_num"], dtype=str)
        for trip_i, trip_row in df_trips.iterrows():
            response = requests.get(self.endpoint_tickets + trip_row["id"])
            df_tickets = df_tickets.append(pd.DataFrame(response.json(), dtype=str), ignore_index=True)

        temp = self.merge(df_trips, df_tickets)
        # add mark
        temp["provider_id"] = ["2" for x in range(len(temp))]
        return temp

    def get_by(self, args):
        # get trips table
        response = requests.get(self.endpoint_trips)
        df_trips = pd.DataFrame(response.json(), dtype=str)

        # filter trips
        for key, value in args.items():
            if key in df_trips.columns and key != "id":
                df_trips = df_trips[df_trips[key] == value]

        # for every trip get tickets
        df_tickets = pd.DataFrame(columns=["trip_id", "seat_type", "seat_num"], dtype=str)
        for trip_i, trip_row in df_trips.iterrows():
            response = requests.get(self.endpoint_tickets + trip_row["id"])
            df_tickets = df_tickets.append(pd.DataFrame(response.json(), dtype=str), ignore_index=True)

        # return merged
        temp = self.merge(df_trips, df_tickets)
        # add mark
        temp["provider_id"] = ["2" for x in range(len(temp))]

        # filter tickets
        for key, value in args.items():
            if key in temp.columns:
                temp = temp[temp[key] == value]

        return temp

    def merge(self, df_trips, df_tickets):
        temp = df_trips.merge(df_tickets, how="left", left_on="id", right_on="trip_id", suffixes=("_", ""))

        temp["cost"] = ["" for x in range(len(temp))]
        for i, row in temp.iterrows():
            if row["seat_type"] == "1":
                temp.at[i, "cost"] = row["seat_type_1_price"]
            elif row["seat_type"] == "2":
                temp.at[i, "cost"] = row["seat_type_2_price"]
            elif row["seat_type"] == "3":
                temp.at[i, "cost"] = row["seat_type_3_price"]
        # drop columns
        for column in ["id_", "seat_type_1_price", "seat_type_2_price", "seat_type_3_price"]:
            if column in temp.columns:
                temp = temp.drop(column, axis=1)
        return temp
