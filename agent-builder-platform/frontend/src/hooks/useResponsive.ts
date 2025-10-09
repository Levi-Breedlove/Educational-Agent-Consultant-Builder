import { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { useTheme } from '@mui/material/styles'
import useMediaQuery from '@mui/material/useMediaQuery'
import { setIsMobile } from '../store/slices/uiSlice'

export const useResponsive = () => {
  const theme = useTheme()
  const dispatch = useDispatch()
  
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const isTablet = useMediaQuery(theme.breakpoints.between('md', 'lg'))
  const isDesktop = useMediaQuery(theme.breakpoints.up('lg'))
  
  useEffect(() => {
    dispatch(setIsMobile(isMobile))
  }, [isMobile, dispatch])
  
  return {
    isMobile,
    isTablet,
    isDesktop,
  }
}

export default useResponsive
