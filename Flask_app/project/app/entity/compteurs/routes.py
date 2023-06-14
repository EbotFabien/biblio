from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


compteur_s = db.collection('compteurs')





compteurs =Blueprint('compteurs',__name__)

@compteurs.route('/compteurs/ajouter', methods=['POST'])
def create():
    temp,parti=compteur_s.add(request.json)
    todo = compteur_s.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@compteurs.route('/compteurs/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in compteur_s.stream()]
    all_todos=[]
    for doc in compteur_s.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@compteurs.route('/compteurs/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = compteur_s.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@compteurs.route('/compteurs/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = compteur_s.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            compteur_s.document(todo_id).update(request.json)
            todo = compteur_s.document(ide).get()
            final_= todo.to_dict()
            final_["id"] = ide
            return jsonify(final_), 200

@compteurs.route('/compteurs/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = compteur_s.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        compteur_s.document(todo_id).delete()
        return jsonify({"success": True}), 200
