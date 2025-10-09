import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { ConfidenceDashboard } from '../ConfidenceDashboard'
import type { ConfidenceScore } from '../ConfidenceDashboard'

describe('ConfidenceDashboard', () => {
  const mockScore: ConfidenceScore = {
    overallConfidence: 0.96,
    factors: {
      informationCompleteness: 0.95,
      requirementClarity: 0.97,
      technicalFeasibility: 0.98,
      validationCoverage: 0.94,
      riskAssessment: 0.96,
      userAlignment: 0.95,
    },
    confidenceBoosters: [
      'Clear requirements provided',
      'All technical constraints identified',
    ],
    uncertaintyFactors: [
      'Performance requirements not specified',
    ],
    recommendedActions: [
      'Clarify expected user load',
    ],
    meetsBaseline: true,
    timestamp: new Date().toISOString(),
  }

  it('renders confidence score', () => {
    render(<ConfidenceDashboard currentScore={mockScore} />)
    const scores = screen.getAllByText('96.0%')
    expect(scores.length).toBeGreaterThan(0)
    expect(scores[0]).toBeInTheDocument()
  })

  it('shows baseline status when above 95%', () => {
    render(<ConfidenceDashboard currentScore={mockScore} />)
    expect(screen.queryByText(/Below Baseline Threshold/)).not.toBeInTheDocument()
  })

  it('shows warning when below baseline', () => {
    const lowScore = { ...mockScore, overallConfidence: 0.92, meetsBaseline: false }
    render(<ConfidenceDashboard currentScore={lowScore} />)
    expect(screen.getByText(/Below Baseline Threshold/)).toBeInTheDocument()
  })

  it('displays confidence factors', () => {
    render(<ConfidenceDashboard currentScore={mockScore} showDetails={true} />)
    expect(screen.getByText(/Information Completeness/)).toBeInTheDocument()
    expect(screen.getByText(/Requirement Clarity/)).toBeInTheDocument()
  })

  it('shows confidence boosters', () => {
    render(<ConfidenceDashboard currentScore={mockScore} showDetails={true} />)
    expect(screen.getByText('Clear requirements provided')).toBeInTheDocument()
  })

  it('shows uncertainty factors', () => {
    render(<ConfidenceDashboard currentScore={mockScore} showDetails={true} />)
    expect(screen.getByText('Performance requirements not specified')).toBeInTheDocument()
  })

  it('shows recommended actions', () => {
    render(<ConfidenceDashboard currentScore={mockScore} showDetails={true} />)
    expect(screen.getByText('Clarify expected user load')).toBeInTheDocument()
  })
})
