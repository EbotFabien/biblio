from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


ex_t= db.collection('Extension')





extension =Blueprint('extension',__name__)

@extension.route('/extension/ajouter', methods=['POST'])
def create():
    temp,parti=ex_t.add(request.json)
    todo = ex_t.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@extension.route('/extension/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in ex_t.stream()]
    all_todos=[]
    for doc in ex_t.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@extension.route('/extension/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = ex_t.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@extension.route('/extension/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = ex_t.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            ex_t.document(todo_id).update(request.json)
            todo = ex_t.document(ide).get()
            final_= todo.to_dict()
            final_["id"] = ide
            return jsonify(final_), 200
            #return jsonify({"success": True}), 200

@extension.route('/extension/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = ex_t.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        ex_t.document(todo_id).delete()
        return jsonify({"success": True}), 200
