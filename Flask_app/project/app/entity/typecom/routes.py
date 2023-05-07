from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


typeco_m= db.collection('typecom')





typecom =Blueprint('typecom',__name__)

@typecom.route('/typecom/ajouter', methods=['POST'])
def create():
    temp,parti=typeco_m.add(request.json)
    todo = typeco_m.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@typecom.route('/typecom/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in typeco_m.stream()]
    all_todos=[]
    for doc in typeco_m.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@typecom.route('/typecom/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = typeco_m.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@typecom.route('/typecom/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = typeco_m.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            typeco_m.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@typecom.route('/typecom/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = typeco_m.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        typeco_m.document(todo_id).delete()
        return jsonify({"success": True}), 200