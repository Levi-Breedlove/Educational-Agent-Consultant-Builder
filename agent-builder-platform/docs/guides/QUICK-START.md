# Quick Start Guide - Agent Builder Frontend

## Prerequisites

- Node.js 18+ installed
- Backend API running at http://localhost:8000

## Setup (Choose your platform)

### Windows (PowerShell)
```powershell
cd agent-builder-platform/frontend
.\setup.ps1
```

### Linux/Mac (Bash)
```bash
cd agent-builder-platform/frontend
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
npm install
cp .env.example .env
```

## Run Development Server

```bash
npm run dev
```

The frontend will be available at **http://localhost:3000**

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## Environment Variables

Create a `.env` file (or copy from `.env.example`):

```env
VITE_API_URL=http://localhost:8000
```

## Verify Setup

1. ✅ Home page loads at http://localhost:3000
2. ✅ Theme toggle works (sun/moon icon in header)
3. ✅ "Start Building" button navigates to /builder
4. ✅ No console errors

## Troubleshooting

### Port 3000 already in use
```bash
# Change port in vite.config.ts
server: {
  port: 3001,  // Use different port
}
```

### Backend connection fails
- Ensure backend is running at http://localhost:8000
- Check VITE_API_URL in .env file
- Verify proxy configuration in vite.config.ts

### Dependencies fail to install
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Task 12.2: Chat interface (WebSocket, streaming, syntax highlighting)
- Task 12.3: Progress tracker (5-phase visualization)
- Task 12.4: Responsive design (mobile, tablet, desktop)
- Task 12.5: Accessibility (WCAG 2.1 AA compliance)

## Tech Stack

- React 18.2 + TypeScript
- Vite 5.0 (build tool)
- Redux Toolkit 2.0 (state)
- React Query 5.14 (server state)
- Material-UI 5.14 (components)
- React Router 6.20 (routing)

## Support

See `README.md` for detailed documentation.
