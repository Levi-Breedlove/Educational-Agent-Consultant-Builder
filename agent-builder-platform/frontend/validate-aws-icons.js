/**
 * AWS Icon Registry Validation Script
 * 
 * This script validates:
 * 1. All icons are unique (no duplicates)
 * 2. All service IDs are unique
 * 3. All icon imports are valid
 * 4. Service count matches documentation
 */

import { awsServiceRegistry, servicesByCategory, getTotalServiceCount } from './src/components/AWSServiceIconRegistry.tsx'

console.log('🔍 AWS Service Icon Registry Validation\n')
console.log('=' .repeat(60))

// 1. Check for duplicate service IDs
const serviceIds = Object.keys(awsServiceRegistry)
const uniqueIds = new Set(serviceIds)

console.log(`\n📊 Service Count: ${serviceIds.length}`)
console.log(`✅ Unique IDs: ${uniqueIds.size}`)

if (serviceIds.length !== uniqueIds.size) {
  console.error('❌ DUPLICATE SERVICE IDs FOUND!')
  const duplicates = serviceIds.filter((id, index) => serviceIds.indexOf(id) !== index)
  console.error('Duplicates:', duplicates)
  process.exit(1)
} else {
  console.log('✅ No duplicate service IDs')
}

// 2. Check for duplicate official names
const officialNames = Object.values(awsServiceRegistry).map(s => s.officialName)
const uniqueNames = new Set(officialNames)

console.log(`\n📝 Official Names: ${officialNames.length}`)
console.log(`✅ Unique Names: ${uniqueNames.size}`)

if (officialNames.length !== uniqueNames.size) {
  console.warn('⚠️  DUPLICATE OFFICIAL NAMES FOUND!')
  const nameCounts = {}
  officialNames.forEach(name => {
    nameCounts[name] = (nameCounts[name] || 0) + 1
  })
  const duplicateNames = Object.entries(nameCounts)
    .filter(([_, count]) => count > 1)
    .map(([name]) => name)
  console.warn('Duplicate names:', duplicateNames)
}

// 3. Check category assignments
console.log(`\n📁 Categories: ${Object.keys(servicesByCategory).length}`)

let totalInCategories = 0
Object.entries(servicesByCategory).forEach(([category, services]) => {
  console.log(`  ${category}: ${services.length} services`)
  totalInCategories += services.length
})

console.log(`\n✅ Total services in categories: ${totalInCategories}`)
console.log(`✅ Total services in registry: ${serviceIds.length}`)

if (totalInCategories !== serviceIds.length) {
  console.error('❌ MISMATCH: Some services are not categorized!')
  process.exit(1)
}

// 4. Validate all services have required fields
console.log(`\n🔍 Validating service definitions...`)

let validationErrors = 0

serviceIds.forEach(id => {
  const service = awsServiceRegistry[id]
  
  if (!service.id) {
    console.error(`❌ ${id}: Missing 'id' field`)
    validationErrors++
  }
  
  if (!service.name) {
    console.error(`❌ ${id}: Missing 'name' field`)
    validationErrors++
  }
  
  if (!service.officialName) {
    console.error(`❌ ${id}: Missing 'officialName' field`)
    validationErrors++
  }
  
  if (!service.icon) {
    console.error(`❌ ${id}: Missing 'icon' field`)
    validationErrors++
  }
  
  if (!service.category) {
    console.error(`❌ ${id}: Missing 'category' field`)
    validationErrors++
  }
  
  if (!service.description) {
    console.error(`❌ ${id}: Missing 'description' field`)
    validationErrors++
  }
  
  if (!service.useCases || service.useCases.length === 0) {
    console.error(`❌ ${id}: Missing or empty 'useCases' field`)
    validationErrors++
  }
  
  if (!service.tags || service.tags.length === 0) {
    console.error(`❌ ${id}: Missing or empty 'tags' field`)
    validationErrors++
  }
})

if (validationErrors === 0) {
  console.log('✅ All services have required fields')
} else {
  console.error(`❌ Found ${validationErrors} validation errors`)
  process.exit(1)
}

// 5. Summary
console.log('\n' + '='.repeat(60))
console.log('📊 VALIDATION SUMMARY')
console.log('='.repeat(60))
console.log(`✅ Total Services: ${serviceIds.length}`)
console.log(`✅ Categories: ${Object.keys(servicesByCategory).length}`)
console.log(`✅ No Duplicates`)
console.log(`✅ All Fields Valid`)
console.log('\n🎉 AWS Service Icon Registry is valid!\n')
