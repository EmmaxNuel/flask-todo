import os, sys, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from todo.services.todo_service import TodoService
from todo.db.database import init_db, DB_PATH

@pytest.fixture(autouse=True)
def setup():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()

class TestTodoService:
    def test_create_todo(self):
        svc = TodoService()
        todo = svc.create('Test Todo', 'Description', 'high')
        assert todo.title == 'Test Todo'
        assert todo.priority == 'high'

    def test_list_todos(self):
        svc = TodoService()
        svc.create('Todo 1')
        svc.create('Todo 2')
        result = svc.list_all()
        assert result['total'] == 2

    def test_search_todos(self):
        svc = TodoService()
        svc.create('Buy milk')
        svc.create('Walk dog')
        result = svc.list_all(search='milk')
        assert result['total'] == 1

    def test_complete_todo(self):
        svc = TodoService()
        todo = svc.create('Test')
        svc.update(todo.id, completed=True)
        updated = svc.get_by_id(todo.id)
        assert updated.completed == True
