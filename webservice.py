# -*- coding: utf-8 -*-
import os.path
from flask import (Flask, Response, render_template, request, jsonify, _request_ctx_stack, send_from_directory, redirect, url_for, session, make_response)
from datetime import datetime
import json

app = Flask(__name__)

class ListData():
    def __init__(self):
        self.list = []
        self.count = 0
    def append(self, data):
        self.count = self.count+1
        data['id'] = self.count
        print("append:",data)
        self.list.append(data)
    def deleteById(self, logId):
        for item in self.list:
            if str(item['id'])==logId:
                self.list.remove(item)
    def clean(self):
        self.list=[]
        self.count=0
    def get(self,id):
        res = {}
        for item in self.list:
            if item['id']==int(id):
                res = item
        return res

storeInstance = ListData()

@app.route('/')
def index():
    return render_template('index.html')

def custom_error(message, status_code): 
    return make_response(jsonify(message), status_code)

@app.route('/user/<id>', methods=['DELETE','GET'])
def LogController(id):
    if request.method=='DELETE':
        storeInstance.deleteById(id)
        res = {}
        res['list']=storeInstance.list
        return res
    if request.method=='GET':
        res = storeInstance.get(id)
        if res:
            return res
        else:
            return custom_error("Not found!",404)


@app.route('/user', methods=['GET','POST','DELETE'])
def UserController():
    if request.method=='GET':
        res = {}
        res['list']=storeInstance.list
        return res
    elif request.method=='POST':
        data = request.get_json()
        print("POST:data:",data)
        storeInstance.append(data)
        res = {}
        res['list']=storeInstance.list
        return res
    elif request.method=='DELETE':
        storeInstance.clean()
        res = {}
        res['list']=storeInstance.list
        return res
    else:
        return custom_error("Forbidden",403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)