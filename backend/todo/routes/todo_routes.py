from flask import Flask, request, jsonify
from todo.services.todo_service import TodoService
from todo.db.database import init_db

init_db()

app = Flask(__name__)
service = TodoService()

@app.route('/api/todos', methods=['GET'])
def list_todos():
    todos = service.list_all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'completed': t.completed,
        'created_at': t.created_at
    } for t in todos])

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = service.get_by_id(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at
    })

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    todo = service.create(data['title'], data.get('description', ''))
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at
    }), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todo = service.update(
        todo_id,
        title=data.get('title'),
        description=data.get('description'),
        completed=data.get('completed')
    )
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'created_at': todo.created_at
    })

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    deleted = service.delete(todo_id)
    if not deleted:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'message': 'Todo deleted'}), 200
