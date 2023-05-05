from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


piec_e = db.collection('piece')





piece =Blueprint('piece',__name__)

@piece.route('/piece/ajouter', methods=['POST'])
def create():
    temp,parti=piec_e.add(request.json)
    todo = piec_e.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@piece.route('/piece/tous', methods=['GET'])
def read():
    all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in piec_e.stream()]
    return jsonify(all_todos), 200

@piece.route('/piece/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = piec_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@piece.route('/piece/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = piec_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            piec_e.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@piece.route('/piece/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = piec_e.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        piec_e.document(todo_id).delete()
        return jsonify({"success": True}), 200