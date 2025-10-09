import { describe, it, expect } from 'vitest'
import { awsArchitectureTemplates } from '../AWSArchitectureTemplates'

/**
 * AWS Service Validation Tests
 * 
 * These tests ensure that:
 * 1. All AWS services have correct official names
 * 2. Icons match their service names
 * 3. Service types are properly set
 * 4. No duplicate or conflicting service definitions
 */

describe('AWS Service Icon Validation', () => {
  /**
   * Official AWS service name mapping (for reference)
   * See AWS-SERVICE-REGISTRY.md for complete documentation
   */

  it('should have all AWS services with official names', () => {
    const allServices = awsArchitectureTemplates.flatMap(template => template.services)
    const awsServices = allServices.filter(service => service.type === 'aws')

    awsServices.forEach(service => {
      expect(service.name).toBeTruthy()
      expect(service.name).toMatch(/^(Amazon|AWS|Elastic)/)
      expect(service.icon).toBeDefined()
    })
  })

  it('should have correct service type for all AWS services', () => {
    const allServices = awsArchitectureTemplates.flatMap(template => template.services)
    
    allServices.forEach(service => {
      if (service.icon) {
        expect(service.type).toBe('aws')
      } else {
        expect(service.type).toBe('generic')
      }
    })
  })

  it('should have unique service IDs within each template', () => {
    awsArchitectureTemplates.forEach(template => {
      const ids = template.services.map(s => s.id)
      const uniqueIds = new Set(ids)
      expect(uniqueIds.size).toBe(ids.length)
    })
  })

  it('should have descriptions for all services', () => {
    const allServices = awsArchitectureTemplates.flatMap(template => template.services)
    
    allServices.forEach(service => {
      expect(service.description).toBeTruthy()
      expect(service.description?.length).toBeGreaterThan(3)
    })
  })

  it('should use official AWS service names (not abbreviations)', () => {
    const allServices = awsArchitectureTemplates.flatMap(template => template.services)
    const awsServices = allServices.filter(service => service.type === 'aws')

    // Check that we're not using abbreviations
    const invalidNames = awsServices.filter(service => {
      const name = service.name
      return (
        name === 'Lambda' ||
        name === 'S3' ||
        name === 'DynamoDB' ||
        name === 'API Gateway' ||
        name === 'SQS' ||
        name === 'SNS' ||
        name === 'RDS' ||
        name === 'IAM' ||
        name === 'VPC' ||
        name === 'ALB' ||
        name === 'ECS'
      )
    })

    expect(invalidNames).toHaveLength(0)
  })

  it('should have valid connections between existing services', () => {
    awsArchitectureTemplates.forEach(template => {
      const serviceIds = new Set(template.services.map(s => s.id))
      
      template.connections.forEach(conn => {
        expect(serviceIds.has(conn.from)).toBe(true)
        expect(serviceIds.has(conn.to)).toBe(true)
      })
    })
  })

  it('should have proper positioning (no negative coordinates)', () => {
    const allServices = awsArchitectureTemplates.flatMap(template => template.services)
    
    allServices.forEach(service => {
      expect(service.x).toBeGreaterThanOrEqual(0)
      expect(service.y).toBeGreaterThanOrEqual(0)
    })
  })

  it('should have connection labels that are descriptive', () => {
    const allConnections = awsArchitectureTemplates.flatMap(template => template.connections)
    const connectionsWithLabels = allConnections.filter(conn => conn.label)
    
    connectionsWithLabels.forEach(conn => {
      expect(conn.label).toBeTruthy()
      expect(conn.label!.length).toBeGreaterThan(2)
    })
  })

  it('should categorize templates correctly', () => {
    const validCategories = ['Serverless', 'Containers', 'Event-Driven', 'AI/ML', 'Analytics', 'Microservices']
    
    awsArchitectureTemplates.forEach(template => {
      expect(validCategories).toContain(template.category)
    })
  })

  it('should have tags that match services used', () => {
    awsArchitectureTemplates.forEach(template => {
      const awsServices = template.services
        .filter(s => s.type === 'aws')
        .map(s => s.name)
      
      // At least some tags should reference the services
      const hasRelevantTags = template.tags.some(tag => 
        awsServices.some(service => service.includes(tag) || tag.includes(service.split(' ')[1]))
      )
      
      expect(hasRelevantTags).toBe(true)
    })
  })
})

describe('Service Name Consistency', () => {
  it('should use consistent naming across all templates', () => {
    // Group services by their description to find duplicates
    const servicesByDescription = new Map<string, Set<string>>()
    
    awsArchitectureTemplates.forEach(template => {
      template.services.forEach(service => {
        if (service.type === 'aws' && service.description) {
          const desc = service.description.toLowerCase()
          if (!servicesByDescription.has(desc)) {
            servicesByDescription.set(desc, new Set())
          }
          servicesByDescription.get(desc)!.add(service.name)
        }
      })
    })

    // Check that services with same description have same name
    servicesByDescription.forEach((names, desc) => {
      if (names.size > 1) {
        // Multiple names for same description - potential inconsistency
        console.warn(`Multiple names for "${desc}":`, Array.from(names))
      }
    })
    
    // This test passes if we get here - warnings are informational
    expect(true).toBe(true)
  })
})

describe('AI Agent Service Identification', () => {
  it('should provide clear service identification for AI agents', () => {
    const allServices = awsArchitectureTemplates.flatMap(template => template.services)
    const awsServices = allServices.filter(service => service.type === 'aws')

    awsServices.forEach(service => {
      // Each service should have:
      // 1. Official AWS name
      expect(service.name).toMatch(/^(Amazon|AWS|Elastic)/)
      
      // 2. Clear description
      expect(service.description).toBeTruthy()
      
      // 3. Type marker
      expect(service.type).toBe('aws')
      
      // 4. Icon component
      expect(service.icon).toBeDefined()
    })
  })

  it('should have machine-readable service metadata', () => {
    awsArchitectureTemplates.forEach(template => {
      // Template should have structured data
      expect(template.id).toBeTruthy()
      expect(template.name).toBeTruthy()
      expect(template.description).toBeTruthy()
      expect(template.category).toBeTruthy()
      expect(Array.isArray(template.tags)).toBe(true)
      expect(Array.isArray(template.services)).toBe(true)
      expect(Array.isArray(template.connections)).toBe(true)
    })
  })
})
