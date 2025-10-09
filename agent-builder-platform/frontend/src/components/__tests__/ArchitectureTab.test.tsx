import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ThemeProvider, createTheme } from '@mui/material'
import ArchitectureTab from '../ArchitectureTab'
import { awsArchitectureTemplates } from '../AWSArchitectureTemplates'

const theme = createTheme()

const renderWithTheme = (component: React.ReactElement) => {
  return render(<ThemeProvider theme={theme}>{component}</ThemeProvider>)
}

describe('ArchitectureTab', () => {
  it('renders empty state when no template is provided', () => {
    renderWithTheme(<ArchitectureTab />)
    
    expect(screen.getByText('No Architecture Diagram Yet')).toBeInTheDocument()
    expect(screen.getByText(/Your AWS architecture diagram will appear here/)).toBeInTheDocument()
  })

  it('renders AWS architecture diagram when template is provided', () => {
    const template = awsArchitectureTemplates[0]
    renderWithTheme(<ArchitectureTab generatedTemplate={template} />)
    
    expect(screen.queryByText('No Architecture Diagram Yet')).not.toBeInTheDocument()
    expect(screen.getByText(template.name)).toBeInTheDocument()
  })

  it('opens AWS templates drawer when Browse Templates is clicked', async () => {
    renderWithTheme(<ArchitectureTab />)
    
    // Get all Browse Templates buttons (there are 2: one in header, one in empty state)
    const browseButtons = screen.getAllByRole('button', { name: /Browse.*Templates/i })
    fireEvent.click(browseButtons[0])
    
    await waitFor(() => {
      expect(screen.getByText('AWS Architecture Templates')).toBeInTheDocument()
    })
  })

  it('displays professional AWS icons message in templates drawer', async () => {
    renderWithTheme(<ArchitectureTab />)
    
    const browseButtons = screen.getAllByRole('button', { name: /Browse.*Templates/i })
    fireEvent.click(browseButtons[0])
    
    await waitFor(() => {
      expect(screen.getByText(/official AWS service icons/i)).toBeInTheDocument()
    })
  })

  it('closes templates drawer when close button is clicked', async () => {
    renderWithTheme(<ArchitectureTab />)
    
    // Open drawer
    const browseButtons = screen.getAllByRole('button', { name: /Browse.*Templates/i })
    fireEvent.click(browseButtons[0])
    
    await waitFor(() => {
      expect(screen.getByText('AWS Architecture Templates')).toBeInTheDocument()
    })
    
    // Close drawer by clicking backdrop
    const backdrop = document.querySelector('.MuiBackdrop-root')
    if (backdrop) {
      fireEvent.click(backdrop)
    }
    
    await waitFor(() => {
      expect(screen.queryByText('AWS Architecture Templates')).not.toBeInTheDocument()
    })
  })

  it('calls onTemplateUpdate when template is selected', async () => {
    const onTemplateUpdate = vi.fn()
    renderWithTheme(<ArchitectureTab onTemplateUpdate={onTemplateUpdate} />)
    
    // Open drawer
    const browseButtons = screen.getAllByRole('button', { name: /Browse.*Templates/i })
    fireEvent.click(browseButtons[0])
    
    await waitFor(() => {
      expect(screen.getByText('AWS Architecture Templates')).toBeInTheDocument()
    })
    
    // Select a template (find "Use Template" button)
    const useTemplateButtons = screen.getAllByRole('button', { name: /Use Template/i })
    fireEvent.click(useTemplateButtons[0])
    
    await waitFor(() => {
      expect(onTemplateUpdate).toHaveBeenCalled()
    })
  })

  it('displays selected template name in header', async () => {
    renderWithTheme(<ArchitectureTab />)
    
    // Open drawer
    const browseButtons = screen.getAllByRole('button', { name: /Browse.*Templates/i })
    fireEvent.click(browseButtons[0])
    
    await waitFor(() => {
      expect(screen.getByText('Serverless REST API')).toBeInTheDocument()
    })
    
    // Select template
    const useTemplateButtons = screen.getAllByRole('button', { name: /Use Template/i })
    fireEvent.click(useTemplateButtons[0])
    
    await waitFor(() => {
      expect(screen.getByText(/Template: Serverless REST API/)).toBeInTheDocument()
    })
  })

  it('shows professional AWS architecture info when diagram is present', () => {
    const template = awsArchitectureTemplates[0]
    renderWithTheme(<ArchitectureTab generatedTemplate={template} />)
    
    expect(screen.getByText(/Professional AWS Architecture:/)).toBeInTheDocument()
    expect(screen.getByText(/official AWS service icons/)).toBeInTheDocument()
  })

  it('displays all AWS architecture templates', async () => {
    renderWithTheme(<ArchitectureTab />)
    
    const browseButtons = screen.getAllByRole('button', { name: /Browse.*Templates/i })
    fireEvent.click(browseButtons[0])
    
    await waitFor(() => {
      // Check that all templates are displayed
      expect(screen.getByText('Serverless REST API')).toBeInTheDocument()
      expect(screen.getByText('ECS Fargate Application')).toBeInTheDocument()
      expect(screen.getByText('Event-Driven Architecture')).toBeInTheDocument()
      expect(screen.getByText('AI Agent with Bedrock')).toBeInTheDocument()
      expect(screen.getByText('Data Analytics Pipeline')).toBeInTheDocument()
      expect(screen.getByText('Microservices Architecture')).toBeInTheDocument()
    })
  })
})
