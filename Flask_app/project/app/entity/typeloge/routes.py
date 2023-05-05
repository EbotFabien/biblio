from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


typelog_e= db.collection('typeloge')





typeloge =Blueprint('typeloge',__name__)

@typeloge.route('/typeloge/ajouter', methods=['POST'])
def create():
    temp,parti=typelog_e.add(request.json)
    todo = typelog_e.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@typeloge.route('/typeloge/tous', methods=['GET'])
def read():
    all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in typelog_e.stream()]
    return jsonify(all_todos), 200

@typeloge.route('/typeloge/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = typelog_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@typeloge.route('/typeloge/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = typelog_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            typelog_e.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200

@typeloge.route('/typeloge/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = typelog_e.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        typelog_e.document(todo_id).delete()
        return jsonify({"success": True}), 200