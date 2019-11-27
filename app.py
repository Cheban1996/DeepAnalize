from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from main import Task, AuditDB

app = Flask(__name__)
api = Api(app)


class Audits(Resource):
    def get(self):
        return jsonify({'data': Task.list_audit()})


class StartAudit(Resource):
    def post(self):
        url = request.json.get('url')
        audit = request.json.get('audit')

        if audit not in Task.list_audit():
            return {'message': 'audit not exist'}, 400

        result = Task(url=url, audit=audit).start_audit()
        return jsonify({'data': {'id': result}})


class History(Resource):
    def get(self):
        return {'data': [doc for doc in AuditDB().get_all_result()]}


api.add_resource(Audits, '/list_audit')
api.add_resource(StartAudit, '/start_audit')
api.add_resource(History, '/history')

if __name__ == '__main__':
    app.run(debug=True, port=5050)
