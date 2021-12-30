from train_ticket_system.tts_system import TrainTicketSystem
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

server = TrainTicketSystem()



class TTSResource(Resource):
    def get(self):
        if len(request.args) == 0:
            return server.get_all().to_dict(orient="records")
        else:
            return server.get_by(request.args).to_dict(orient="records")

    def put(self):
        args = update_ticket_args.parse_args()
        try:
            server.set_status(args)
            return {"id": str(args["id"]), "status": args["status"]}
        except:
            print("Error", args)

    def delete(self):
        args = delete_ticket_args.parse_args()
        try:
            server.delete_ticket(args)
            return {"id": str(args["id"]), "status": "deleted"}
        except:
            print("Error", args)
            return {"status": "error"}

    def post(self):
        args = insert_ticket_args.parse_args()
        try:
            server.insert_ticket(args)
            return {"status": "inserted"}
        except:
            print("Error", args)
            return {"status": "error"}


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(TTSResource, "/tickets")
    app.run(port=8080, debug=False)
