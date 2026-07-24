# Flask Todo App

A full-featured CRUD todo application built with a **Flask backend** and **React frontend**, following a layered architecture pattern.

## Architecture

The backend uses a layered architecture where route handlers delegate to service logic, which manages model and database operations — keeping each layer focused and testable.

```
frontend/          # React SPA (Create React App)
backend/
  app.py           # Application entry point
  todo/
    routes/        # Flask route handlers (HTTP layer)
    services/      # Business logic layer
    models/        # Data models (dataclasses)
    db/            # Database connection & initialization
```

## Features

- **Create** — Add new todos with a title and optional description
- **Read** — List all todos or fetch a single todo by ID
- **Update** — Edit todo title, description, and toggle completion status
- **Delete** — Remove todos with confirmation
- **CORS-enabled** — API accessible from the React frontend on localhost:3000
- **SQLite persistence** — Lightweight file-based database with foreign key support

## Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Frontend    | React 18, JavaScript    |
| Backend     | Flask 3.0, Flask-CORS   |
| Database    | SQLite 3                |

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API server runs on `http://localhost:5000`.

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The React dev server runs on `http://localhost:3000`.

### Install Everything

```bash
npm run install-all
```

## API Endpoints

| Method | Endpoint          | Description                  |
|--------|-------------------|------------------------------|
| GET    | `/api/todos`      | List all todos               |
| GET    | `/api/todos/<id>` | Get a single todo            |
| POST   | `/api/todos`      | Create a new todo            |
| PUT    | `/api/todos/<id>` | Update an existing todo      |
| DELETE | `/api/todos/<id>` | Delete a todo                |

### Example Request — Create Todo

```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs"}'
```

## License

MIT
