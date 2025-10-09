# Agent Builder Platform - Frontend

React 18+ frontend application for the Agent Builder Platform with TypeScript, Vite, Redux Toolkit, React Query, and Material-UI.

## Features

- **React 18+** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **Redux Toolkit** for global state management
- **React Query** for server state and API calls
- **Material-UI** for component library and theming
- **React Router** for client-side routing
- **Dark/Light theme** support

## Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on http://localhost:8000

## Installation

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env
```

## Development

```bash
# Start development server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and endpoints
│   ├── components/       # Reusable React components
│   ├── pages/            # Page components
│   ├── store/            # Redux store and slices
│   ├── theme/            # Material-UI theme configuration
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # Entry point
│   └── index.css         # Global styles
├── public/               # Static assets
├── index.html            # HTML template
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000` with the following endpoints:

- `POST /api/sessions` - Create new session
- `GET /api/sessions/:id` - Get session details
- `POST /api/agents/create` - Create new agent
- `GET /api/agents/:id/status` - Get agent status
- `WS /ws/agents/:id` - WebSocket for real-time updates

## State Management

### Redux Slices

- **sessionSlice**: Session and connection state
- **workflowSlice**: Workflow phases and progress
- **uiSlice**: UI state (theme, sidebar, loading, errors)

### React Query

Used for server state management with automatic caching, refetching, and error handling.

## Theming

Material-UI theme with light/dark mode support. Toggle theme using the button in the app bar.

## Next Steps

- Task 12.2: Build chat interface component
- Task 12.3: Implement progress tracker component
- Task 12.4: Build responsive design and theming
- Task 12.5: Implement accessibility features
