from flask import Flask, request, jsonify
from flask_cors import CORS
from todo.db.database import get_connection, init_db
from todo.services.todo_service import TodoService
from datetime import datetime

init_db()

app = Flask(__name__)
CORS(app, origins=["*"])
service = TodoService()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Flask Todo API is running', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/todos', methods=['GET'])
def list_todos():
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    result = service.list_all(search=search, status=status, priority=priority, page=page, per_page=per_page)
    return jsonify(result)

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = service.get_by_id(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo.__dict__)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    if not data['title'].strip():
        return jsonify({'error': 'Title cannot be empty'}), 400
    todo = service.create(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date')
    )
    return jsonify(todo.__dict__), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todo = service.update(
        todo_id,
        title=data.get('title'),
        description=data.get('description'),
        completed=data.get('completed'),
        priority=data.get('priority'),
        due_date=data.get('due_date')
    )
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo.__dict__)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    deleted = service.delete(todo_id)
    if not deleted:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'message': 'Todo deleted'}), 200

@app.route('/api/todos/clear-completed', methods=['DELETE'])
def clear_completed():
    count = service.clear_completed()
    return jsonify({'message': f'Cleared {count} completed todos', 'deleted_count': count}), 200
