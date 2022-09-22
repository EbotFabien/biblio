from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


rubri_c = db.collection('Rubric')





rubric=Blueprint('Rubric',__name__)

@rubric.route('/Rubric/ajouter', methods=['POST'])
def create():
    try:
        id=[doc.to_dict() for doc in rubri_c.stream()][-1]['id']
        id=str(int(id)+1)
    except:
        id='0'
    if id:
        request.json['id']=str(id)
        todo = rubri_c.document(id).get()
        if  todo.to_dict() is None :
            rubri_c.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"Fail": "donnee exist deja"}), 400
    else:
        return 400

@rubric.route('/Rubric/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in rubri_c.stream()]
    return jsonify(all_todos), 200

@rubric.route('/Rubric/<int:ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = rubri_c.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@rubric.route('/Rubric/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = rubri_c.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            rubri_c.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@rubric.route('/Rubric/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = rubri_c.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        rubri_c.document(todo_id).delete()
        return jsonify({"success": True}), 200