from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


typeco_m= db.collection('typecom')





typecom =Blueprint('typecom',__name__)

@typecom.route('/typecom/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    if id:
        todo = typeco_m.document(id).get()
        if  todo.to_dict() is None :
            typelog_e.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@typecom.route('/typecom/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in typeco_m.stream()]
    return jsonify(all_todos), 200

@typecom.route('/typecom/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = typeco_m.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@typecom.route('/typecom/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = typeco_m.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            typeco_m.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@typecom.route('/typecom/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = typeco_m.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        typeco_m.document(todo_id).delete()
        return jsonify({"success": True}), 200