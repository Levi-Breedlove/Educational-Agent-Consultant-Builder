# AWS Architecture Diagram - Center Alignment Fix

## Summary
Fixed connection line center point calculations so generic text boxes (Client, User, Event Source) align properly with AWS service icons.

## Problem
Connection lines were not centered correctly because the code used fixed center points that didn't account for different node sizes:
- AWS icons: 70px wide × 90px tall
- Generic boxes: 90px wide × 45px tall

This caused misalignment where lines connected to the wrong vertical position on generic boxes.

## Solution
Updated center point calculation to dynamically determine the center based on node type.

### Center Point Algorithm

**Horizontal Center (X-axis)**:
- AWS icons: `x + 35px` (70px width / 2)
- Generic boxes: `x + 45px` (90px width / 2)

**Vertical Center (Y-axis)**:
- AWS icons: `y + 45px` (90px height / 2)
- Generic boxes: `y + 22.5px` (45px height / 2)

### Code Changes

**AWSArchitectureDiagram.tsx**:
```typescript
// Before: Fixed center points
const x1 = fromService.x + 40
const y1 = fromService.y + 40

// After: Dynamic based on node type
const fromIsAWS = (fromService.type === 'aws' || (!fromService.type && fromService.icon)) && fromService.icon
const x1 = fromService.x + (fromIsAWS ? 35 : 45)
const y1 = fromService.y + (fromIsAWS ? 45 : 22.5)
```

**HybridArchitectureDiagram.tsx**:
```typescript
// Before: Incorrect generic box center
const fromCenterY = fromService.y + (fromService.type === 'aws' ? 55 : 30)

// After: Correct generic box center
const fromCenterY = fromService.y + (fromService.type === 'aws' ? 55 : 22.5)
```

## Files Updated
- `src/components/AWSArchitectureDiagram.tsx`
- `src/components/HybridArchitectureDiagram.tsx`

## Result
✅ Connection lines now connect to the exact center of both AWS icons and generic boxes
✅ Perfect vertical alignment across all node types
✅ Professional, balanced appearance
✅ No more offset or misaligned connections
✅ Works for all templates (Serverless API, ECS Fargate, Event-Driven, etc.)

## Visual Improvements
- "Event Source" box now aligns perfectly with "Amazon EventBridge" icon
- "Client" and "User" boxes align with their connected AWS services
- All connection lines flow smoothly from center to center
- Diagram looks polished and professional
