import { Box, Container, Typography, Stack, Paper } from '@mui/material'
import ConfidenceDashboard, { type ConfidenceScore } from '../components/ConfidenceDashboard'

/**
 * Test page to verify ConfidenceDashboard color ranges
 * 
 * Color Ranges:
 * - Green (Success): >= 95% confidence
 * - Yellow (Warning): 85% - 94.9% confidence
 * - Red (Error): < 85% confidence
 */
export default function ConfidenceDashboardTestPage() {
  // Test case 1: Excellent confidence (>= 95%) - Should be GREEN
  const excellentScore: ConfidenceScore = {
    overallConfidence: 0.97,
    factors: {
      informationCompleteness: 0.98,
      requirementClarity: 0.97,
      technicalFeasibility: 0.96,
      validationCoverage: 0.97,
      riskAssessment: 0.96,
      userAlignment: 0.98,
    },
    confidenceBoosters: [
      'All requirements clearly defined',
      'Architecture validated against AWS Well-Architected Framework',
      'All dependencies identified and available',
    ],
    uncertaintyFactors: [],
    recommendedActions: [],
    meetsBaseline: true,
    timestamp: new Date().toISOString(),
  }

  // Test case 2: Good confidence (85-94%) - Should be YELLOW
  const goodScore: ConfidenceScore = {
    overallConfidence: 0.89,
    factors: {
      informationCompleteness: 0.92,
      requirementClarity: 0.88,
      technicalFeasibility: 0.90,
      validationCoverage: 0.87,
      riskAssessment: 0.88,
      userAlignment: 0.89,
    },
    confidenceBoosters: [
      'Core requirements identified',
      'Technical approach validated',
    ],
    uncertaintyFactors: [
      'Some edge cases need clarification',
      'Performance benchmarks not yet established',
    ],
    recommendedActions: [
      'Define performance SLAs',
      'Clarify edge case handling',
    ],
    meetsBaseline: false,
    timestamp: new Date().toISOString(),
  }

  // Test case 3: Low confidence (< 85%) - Should be RED
  const lowScore: ConfidenceScore = {
    overallConfidence: 0.78,
    factors: {
      informationCompleteness: 0.75,
      requirementClarity: 0.80,
      technicalFeasibility: 0.82,
      validationCoverage: 0.70,
      riskAssessment: 0.78,
      userAlignment: 0.83,
    },
    confidenceBoosters: [
      'Initial requirements gathered',
    ],
    uncertaintyFactors: [
      'Missing critical information about data sources',
      'Integration requirements unclear',
      'Security requirements not fully defined',
      'Performance requirements ambiguous',
    ],
    recommendedActions: [
      'Gather more information about data sources',
      'Define integration requirements',
      'Specify security requirements',
      'Establish performance benchmarks',
    ],
    meetsBaseline: false,
    timestamp: new Date().toISOString(),
  }

  // Test case 4: Edge case - Exactly 95% - Should be GREEN
  const edgeCase95: ConfidenceScore = {
    overallConfidence: 0.95,
    factors: {
      informationCompleteness: 0.95,
      requirementClarity: 0.95,
      technicalFeasibility: 0.95,
      validationCoverage: 0.95,
      riskAssessment: 0.95,
      userAlignment: 0.95,
    },
    confidenceBoosters: ['Meets baseline threshold'],
    uncertaintyFactors: [],
    recommendedActions: [],
    meetsBaseline: true,
    timestamp: new Date().toISOString(),
  }

  // Test case 5: Edge case - Exactly 85% - Should be YELLOW
  const edgeCase85: ConfidenceScore = {
    overallConfidence: 0.85,
    factors: {
      informationCompleteness: 0.85,
      requirementClarity: 0.85,
      technicalFeasibility: 0.85,
      validationCoverage: 0.85,
      riskAssessment: 0.85,
      userAlignment: 0.85,
    },
    confidenceBoosters: ['Minimum acceptable confidence'],
    uncertaintyFactors: ['At threshold boundary'],
    recommendedActions: ['Improve confidence to reach baseline'],
    meetsBaseline: false,
    timestamp: new Date().toISOString(),
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" gutterBottom>
        Confidence Dashboard Color Range Test
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        This page tests the ConfidenceDashboard component with different confidence levels
        to verify color coding is working correctly.
      </Typography>

      <Paper sx={{ p: 2, mb: 3, bgcolor: 'background.default' }}>
        <Typography variant="h6" gutterBottom>
          Color Range Specification:
        </Typography>
        <Stack spacing={1}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                width: 24,
                height: 24,
                bgcolor: 'success.main',
                borderRadius: 1,
              }}
            />
            <Typography>
              <strong>Green (Success):</strong> ≥ 95% confidence - Meets baseline, ready to proceed
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                width: 24,
                height: 24,
                bgcolor: 'warning.main',
                borderRadius: 1,
              }}
            />
            <Typography>
              <strong>Yellow (Warning):</strong> 85% - 94.9% confidence - Below baseline, needs improvement
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                width: 24,
                height: 24,
                bgcolor: 'error.main',
                borderRadius: 1,
              }}
            />
            <Typography>
              <strong>Red (Error):</strong> &lt; 85% confidence - Significantly below baseline, requires attention
            </Typography>
          </Box>
        </Stack>
      </Paper>

      <Stack spacing={4}>
        {/* Test Case 1: Excellent (Green) */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Test Case 1: Excellent Confidence (97%) - Expected: GREEN
          </Typography>
          <ConfidenceDashboard currentScore={excellentScore} showDetails={true} />
        </Box>

        {/* Test Case 2: Good (Yellow) */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Test Case 2: Good Confidence (89%) - Expected: YELLOW
          </Typography>
          <ConfidenceDashboard currentScore={goodScore} showDetails={true} />
        </Box>

        {/* Test Case 3: Low (Red) */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Test Case 3: Low Confidence (78%) - Expected: RED
          </Typography>
          <ConfidenceDashboard currentScore={lowScore} showDetails={true} />
        </Box>

        {/* Test Case 4: Edge Case 95% (Green) */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Test Case 4: Edge Case - Exactly 95% - Expected: GREEN
          </Typography>
          <ConfidenceDashboard currentScore={edgeCase95} showDetails={true} />
        </Box>

        {/* Test Case 5: Edge Case 85% (Yellow) */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Test Case 5: Edge Case - Exactly 85% - Expected: YELLOW
          </Typography>
          <ConfidenceDashboard currentScore={edgeCase85} showDetails={true} />
        </Box>
      </Stack>

      <Box sx={{ mt: 4, p: 2, bgcolor: 'info.main', color: 'info.contrastText', borderRadius: 1 }}>
        <Typography variant="body2">
          <strong>How to verify:</strong> Check that each dashboard displays the correct color for its
          confidence level. The overall confidence percentage, progress bar, and individual factor bars
          should all use the appropriate color (green, yellow, or red) based on the ranges above.
        </Typography>
      </Box>
    </Container>
  )
}
