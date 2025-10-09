import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import CodeTab from '../CodeTab'
import workflowReducer, { type WorkflowPhase, type PhaseStatus } from '../../store/slices/workflowSlice'

// Helper to create a test store
const createTestStore = (workflowState: Partial<{
    currentPhase: WorkflowPhase
    phases: Record<WorkflowPhase, PhaseStatus>
    progress: number
    startTime: number | null
    elapsedTime: number
}> = {}) => {
    return configureStore({
        reducer: {
            workflow: workflowReducer,
        },
        preloadedState: {
            workflow: {
                currentPhase: 'requirements' as WorkflowPhase,
                phases: {
                    requirements: 'in_progress' as PhaseStatus,
                    architecture: 'pending' as PhaseStatus,
                    implementation: 'pending' as PhaseStatus,
                    testing: 'pending' as PhaseStatus,
                    deployment: 'pending' as PhaseStatus,
                },
                progress: 0,
                startTime: null,
                elapsedTime: 0,
                ...workflowState,
            },
        },
    })
}

describe('CodeTab', () => {
    it('renders empty state when no code is generated', () => {
        const store = createTestStore()

        render(
            <Provider store={store}>
                <CodeTab />
            </Provider>
        )

        expect(screen.getByText('No Code Generated Yet')).toBeInTheDocument()
        expect(screen.getByText(/Complete the requirements and architecture phases/)).toBeInTheDocument()
    })

    it('renders loading state when implementation is in progress', () => {
        const store = createTestStore({
            currentPhase: 'implementation',
            phases: {
                requirements: 'completed',
                architecture: 'completed',
                implementation: 'in_progress',
                testing: 'pending',
                deployment: 'pending',
            },
        })

        render(
            <Provider store={store}>
                <CodeTab />
            </Provider>
        )

        expect(screen.getByText('Generating Your Agent Code...')).toBeInTheDocument()
        expect(screen.getByText(/The Implementation Guide is creating/)).toBeInTheDocument()
    })

    it('renders code workspace when implementation is complete', () => {
        const store = createTestStore({
            currentPhase: 'testing',
            phases: {
                requirements: 'completed',
                architecture: 'completed',
                implementation: 'completed',
                testing: 'in_progress',
                deployment: 'pending',
            },
        })

        render(
            <Provider store={store}>
                <CodeTab />
            </Provider>
        )

        expect(screen.getByText('Code Generated Successfully')).toBeInTheDocument()
        expect(screen.getByText('Generated Agent Code')).toBeInTheDocument()
    })

    it('displays current phase in empty state alert', () => {
        const store = createTestStore({
            currentPhase: 'architecture',
        })

        render(
            <Provider store={store}>
                <CodeTab />
            </Provider>
        )

        expect(screen.getByText(/Current Phase: architecture/)).toBeInTheDocument()
    })
})
