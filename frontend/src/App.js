import React, { useState, useEffect } from 'react';

function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(null);

  const loadTodos = async () => {
    try {
      const res = await fetch('/api/todos');
      const data = await res.json();
      setTodos(data);
    } catch (e) {
      setError('Failed to connect to backend');
    }
  };

  useEffect(() => { loadTodos(); }, []);

  const addTodo = async () => {
    if (!title.trim()) return;
    setError('');
    try {
      const res = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
      });
      const data = await res.json();
      if (res.ok) { setTodos([data, ...todos]); setTitle(''); setDescription(''); }
      else setError(data.error || 'Failed to add');
    } catch (e) { setError('Network error'); }
  };

  const toggleTodo = async (id, completed) => {
    try {
      await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !completed })
      });
      loadTodos();
    } catch (e) { setError('Failed to update'); }
  };

  const deleteTodo = async (id) => {
    try {
      await fetch(`/api/todos/${id}`, { method: 'DELETE' });
      loadTodos();
    } catch (e) { setError('Failed to delete'); }
  };

  const startEdit = (todo) => {
    setEditing(todo.id);
    setTitle(todo.title);
    setDescription(todo.description || '');
  };

  const saveEdit = async (id) => {
    if (!title.trim()) return;
    setError('');
    try {
      const res = await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
      });
      const data = await res.json();
      if (res.ok) { setEditing(null); setTitle(''); setDescription(''); loadTodos(); }
      else setError(data.error || 'Failed to update');
    } catch (e) { setError('Network error'); }
  };

  const cancelEdit = () => {
    setEditing(null);
    setTitle('');
    setDescription('');
    setError('');
  };

  return (
    <div style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh', padding: '40px 20px' }}>
      <div style={{ maxWidth: '640px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{ color: 'white', fontSize: '2.5rem', marginBottom: '8px', textShadow: '0 2px 10px rgba(0,0,0,0.2)' }}>📝 Todo List</h1>
          <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '1.1rem', margin: 0 }}>Stay organized, get things done</p>
        </div>

        <div style={{ background: 'white', borderRadius: '16px', padding: '24px', boxShadow: '0 10px 40px rgba(0,0,0,0.2)', marginBottom: '20px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {editing !== null ? (
              <>
                <h3 style={{ margin: '0 0 8px', color: '#333' }}>✏️ Edit Todo</h3>
                <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" style={{ padding: '12px', border: '2px solid #e0e0e0', borderRadius: '8px', fontSize: '1rem', outline: 'none' }} />
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description (optional)" rows={2} style={{ padding: '12px', border: '2px solid #e0e0e0', borderRadius: '8px', fontSize: '1rem', outline: 'none', resize: 'vertical', fontFamily: 'inherit' }} />
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button onClick={() => saveEdit(editing)} style={{ flex: 1, padding: '10px', background: '#667eea', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '1rem', fontWeight: '600' }}>Save</button>
                  <button onClick={cancelEdit} style={{ padding: '10px 20px', background: '#eee', color: '#333', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '1rem' }}>Cancel</button>
                </div>
              </>
            ) : (
              <>
                <h3 style={{ margin: '0 0 8px', color: '#333' }}>➕ Add New Todo</h3>
                <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="What needs to be done?" style={{ padding: '12px', border: '2px solid #e0e0e0', borderRadius: '8px', fontSize: '1rem', outline: 'none' }} />
                <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description (optional)" style={{ padding: '12px', border: '2px solid #e0e0e0', borderRadius: '8px', fontSize: '1rem', outline: 'none' }} />
                <button onClick={addTodo} style={{ padding: '12px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '1rem', fontWeight: '600', boxShadow: '0 4px 15px rgba(102,126,234,0.4)' }}>Add Todo</button>
              </>
            )}
          </div>
          {error && <p style={{ color: '#e74c3c', marginTop: '12px', padding: '8px 12px', background: '#ffeaea', borderRadius: '6px', fontSize: '0.9rem' }}>{error}</p>}
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px', padding: '0 4px' }}>
          <h2 style={{ color: 'white', fontSize: '1.3rem', margin: 0 }}>Tasks</h2>
          <span style={{ color: 'rgba(255,255,255,0.8)', background: 'rgba(255,255,255,0.2)', padding: '4px 12px', borderRadius: '20px', fontSize: '0.9rem' }}>{todos.length} {todos.length === 1 ? 'task' : 'tasks'}</span>
        </div>

        {todos.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'rgba(255,255,255,0.7)', background: 'rgba(255,255,255,0.1)', borderRadius: '12px', backdropFilter: 'blur(10px)' }}>
            <p style={{ fontSize: '1.2rem', margin: 0 }}>🎉 No tasks yet! Add one above.</p>
          </div>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {todos.map(t => (
              <li key={t.id} style={{ background: 'white', borderRadius: '12px', padding: '14px 16px', display: 'flex', alignItems: 'center', gap: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.08)', borderLeft: t.completed ? '4px solid #667eea' : '4px solid transparent' }}>
                <input type="checkbox" checked={t.completed} onChange={() => toggleTodo(t.id, t.completed)} style={{ width: '20px', height: '20px', cursor: 'pointer', accentColor: '#667eea' }} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: '500', color: '#333', textDecoration: t.completed ? 'line-through' : 'none', opacity: t.completed ? 0.6 : 1, wordBreak: 'break-word' }}>{t.title}</div>
                  {t.description && <div style={{ fontSize: '0.85rem', color: '#999', marginTop: '2px' }}>{t.description}</div>}
                </div>
                <button onClick={() => startEdit(t)} style={{ background: '#f0f0f0', border: 'none', padding: '6px 10px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem', color: '#667eea', flexShrink: 0 }}>Edit</button>
                <button onClick={() => deleteTodo(t.id)} style={{ background: '#ffe0e0', border: 'none', padding: '6px 10px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem', color: '#e74c3c', flexShrink: 0 }}>Delete</button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
