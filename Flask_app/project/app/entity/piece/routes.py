from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


piec_e = db.collection('piece')





piece =Blueprint('piece',__name__)

@piece.route('/piece/ajouter', methods=['POST'])
def create():
    id = request.json['id']
    if id:
        request.json['pass']=bcrypt.generate_password_hash(request.json['pass']).decode('utf-8')
        todo = piec_e.document(id).get()
        if  todo.to_dict() is None :
            piec_e.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@piece.route('/piece/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in piec_e.stream()]
    return jsonify(all_todos), 200

@piece.route('/piece/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = piec_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@piece.route('/piece/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = piec_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            piec_e.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@piece.route('/piece/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = piec_e.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        piec_e.document(todo_id).delete()
        return jsonify({"success": True}), 200