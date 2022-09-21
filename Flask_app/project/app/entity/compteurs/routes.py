from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


compteur_s = db.collection('compteurs')





compteurs =Blueprint('compteurs',__name__)

@compteurs.route('/compteurs/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    request.json['pass']=bcrypt.generate_password_hash(request.json['pass']).decode('utf-8')
    if id:
        todo = compteur_s.document(id).get()
        if  todo.to_dict() is None :
            compteur_s.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@compteurs.route('/compteurs/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in compteur_s.stream()]
    return jsonify(all_todos), 200

@compteurs.route('/compteurs/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = compteur_s.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@compteurs.route('/compteurs/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = compteur_s.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            compteur_s.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@compteurs.route('/compteurs/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = compteur_s.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        compteur_s.document(todo_id).delete()
        return jsonify({"success": True}), 200