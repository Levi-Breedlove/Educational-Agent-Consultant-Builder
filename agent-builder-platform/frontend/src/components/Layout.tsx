import { Outlet, useNavigate } from 'react-router-dom'
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Menu,
  MenuItem,
  Divider,
  useTheme,
} from '@mui/material'
import {
  Brightness4,
  Brightness7,
  Settings,
  Code,
} from '@mui/icons-material'
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../store'
import { setTheme, setSystemTheme } from '../store/slices/uiSlice'
import useSystemTheme from '../hooks/useSystemTheme'
import SkipLinks from './SkipLink'

export default function Layout() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const theme = useTheme()
  const isDark = theme.palette.mode === 'dark'
  const currentTheme = useSelector((state: RootState) => state.ui.theme)
  const themeSource = useSelector((state: RootState) => state.ui.themeSource)
  const [themeMenuAnchor, setThemeMenuAnchor] = useState<null | HTMLElement>(null)

  // Listen for system theme changes
  useSystemTheme()

  // Set data-theme attribute on body for CSS styling
  useEffect(() => {
    document.body.setAttribute('data-theme', currentTheme)
  }, [currentTheme])

  const handleThemeMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setThemeMenuAnchor(event.currentTarget)
  }

  const handleThemeMenuClose = () => {
    setThemeMenuAnchor(null)
  }

  const handleSetLightTheme = () => {
    dispatch(setTheme('light'))
    handleThemeMenuClose()
  }

  const handleSetDarkTheme = () => {
    dispatch(setTheme('dark'))
    handleThemeMenuClose()
  }

  const handleSetSystemTheme = () => {
    dispatch(setSystemTheme())
    handleThemeMenuClose()
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>
      <SkipLinks />
      <AppBar 
        position="static" 
        elevation={1} 
        component="header" 
        role="banner"
        sx={{
          ...(isDark && {
            background: 'rgba(15, 23, 42, 0.8)',
            backdropFilter: 'blur(20px) saturate(180%)',
            borderBottom: '1px solid rgba(104, 211, 145, 0.3)',
            boxShadow: '0 4px 20px rgba(104, 211, 145, 0.15)',
          }),
        }}
      >
        <Toolbar id="navigation">
          <Code 
            sx={{ 
              mr: 1.5, 
              fontSize: 28,
              color: isDark ? '#68d391' : 'inherit',
              filter: isDark ? 'drop-shadow(0 0 8px rgba(104, 211, 145, 0.6))' : 'none',
            }} 
          />
          <Typography
            variant="h6"
            component="div"
            sx={{
              flexGrow: 1,
              fontSize: { xs: '1rem', sm: '1.25rem' },
              cursor: 'pointer',
              fontWeight: 600,
              ...(isDark && {
                background: 'linear-gradient(135deg, #68d391 0%, #ec4899 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }),
            }}
            onClick={() => navigate('/')}
          >
            Agent Builder Platform
          </Typography>
          {/* Theme toggle removed - dark theme is default */}
        </Toolbar>
      </AppBar>

      <Box
        component="main"
        id="main-content"
        role="main"
        aria-label="Main content"
        tabIndex={-1}
        sx={{
          flex: 1,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          '&:focus': {
            outline: 'none',
          },
        }}
      >
        <Outlet />
      </Box>
    </Box>
  )
}
