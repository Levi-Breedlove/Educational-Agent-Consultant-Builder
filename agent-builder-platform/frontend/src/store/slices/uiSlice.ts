import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface UiState {
  theme: 'light' | 'dark'
  themeSource: 'system' | 'manual'
  sidebarOpen: boolean
  loading: boolean
  error: string | null
  isMobile: boolean
  activeTab: number
  tabHistory: number[]
}

// Detect system theme preference
const getSystemTheme = (): 'light' | 'dark' => {
  if (typeof window !== 'undefined' && window.matchMedia) {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  return 'light'
}

// Detect mobile device
const getIsMobile = (): boolean => {
  if (typeof window !== 'undefined') {
    return window.innerWidth < 960
  }
  return false
}

// Load saved theme preference or default to dark
const loadInitialTheme = (): 'light' | 'dark' => {
  // Always default to dark theme
  return 'dark'
}

const loadThemeSource = (): 'system' | 'manual' => {
  // Always use manual theme (dark by default)
  return 'manual'
}

const initialState: UiState = {
  theme: loadInitialTheme(),
  themeSource: loadThemeSource(),
  sidebarOpen: !getIsMobile(),
  loading: false,
  error: null,
  isMobile: getIsMobile(),
  activeTab: 0, // Default to Chat tab
  tabHistory: [0],
}

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.theme = state.theme === 'light' ? 'dark' : 'light'
      state.themeSource = 'manual'
      if (typeof window !== 'undefined') {
        localStorage.setItem('theme', state.theme)
        localStorage.setItem('themeSource', 'manual')
      }
    },
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload
      state.themeSource = 'manual'
      if (typeof window !== 'undefined') {
        localStorage.setItem('theme', action.payload)
        localStorage.setItem('themeSource', 'manual')
      }
    },
    setSystemTheme: (state) => {
      state.theme = getSystemTheme()
      state.themeSource = 'system'
      if (typeof window !== 'undefined') {
        localStorage.setItem('themeSource', 'system')
        localStorage.removeItem('theme')
      }
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
    setIsMobile: (state, action: PayloadAction<boolean>) => {
      state.isMobile = action.payload
      // Auto-close sidebar on mobile
      if (action.payload) {
        state.sidebarOpen = false
      }
    },
    setActiveTab: (state, action: PayloadAction<number>) => {
      state.activeTab = action.payload
      // Add to history if not already the last item
      if (state.tabHistory[state.tabHistory.length - 1] !== action.payload) {
        state.tabHistory.push(action.payload)
        // Keep history limited to last 10 tabs
        if (state.tabHistory.length > 10) {
          state.tabHistory.shift()
        }
      }
    },
  },
})

export const { 
  toggleTheme, 
  setTheme, 
  setSystemTheme,
  toggleSidebar, 
  setSidebarOpen,
  setLoading, 
  setError,
  setIsMobile,
  setActiveTab,
} = uiSlice.actions
export default uiSlice.reducer
