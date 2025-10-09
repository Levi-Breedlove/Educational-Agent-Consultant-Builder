import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState } from '../store'
import { setSystemTheme } from '../store/slices/uiSlice'

export const useSystemTheme = () => {
  const dispatch = useDispatch()
  const themeSource = useSelector((state: RootState) => state.ui.themeSource)
  
  useEffect(() => {
    // Only listen to system theme changes if user hasn't manually set a theme
    if (themeSource !== 'system') return
    
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    
    const handleChange = () => {
      if (themeSource === 'system') {
        dispatch(setSystemTheme())
      }
    }
    
    // Listen for system theme changes
    mediaQuery.addEventListener('change', handleChange)
    
    return () => {
      mediaQuery.removeEventListener('change', handleChange)
    }
  }, [dispatch, themeSource])
}

export default useSystemTheme
