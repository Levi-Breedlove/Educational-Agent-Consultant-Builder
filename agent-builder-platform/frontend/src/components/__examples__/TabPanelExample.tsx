import { useState } from 'react'
import { Box, Tabs, Tab, Paper, Typography } from '@mui/material'
import { Chat, Architecture, Code, CheckCircle } from '@mui/icons-material'
import TabPanel, { a11yProps } from '../TabPanel'

/**
 * TabPanel Example Component
 * 
 * Demonstrates the usage of TabPanel component with Material-UI Tabs.
 * This example shows a typical tabbed interface with icons and labels.
 * 
 * To use this example:
 * 1. Import it in your page/component
 * 2. Render it: <TabPanelExample />
 * 3. Customize the tabs and content as needed
 */
export default function TabPanelExample() {
  const [activeTab, setActiveTab] = useState(0)

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue)
  }

  return (
    <Box sx={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Tab Navigation */}
      <Paper sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs
          value={activeTab}
          onChange={handleChange}
          aria-label="agent builder tabs example"
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab
            icon={<Chat />}
            label="Chat"
            iconPosition="start"
            {...a11yProps(0, 'example')}
          />
          <Tab
            icon={<Architecture />}
            label="Architecture"
            iconPosition="start"
            {...a11yProps(1, 'example')}
          />
          <Tab
            icon={<Code />}
            label="Code"
            iconPosition="start"
            {...a11yProps(2, 'example')}
          />
          <Tab
            icon={<CheckCircle />}
            label="Confidence"
            iconPosition="start"
            {...a11yProps(3, 'example')}
          />
        </Tabs>
      </Paper>

      {/* Tab Content */}
      <Box sx={{ flex: 1, overflow: 'hidden', p: 2 }}>
        <TabPanel value={activeTab} index={0} id="example">
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h5" gutterBottom>
              Chat Interface
            </Typography>
            <Typography variant="body1" color="text.secondary">
              This is where the ChatInterface component would be rendered.
              The content is only mounted when this tab is active.
            </Typography>
          </Paper>
        </TabPanel>

        <TabPanel value={activeTab} index={1} id="example">
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h5" gutterBottom>
              Architecture Visualizer
            </Typography>
            <Typography variant="body1" color="text.secondary">
              This is where the ArchitectureVisualizer component would be rendered.
              It includes Mermaid diagrams and architecture templates.
            </Typography>
          </Paper>
        </TabPanel>

        <TabPanel value={activeTab} index={2} id="example" keepMounted>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h5" gutterBottom>
              Code Workspace
            </Typography>
            <Typography variant="body1" color="text.secondary">
              This is where the CodeWorkspace component would be rendered.
              Note: This tab uses keepMounted=true to preserve state when switching tabs.
            </Typography>
          </Paper>
        </TabPanel>

        <TabPanel value={activeTab} index={3} id="example">
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h5" gutterBottom>
              Confidence History
            </Typography>
            <Typography variant="body1" color="text.secondary">
              This is where the ConfidenceHistory component would be rendered.
              It shows detailed confidence tracking over time.
            </Typography>
          </Paper>
        </TabPanel>
      </Box>
    </Box>
  )
}
