import { Box } from '@mui/material'
import { ReactNode } from 'react'

interface TabPanelProps {
  children?: ReactNode
  index: number
  value: number
  keepMounted?: boolean
  id?: string
}

/**
 * TabPanel Component
 * 
 * Accessible tab panel component that manages visibility and ARIA attributes
 * for tabbed interfaces. Follows WAI-ARIA best practices for tab panels.
 * 
 * @param children - Content to display in the tab panel
 * @param index - The index of this tab panel
 * @param value - The currently active tab index
 * @param keepMounted - If true, keeps the panel mounted in DOM when hidden (default: false)
 * @param id - Optional ID prefix for ARIA attributes
 * 
 * @example
 * ```tsx
 * <TabPanel value={activeTab} index={0}>
 *   <ChatInterface />
 * </TabPanel>
 * ```
 */
export default function TabPanel({
  children,
  index,
  value,
  keepMounted = false,
  id = 'tab',
}: TabPanelProps) {
  const isActive = value === index

  // If not keeping mounted and not active, don't render
  if (!keepMounted && !isActive) {
    return null
  }

  return (
    <Box
      role="tabpanel"
      hidden={!isActive}
      id={`${id}-panel-${index}`}
      aria-labelledby={`${id}-${index}`}
      sx={{
        width: '100%',
        height: '100%',
        display: isActive ? 'flex' : 'none',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      {children}
    </Box>
  )
}

/**
 * Helper function to generate ARIA props for tab buttons
 * 
 * @param index - The index of the tab
 * @param id - Optional ID prefix (default: 'tab')
 * @returns Object with id, aria-controls, and aria-selected props
 * 
 * @example
 * ```tsx
 * <Tab label="Chat" {...a11yProps(0)} />
 * ```
 */
export function a11yProps(index: number, id: string = 'tab') {
  return {
    id: `${id}-${index}`,
    'aria-controls': `${id}-panel-${index}`,
  }
}
