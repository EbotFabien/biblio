from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


clef_s = db.collection('clefs')





clefs =Blueprint('clefs',__name__)

@clefs.route('/Clefs/ajouter', methods=['POST'])
def create():
    temp,parti=clef_s.add(request.json)
    todo = clef_s.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@clefs.route('/Clefs/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in clef_s.stream()]
    all_todos=[]
    for doc in clef_s.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@clefs.route('/Clefs/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = clef_s.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@clefs.route('/Clefs/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = clef_s.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            clef_s.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@clefs.route('/Clefs/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = clef_s.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        clef_s.document(todo_id).delete()
        return jsonify({"success": True}), 200