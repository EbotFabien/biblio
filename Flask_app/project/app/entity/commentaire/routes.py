from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


commentair_e= db.collection('commentaire')





commentaire =Blueprint('commentaire',__name__)

@commentaire.route('/commentaire/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    if id:
        todo = commentair_e.document(id).get()
        if  todo.to_dict() is None :
            commentair_e.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@commentaire.route('/commentaire/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in commentair_e.stream()]
    return jsonify(all_todos), 200

@commentaire.route('/commentaire/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = commentair_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@commentaire.route('/commentaire/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = commentair_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            commentair_e.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@commentaire.route('/commentaire/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = commentair_e.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        commentair_e.document(todo_id).delete()
        return jsonify({"success": True}), 200