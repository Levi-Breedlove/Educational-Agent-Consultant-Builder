#!/usr/bin/env python3
"""
Consolidate ALL AWS icons from AWSServiceIconRegistry.tsx
and create a complete exportable registry for diagrams.
"""

import re

# Read the main registry
with open('src/components/AWSServiceIconRegistry.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all import statements
import_pattern = r'^import (Architecture\w+|Resource\w+) from [\'"]([^\'"]+)[\'"]'
imports = re.findall(import_pattern, content, re.MULTILINE)

print(f"Found {len(imports)} icon imports")

# Extract all registry entries
registry_pattern = r"  '([^']+)': \{[^}]+icon: (\w+),"
registry_entries = re.findall(registry_pattern, content)

print(f"Found {len(registry_entries)} registry entries")

# Generate the complete file
output = """/**
 * COMPLETE AWS SERVICE ICON REGISTRY - ALL ICONS EXPORTED
 * 
 * This file consolidates ALL AWS service icons from the main registry
 * and exports them for use in architecture diagrams.
 * 
 * Total Icons: """ + str(len(imports)) + """
 * Registry Entries: """ + str(len(registry_entries)) + """
 * 
 * Usage:
 * 1. Direct import: import { ArchitectureServiceAWSLambda } from './AWSServiceIcons'
 * 2. Registry object: import { awsServiceRegistry } from './AWSServiceIcons'
 * 3. Icon by ID: awsServiceRegistry['lambda'].icon
 */

import type { ComponentType } from 'react'

// ============================================================================
// ALL AWS SERVICE ICON IMPORTS
// ============================================================================

"""

# Add all imports
for icon_name, icon_path in imports:
    output += f"import {icon_name} from '{icon_path}'\n"

output += """
// ============================================================================
// EXPORT ALL ICONS INDIVIDUALLY
// ============================================================================

export {
"""

# Export all icons
for icon_name, _ in imports:
    output += f"  {icon_name},\n"

output += """}

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface AWSServiceDefinition {
  id: string
  name: string
  officialName: string
  icon: ComponentType
  category: string
  description: string
  useCases: string[]
  tags: string[]
}

// ============================================================================
// COMPLETE SERVICE REGISTRY (from main registry)
// ============================================================================

// Re-export the complete registry from the main file
export { awsServiceRegistry } from './AWSServiceIconRegistry'

// ============================================================================
// ICON LOOKUP BY NAME (for convenience)
// ============================================================================

export const iconsByName = {
"""

# Create icon lookup by service ID
for service_id, icon_name in registry_entries:
    output += f"  '{service_id}': {icon_name},\n"

output += """}

export default iconsByName
"""

# Write the output
with open('src/components/AWSServiceIcons.tsx', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"\n✅ Created AWSServiceIcons.tsx with {len(imports)} icons")
print(f"✅ All icons exported individually")
print(f"✅ Registry with {len(registry_entries)} services")
print(f"\n📦 Usage:")
print(f"   import {{ ArchitectureServiceAWSLambda }} from './AWSServiceIcons'")
print(f"   import {{ awsServiceRegistry }} from './AWSServiceIcons'")
print(f"   import {{ iconsByName }} from './AWSServiceIcons'")
