/**
 * AWS SERVICE ICONS - COMPLETE EXPORT
 * 
 * This file re-exports ALL 116 AWS service icons from the main registry
 * for easy use in architecture diagrams.
 * 
 * Usage Examples:
 * 
 * 1. Use the complete registry:
 *    import { awsServiceRegistry } from './AWSServiceIcons'
 *    const lambdaIcon = awsServiceRegistry['lambda'].icon
 * 
 * 2. Direct icon access by service ID:
 *    import { getIconByServiceId } from './AWSServiceIcons'
 *    const icon = getIconByServiceId('lambda')
 * 
 * Total Services: 108
 * Total Icons: 116 (includes generic resources)
 */

import { awsServiceRegistry, type AWSServiceDefinition } from './AWSServiceIconRegistry'
import type { ComponentType } from 'react'

// Re-export everything from the main registry
export { awsServiceRegistry }
export type { AWSServiceDefinition }

/**
 * Get icon component by service ID
 * @param serviceId - The service ID (e.g., 'lambda', 's3', 'dynamodb')
 * @returns The icon component or undefined if not found
 */
export function getIconByServiceId(serviceId: string): ComponentType | undefined {
  return awsServiceRegistry[serviceId]?.icon
}

/**
 * Get all available service IDs
 * @returns Array of all service IDs
 */
export function getAllServiceIds(): string[] {
  return Object.keys(awsServiceRegistry)
}

/**
 * Search services by category
 * @param category - Category name (e.g., 'Compute', 'Storage', 'Database')
 * @returns Array of services in that category
 */
export function getServicesByCategory(category: string): AWSServiceDefinition[] {
  return Object.values(awsServiceRegistry).filter(
    (service) => service.category === category
  )
}

/**
 * Search services by tag
 * @param tag - Tag to search for
 * @returns Array of services with that tag
 */
export function getServicesByTag(tag: string): AWSServiceDefinition[] {
  return Object.values(awsServiceRegistry).filter(
    (service) => service.tags.includes(tag)
  )
}

// Export default for convenience
export default awsServiceRegistry
