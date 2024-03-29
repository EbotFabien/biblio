from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


logemen_t= db.collection('logement')





logement =Blueprint('logement',__name__)

@logement.route('/logement/ajouter', methods=['POST'])
def create():
    temp,parti=logemen_t.add(request.json)
    todo = logemen_t.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@logement.route('/logement/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in logemen_t.stream()]
    all_todos=[]
    for doc in logemen_t.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@logement.route('/logement/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = logemen_t.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@logement.route('/logement/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = logemen_t.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            logemen_t.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@logement.route('/logement/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = logemen_t.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        logemen_t.document(todo_id).delete()
        return jsonify({"success": True}), 200