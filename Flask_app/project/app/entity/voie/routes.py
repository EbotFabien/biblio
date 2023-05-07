from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


voi_e = db.collection('Rubric')





voie=Blueprint('Voie',__name__)

@voie.route('/voie/ajouter', methods=['POST'])
def create():
    temp,parti=voi_e.add(request.json)
    todo = voi_e.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@voie.route('/voie/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in voi_e.stream()]
    all_todos=[]
    for doc in voi_e.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@voie.route('/voie/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = voi_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@voie.route('/voie/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = voi_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            voi_e.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@voie.route('/voie/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = voi_e.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        voi_e.document(todo_id).delete()
        return jsonify({"success": True}), 200