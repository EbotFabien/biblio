from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db


commentair_e= db.collection('commentaire')





commentaire =Blueprint('commentaire',__name__)

@commentaire.route('/amsv2com/ajouter', methods=['POST'])
def create():
    temp,parti=commentair_e.add(request.json)
    todo = commentair_e.document(parti.id).get()
    v=todo.to_dict()
    v['id']=parti.id
    return jsonify(v), 200

@commentaire.route('/amsv2com/tous', methods=['GET'])
def read():
    #all_todos = [{"data":doc.to_dict(),"id":doc.id} for doc in commentair_e.stream()]
    all_todos=[]
    for doc in commentair_e.stream():
        #if doc.to_dict()["utilisateur_id"] == "vide":
        v=doc.to_dict()
        v["id"]=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200

@commentaire.route('/amsv2com/<ide>', methods=['GET'])
def read_ind(ide):
    todo_id = str(ide)
    
    if todo_id:
        todo = commentair_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200
        
@commentaire.route('/amsv2com/<Type>/<category>', methods=['GET'])
def search_ind(Type,category):
    if category == 'None':
        todo = commentair_e.where('type', '==',Type)
        all_todos=[]
        for doc in todo.stream():
            #if doc.to_dict()["utilisateur_id"] == "vide":
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200
        
    if Type == "None":
        todo = commentair_e.where('nature', '==', category)
        all_todos=[]
        for doc in todo.stream():
            #if doc.to_dict()["utilisateur_id"] == "vide":
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200
    else:
        todo = commentair_e.where('type', '==',Type).where('nature', '==', category)
        all_todos=[]
        for doc in todo.stream():
            #if doc.to_dict()["utilisateur_id"] == "vide":
            v=doc.to_dict()
            v["id"]=doc.id
            all_todos.append(v)
        return jsonify(all_todos), 200
@commentaire.route('/amsv2com/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = commentair_e.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            commentair_e.document(todo_id).update(request.json)
            todo = commentair_e.document(ide).get()
            final_= todo.to_dict()
            final_["id"] = ide
            return jsonify(final_), 200
            

@commentaire.route('/amsv2com/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = commentair_e.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        commentair_e.document(todo_id).delete()
        return jsonify({"success": True}), 200
