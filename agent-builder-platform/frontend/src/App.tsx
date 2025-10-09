import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { useSelector } from 'react-redux'
import { RootState } from './store'
import { lightTheme, darkTheme } from './theme'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import AgentBuilderPage from './pages/AgentBuilderPage'
import CodeMirrorTestPage from './pages/CodeMirrorTestPage'
import ConfidenceDashboardTestPage from './pages/ConfidenceDashboardTestPage'

function App() {
  const theme = useSelector((state: RootState) => state.ui.theme)
  const currentTheme = theme === 'dark' ? darkTheme : lightTheme

  return (
    <ThemeProvider theme={currentTheme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="builder" element={<AgentBuilderPage />} />
            <Route path="builder/:agentId" element={<AgentBuilderPage />} />
            <Route path="test-codemirror" element={<CodeMirrorTestPage />} />
            <Route path="test-confidence" element={<ConfidenceDashboardTestPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
