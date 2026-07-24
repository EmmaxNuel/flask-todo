from flask import Flask, request, jsonify
from flask_cors import CORS
from todo.db.database import get_connection, init_db

init_db()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"])

@app.route('/api/todos', methods=['GET'])
def list_todos():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM todos ORDER BY created_at DESC").fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        conn.close()

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if row is None:
            return jsonify({'error': 'Todo not found'}), 404
        return jsonify(dict(row))
    finally:
        conn.close()

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO todos (title, description) VALUES (?, ?)",
            (data['title'], data.get('description', ''))
        )
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    finally:
        conn.close()

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if row is None:
            return jsonify({'error': 'Todo not found'}), 404
        title = data.get('title', row['title'])
        description = data.get('description', row['description'])
        completed = data.get('completed', bool(row['completed']))
        conn.execute(
            "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
            (title, description, 1 if completed else 0, todo_id)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        return jsonify(dict(row))
    finally:
        conn.close()

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if row is None:
            return jsonify({'error': 'Todo not found'}), 404
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        return jsonify({'message': 'Todo deleted'}), 200
    finally:
        conn.close()
