import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ThemeProvider, createTheme } from '@mui/material'
import ConfidenceTab from '../ConfidenceTab'
import type { ConfidenceScore } from '../ConfidenceDashboard'
import type { ConfidenceHistoryPoint } from '../ConfidenceHistory'

const theme = createTheme()

const mockConfidenceScore: ConfidenceScore = {
    overallConfidence: 0.96,
    factors: {
        informationCompleteness: 0.95,
        requirementClarity: 0.98,
        technicalFeasibility: 0.97,
        validationCoverage: 0.94,
        riskAssessment: 0.96,
        userAlignment: 0.95,
    },
    confidenceBoosters: [
        'Clear requirements provided',
        'Architecture validated',
    ],
    uncertaintyFactors: [
        'Performance benchmarks pending',
    ],
    recommendedActions: [
        'Define performance SLAs',
    ],
    meetsBaseline: true,
    timestamp: new Date().toISOString(),
}

const mockHistory: ConfidenceHistoryPoint[] = [
    { timestamp: new Date(Date.now() - 300000).toISOString(), confidence: 0.88, phase: 'requirements' },
    { timestamp: new Date(Date.now() - 240000).toISOString(), confidence: 0.91, phase: 'requirements' },
    { timestamp: new Date(Date.now() - 180000).toISOString(), confidence: 0.93, phase: 'architecture' },
    { timestamp: new Date(Date.now() - 120000).toISOString(), confidence: 0.95, phase: 'architecture' },
    { timestamp: new Date(Date.now() - 60000).toISOString(), confidence: 0.96, phase: 'implementation' },
]

describe('ConfidenceTab', () => {
    it('renders confidence analysis header', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        expect(screen.getByText('Confidence Analysis')).toBeInTheDocument()
        expect(screen.getByText(/Detailed confidence history with trends/)).toBeInTheDocument()
    })

    it('displays filters section', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        expect(screen.getByText('Filters')).toBeInTheDocument()
        expect(screen.getByLabelText('Phase')).toBeInTheDocument()
        expect(screen.getByLabelText('Date Range')).toBeInTheDocument()
    })

    it('displays insights summary', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        expect(screen.getByText('Insights')).toBeInTheDocument()
        expect(screen.getAllByText('Average').length).toBeGreaterThan(0)
        expect(screen.getByText('Range')).toBeInTheDocument()
        expect(screen.getByText('Volatility')).toBeInTheDocument()
        expect(screen.getByText('Change Rate')).toBeInTheDocument()
    })

    it('displays current confidence factors', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        expect(screen.getByText('Current Confidence Factors')).toBeInTheDocument()
        expect(screen.getByText('Information Completeness')).toBeInTheDocument()
        expect(screen.getByText('Requirement Clarity')).toBeInTheDocument()
        expect(screen.getByText('Technical Feasibility')).toBeInTheDocument()
        expect(screen.getByText('Validation Coverage')).toBeInTheDocument()
        expect(screen.getByText('Risk Assessment')).toBeInTheDocument()
        expect(screen.getByText('User Alignment')).toBeInTheDocument()
    })

    it('filters history by phase', async () => {
        const user = userEvent.setup()
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        // Open phase filter
        const phaseSelect = screen.getByLabelText('Phase')
        await user.click(phaseSelect)

        // Select requirements phase
        const requirementsOption = screen.getByRole('option', { name: /requirements/i })
        await user.click(requirementsOption)

        // Check that filter is active
        expect(screen.getByText(/Filters Active/)).toBeInTheDocument()
        expect(screen.getByText(/Phase: requirements/)).toBeInTheDocument()
    })

    it('filters history by date range', async () => {
        const user = userEvent.setup()
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        // Open date range filter
        const dateRangeSelect = screen.getByLabelText('Date Range')
        await user.click(dateRangeSelect)

        // Select last hour
        const lastHourOption = screen.getByRole('option', { name: /Last Hour/i })
        await user.click(lastHourOption)

        // Check that filter is active
        expect(screen.getByText(/Filters Active/)).toBeInTheDocument()
        expect(screen.getByText(/Date range: 1h/)).toBeInTheDocument()
    })

    it('shows improving trend insight', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        expect(screen.getByText('Improving')).toBeInTheDocument()
        expect(screen.getByText(/Confidence is improving over time/)).toBeInTheDocument()
    })

    it('shows appropriate confidence alerts based on average', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        // With history average of 92.6%, we should see the below baseline warning
        expect(screen.getByText(/Confidence is below the 95% baseline but above 85%/)).toBeInTheDocument()
    })

    it('displays empty state when no history', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={[]} />
            </ThemeProvider>
        )

        expect(screen.getByText('No Confidence History Yet')).toBeInTheDocument()
        expect(screen.getByText(/Confidence tracking will appear as you progress/)).toBeInTheDocument()
    })

    it('calculates insights correctly', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        // Average should be around 92.6% - use getAllByText since it appears in multiple places
        const avgTexts = screen.getAllByText(/92\.\d%/)
        expect(avgTexts.length).toBeGreaterThan(0)

        // Range should be 88.0% - 96.0%
        expect(screen.getByText(/88\.0% - 96\.0%/)).toBeInTheDocument()
    })

    it('shows all available phases in filter', async () => {
        const user = userEvent.setup()
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        // Open phase filter
        const phaseSelect = screen.getByLabelText('Phase')
        await user.click(phaseSelect)

        // Check that all phases are available
        expect(screen.getByRole('option', { name: /All Phases/i })).toBeInTheDocument()
        expect(screen.getByRole('option', { name: /requirements/i })).toBeInTheDocument()
        expect(screen.getByRole('option', { name: /architecture/i })).toBeInTheDocument()
        expect(screen.getByRole('option', { name: /implementation/i })).toBeInTheDocument()
    })

    it('displays factor percentages correctly', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        // Check that all factor values are displayed - use getAllByText since values may appear multiple times
        expect(screen.getAllByText('95.0%').length).toBeGreaterThan(0) // Information Completeness
        expect(screen.getAllByText('98.0%').length).toBeGreaterThan(0) // Requirement Clarity
        expect(screen.getAllByText('97.0%').length).toBeGreaterThan(0) // Technical Feasibility
        expect(screen.getAllByText('94.0%').length).toBeGreaterThan(0) // Validation Coverage
        expect(screen.getAllByText('96.0%').length).toBeGreaterThan(0) // Risk Assessment & User Alignment
    })

    it('is accessible', () => {
        render(
            <ThemeProvider theme={theme}>
                <ConfidenceTab currentScore={mockConfidenceScore} history={mockHistory} />
            </ThemeProvider>
        )

        // Check for proper ARIA labels
        expect(screen.getByLabelText('Phase')).toBeInTheDocument()
        expect(screen.getByLabelText('Date Range')).toBeInTheDocument()

        // Check for proper heading structure
        const headings = screen.getAllByRole('heading')
        expect(headings.length).toBeGreaterThan(0)
    })
})
