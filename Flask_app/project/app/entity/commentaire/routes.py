from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


commentair_e= db.collection('commentaire')





commentaire =Blueprint('commentaire',__name__)

@commentaire.route('/commentaire/ajouter', methods=['POST'])
def create():
    temp,parti=commentair_e.add(request.json)
    todo = commentair_e.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@commentaire.route('/commentaire/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in commentair_e.stream()]
    all_todos=[]
    for doc in commentair_e.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@commentaire.route('/commentaire/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = commentair_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200
@commentaire.route('/commentaire/<Type>/<category>', methods=['GET'])
def read_ind(Type,category=None):
    if category == None:
        todo = commentair_e.where('type', '==',Type)
        all_todos=[]
        for doc in todo.stream():
            #if doc.to_dict()["utilisateur_id"] == "vide":
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200
    else:
        todo = commentair_e.where('type', '==',Type).where('category', '==', category)
        all_todos=[]
        for doc in todo.stream():
            #if doc.to_dict()["utilisateur_id"] == "vide":
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200
@commentaire.route('/commentaire/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = commentair_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            commentair_e.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@commentaire.route('/commentaire/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = commentair_e.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        commentair_e.document(todo_id).delete()
        return jsonify({"success": True}), 200
