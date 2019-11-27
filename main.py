import os
import datetime
import importlib
import tarfile
from time import sleep
from io import BytesIO

import docker

from blessings import Terminal

from rq import Queue
from redis import Redis

from pymongo import MongoClient
from pymongo.collection import ObjectId

from primitives import validate_url

terminal = Terminal()


class Docker:
    def __init__(self):
        self.client = docker.from_env()

    def run(self, name_container: str, *args, detach=True, read_file=False,
            path_file=None, file=None):
        """
        :param name_container:
        :param args: params for of run container audit
        :param detach:
        :return: bool -> True if run success, False if run failed
        """
        try:
            container = self.client.run(name_container, *args, detach=detach)

            if read_file:
                sleep(5)
                file_json = container.get_archive(f'{path_file}/{file}')
                stream, stat = file_json
                file_obj = BytesIO()
                for i in stream:
                    file_obj.write(i)
                file_obj.seek(0)
                tar = tarfile.open(mode='r', fileobj=file_obj)
                text = tar.extractfile(f'{file}')
                res = text.read()
                return res.decode('utf-8')
        except Exception as error:
            print(error)


class DB:
    pass


class MongoDB(DB):
    def __init__(self, host='localhost', port=27017):
        self.client = MongoClient(host=host, port=port)
        self.db = self.client['DeepAnalyze']

    @staticmethod
    def init_object_id():
        return ObjectId()


class AuditDB(MongoDB):
    """ Collection audit"""

    def __init__(self):
        MongoDB.__init__(self)
        self.collection = self.db['audit']

    def get_all_result(self):
        """
        Method get document by id rq task
        :param id:
        :return:
        """
        return self.collection.find({}, {'_id': False})

    def add_result(self, _id, queue_id, audit, url):
        self.collection.insert_one({
            '_id': _id,
            'queue_id': queue_id,
            'audit': audit,
            'url': url
        })

    def update_result(self, object_id, data):
        self.collection.update_one({"_id": object_id},
                                   {"$set": data})


class Task:

    def __init__(self, url, audit):
        self.url = validate_url(url)
        self.audit = audit
        self.rq_audit = Queue('audit',
                              connection=Redis.from_url('redis://'))

    def start_audit(self):
        object_id = AuditDB.init_object_id()
        audit = self.rq_audit.enqueue(call_audit,
                                      data={'audit': self.audit,
                                            'url': self.url,
                                            'object_id': object_id},
                                      job_timeout=864000)
        AuditDB().add_result(_id=object_id,
                             queue_id=audit.id,
                             audit=self.audit,
                             url=self.url)
        return audit.id

    @staticmethod
    def list_audit() -> dict:
        path = os.getcwd() + '/audits/'

        def convert_name(name):
            return name.replace('_', ' ').title().replace(' ', '')

        return {name_audit: convert_name(name_audit)
                for name_audit in os.listdir(path)
                if '__' not in name_audit}


def call_audit(data):
    message = f'%status% audit "{data["audit"]}" - {datetime.datetime.now()}'

    print(terminal.green(message.replace('%status%', 'Start')))
    audit = data['audit']
    module_audit = importlib.import_module(f"audits.{audit}.{audit}")
    module_audit.audit = getattr(module_audit, audit)
    result_audit = None
    status = True
    try:
        result_audit = module_audit.audit(data)
    except Exception as e:
        print(str(e))
        status = False
    AuditDB().update_result(object_id=data['object_id'],
                            data={'audit_result': result_audit,
                                  'status': status})
    if status:
        # status success
        print(terminal.green(message.replace('%status%', 'Finished')))
    else:
        # status failed
        print(terminal.red(message.replace('%status%', 'Failed')))
