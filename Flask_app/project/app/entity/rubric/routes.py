from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt


rubri_c = db.collection('Rubric')





rubric=Blueprint('Rubric',__name__)

@rubric.route('/Rubric/ajouter', methods=['POST'])
def create():
    temp,parti=rubri_c.add(request.json)
    todo = rubri_c.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@rubric.route('/Rubric/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in rubri_c.stream()]
    all_todos=[]
    for doc in rubri_c.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@rubric.route('/Rubric/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = rubri_c.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@rubric.route('/Rubric/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = rubri_c.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            rubri_c.document(todo_id).update(request.json)
            todo = rubri_c.document(ide).get()
            final_= todo.to_dict()
            final_["id"] = ide
            return jsonify(final_), 200

@rubric.route('/Rubric/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = rubri_c.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        rubri_c.document(todo_id).delete()
        return jsonify({"success": True}), 200
