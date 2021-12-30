import pandas as pd
from flask import Flask, request
from flask_restful import Resource, Api

df = pd.read_csv("data/tickets.csv", dtype=str)


class Provider1Resource(Resource):
    def get(self):
        temp = df
        for key, value in request.args.items():
            if key in temp.columns:
                temp = temp[temp[key] == value]
        return temp.to_dict(orient="records")


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Provider1Resource, "/search")
    app.run(port=8081, debug=True)
