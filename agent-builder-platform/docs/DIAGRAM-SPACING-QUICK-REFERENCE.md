# AWS Diagram Spacing - Quick Reference Card

## 🎯 Core Rules (Memorize These!)

### Icon Dimensions
```
Width:  90px
Height: 110px (70px icon + 40px label)
```

### Minimum Spacing
```
Vertical:   140px (110px + 30px clearance)
Horizontal: 150px (90px + 60px clearance)
```

### Standard Coordinates

**X-Coordinates (Horizontal):**
```
50, 200, 350, 500, 650, 800
```

**Y-Coordinates (Vertical):**
```
60, 200, 340, 480, 620, 760
```

### Position Formulas
```python
x = 50 + (column_index * 150)
y = 60 + (row_index * 140)
```

## 📐 Layout Grid

```
        Col 0   Col 1   Col 2   Col 3   Col 4   Col 5
        x=50    x=200   x=350   x=500   x=650   x=800
        ↓       ↓       ↓       ↓       ↓       ↓
Row 0   [60]    [60]    [60]    [60]    [60]    [60]    ← Supporting
y=60    
        
Row 1   [200]   [200]   [200]   [200]   [200]   [200]   ← Main Flow
y=200   
        
Row 2   [340]   [340]   [340]   [340]   [340]   [340]   ← Data Layer
y=340   
        
Row 3   [480]   [480]   [480]   [480]   [480]   [480]   ← Additional
y=480   
```

## ✅ Valid Example

```json
{
  "services": [
    {"id": "apigw", "x": 50, "y": 200},
    {"id": "lambda", "x": 200, "y": 200},
    {"id": "dynamodb", "x": 350, "y": 60},
    {"id": "s3", "x": 350, "y": 340}
  ]
}
```

## ❌ Invalid Example

```json
{
  "services": [
    {"id": "s1", "x": 100, "y": 150},  // ❌ Not standard coordinates
    {"id": "s2", "x": 100, "y": 200}   // ❌ Only 50px gap - OVERLAP!
  ]
}
```

## 🔍 Quick Validation

### Check 1: Standard Coordinates
```python
valid_x = [50, 200, 350, 500, 650, 800]
valid_y = [60, 200, 340, 480, 620, 760]

assert service['x'] in valid_x
assert service['y'] in valid_y
```

### Check 2: Minimum Spacing
```python
# Same column (vertical spacing)
if abs(s1['x'] - s2['x']) < 90:
    assert abs(s1['y'] - s2['y']) >= 140

# Same row (horizontal spacing)
if abs(s1['y'] - s2['y']) < 110:
    assert abs(s1['x'] - s2['x']) >= 150
```

## 🎨 Common Patterns

### Pattern 1: Simple Flow (Horizontal)
```
[Client] → [API Gateway] → [Lambda] → [Database]
x=50        x=200           x=350      x=500
y=200       y=200           y=200      y=200
```

### Pattern 2: Layered (Vertical)
```
         [IAM]
         x=200, y=60
            ↓
[Client] → [Lambda] → [Database]
x=50       x=200       x=350
y=200      y=200       y=200
            ↓
      [CloudWatch]
      x=200, y=340
```

### Pattern 3: Microservices
```
                [Auth DB]    [User DB]    [Order DB]
                x=350        x=350        x=350
                y=60         y=200        y=340
                   ↑            ↑            ↑
[API GW] → [Auth λ]    [User λ]    [Order λ]
x=50       x=200       x=200       x=200
y=200      y=60        y=200       y=340
```

## 🚀 Quick Start for AI Agents

### Step 1: Plan Layout
```
Row 0 (y=60):  Supporting services (IAM, Secrets, etc.)
Row 1 (y=200): Main application flow
Row 2 (y=340): Data layer (databases, storage)
Row 3 (y=480): Monitoring, logging
```

### Step 2: Assign Positions
```python
services = []

# Row 1 - Main flow
services.append({"id": "apigw", "x": 50, "y": 200})
services.append({"id": "lambda", "x": 200, "y": 200})

# Row 0 - Supporting
services.append({"id": "iam", "x": 200, "y": 60})

# Row 2 - Data
services.append({"id": "dynamodb", "x": 350, "y": 340})
```

### Step 3: Validate
```python
from utils.diagram_validator import DiagramValidator

is_valid, errors = DiagramValidator.validate_diagram(services)
if not is_valid:
    services = DiagramValidator.auto_fix_spacing(services)
```

## 📋 Checklist

Before submitting any diagram:

- [ ] All x-coordinates are from: 50, 200, 350, 500, 650, 800
- [ ] All y-coordinates are from: 60, 200, 340, 480, 620, 760
- [ ] No two services have the same (x, y) position
- [ ] Vertical spacing ≥ 140px
- [ ] Horizontal spacing ≥ 150px
- [ ] Validation passed

## 🎯 Zero Tolerance

**Never allow:**
- ❌ Random coordinates (e.g., x=127, y=189)
- ❌ Overlapping icons
- ❌ Spacing < 140px vertical
- ❌ Spacing < 150px horizontal
- ❌ Unvalidated diagrams

## 📚 Full Documentation

For complete details, see:
- `docs/AWS-DIAGRAM-GENERATION-STANDARDS.md` - Technical specification
- `prompt_engineering/diagram_generation_prompt.md` - AI agent template
- `frontend/DIAGRAM-SPACING-STANDARDS-IMPLEMENTATION.md` - Implementation guide

---

**Print this card and keep it handy when generating diagrams!**

**Version**: 1.0 | **Last Updated**: October 8, 2025
