import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import TabPanel, { a11yProps } from '../TabPanel'

describe('TabPanel', () => {
  it('renders children when active', () => {
    render(
      <TabPanel value={0} index={0}>
        <div>Active Content</div>
      </TabPanel>
    )
    
    expect(screen.getByText('Active Content')).toBeInTheDocument()
    expect(screen.getByRole('tabpanel')).not.toHaveAttribute('hidden')
  })

  it('hides content when not active', () => {
    render(
      <TabPanel value={1} index={0}>
        <div>Inactive Content</div>
      </TabPanel>
    )
    
    // Content should not be rendered when keepMounted is false
    expect(screen.queryByText('Inactive Content')).not.toBeInTheDocument()
  })

  it('keeps content mounted when keepMounted is true', () => {
    render(
      <TabPanel value={1} index={0} keepMounted>
        <div>Mounted Content</div>
      </TabPanel>
    )
    
    const panel = screen.getByRole('tabpanel', { hidden: true })
    expect(panel).toHaveAttribute('hidden')
    expect(screen.getByText('Mounted Content')).toBeInTheDocument()
  })

  it('has correct ARIA attributes', () => {
    render(
      <TabPanel value={0} index={0} id="custom">
        <div>Content</div>
      </TabPanel>
    )
    
    const panel = screen.getByRole('tabpanel')
    expect(panel).toHaveAttribute('id', 'custom-panel-0')
    expect(panel).toHaveAttribute('aria-labelledby', 'custom-0')
  })

  it('uses default id when not provided', () => {
    render(
      <TabPanel value={2} index={2}>
        <div>Content</div>
      </TabPanel>
    )
    
    const panel = screen.getByRole('tabpanel')
    expect(panel).toHaveAttribute('id', 'tab-panel-2')
    expect(panel).toHaveAttribute('aria-labelledby', 'tab-2')
  })
})

describe('a11yProps', () => {
  it('generates correct props with default id', () => {
    const props = a11yProps(0)
    
    expect(props).toEqual({
      id: 'tab-0',
      'aria-controls': 'tab-panel-0',
    })
  })

  it('generates correct props with custom id', () => {
    const props = a11yProps(2, 'custom')
    
    expect(props).toEqual({
      id: 'custom-2',
      'aria-controls': 'custom-panel-2',
    })
  })
})
