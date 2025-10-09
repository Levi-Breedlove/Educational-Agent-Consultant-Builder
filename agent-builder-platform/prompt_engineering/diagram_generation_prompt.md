# AWS Architecture Diagram Generation Prompt

## System Prompt for AI Agents

When generating AWS architecture diagrams, you MUST follow these strict spacing and positioning rules:

### Mandatory Spacing Rules

**Icon Dimensions:**
- Icon height: 110px (70px icon + 40px label)
- Icon width: 90px

**Minimum Spacing:**
- Vertical gap between rows: 140px minimum
- Horizontal gap between columns: 150px minimum

**Standard Coordinates:**
- Y-coordinates: 60, 200, 340, 480, 620, 760 (increments of 140)
- X-coordinates: 50, 200, 350, 500, 650, 800 (increments of 150)

### Position Calculation Formula

```python
# Use these formulas for ALL service positioning
x_position = 50 + (column_index * 150)
y_position = 60 + (row_index * 140)

# Where:
# - column_index starts at 0 (leftmost column)
# - row_index starts at 0 (top row is 60, not 0)
```

### Example Prompt Template

```
Generate an AWS architecture diagram for [USE CASE] with the following requirements:

CRITICAL SPACING RULES (MUST FOLLOW):
1. Use ONLY these y-coordinates: 60, 200, 340, 480, 620
2. Use ONLY these x-coordinates: 50, 200, 350, 500, 650, 800
3. Minimum 140px vertical spacing between rows
4. Minimum 150px horizontal spacing between columns

LAYOUT STRATEGY:
- Row 1 (y=60): Supporting services (IAM, Secrets, monitoring)
- Row 2 (y=200): Main application flow (API Gateway, Lambda, etc.)
- Row 3 (y=340): Data layer (databases, storage)
- Row 4 (y=480): Additional services (logging, analytics)

OUTPUT FORMAT:
{
  "services": [
    {
      "id": "unique_id",
      "name": "AWS Service Name",
      "type": "aws",
      "icon": "ServiceIcon",
      "description": "Brief description",
      "x": [MUST BE: 50, 200, 350, 500, 650, or 800],
      "y": [MUST BE: 60, 200, 340, 480, or 620]
    }
  ],
  "connections": [
    {
      "from": "service_id",
      "to": "service_id",
      "label": "connection_label",
      "dashed": false
    }
  ]
}

VALIDATION CHECKLIST:
- [ ] All y-coordinates are from: 60, 200, 340, 480, 620
- [ ] All x-coordinates are from: 50, 200, 350, 500, 650, 800
- [ ] No two services have same (x, y) position
- [ ] Services in same row have 150px+ horizontal spacing
- [ ] Services in same column have 140px+ vertical spacing
```

### Architecture Patterns

#### Pattern 1: Simple API Architecture
```json
{
  "services": [
    {"id": "client", "name": "Client", "x": 50, "y": 200},
    {"id": "apigw", "name": "Amazon API Gateway", "x": 200, "y": 200},
    {"id": "lambda", "name": "AWS Lambda", "x": 350, "y": 200},
    {"id": "dynamodb", "name": "Amazon DynamoDB", "x": 500, "y": 60},
    {"id": "s3", "name": "Amazon S3", "x": 500, "y": 340}
  ]
}
```

#### Pattern 2: Microservices Architecture
```json
{
  "services": [
    {"id": "apigw", "name": "Amazon API Gateway", "x": 50, "y": 200},
    {"id": "auth", "name": "AWS Lambda", "x": 200, "y": 60},
    {"id": "users", "name": "AWS Lambda", "x": 200, "y": 200},
    {"id": "orders", "name": "AWS Lambda", "x": 200, "y": 340},
    {"id": "authdb", "name": "Amazon DynamoDB", "x": 350, "y": 60},
    {"id": "userdb", "name": "Amazon DynamoDB", "x": 350, "y": 200},
    {"id": "orderdb", "name": "Amazon DynamoDB", "x": 350, "y": 340}
  ]
}
```

#### Pattern 3: Event-Driven Architecture
```json
{
  "services": [
    {"id": "source", "name": "Event Source", "x": 50, "y": 200},
    {"id": "eventbridge", "name": "Amazon EventBridge", "x": 200, "y": 200},
    {"id": "lambda1", "name": "AWS Lambda", "x": 350, "y": 60},
    {"id": "sqs", "name": "Amazon SQS", "x": 350, "y": 340},
    {"id": "lambda2", "name": "AWS Lambda", "x": 500, "y": 340},
    {"id": "dynamodb", "name": "Amazon DynamoDB", "x": 650, "y": 60},
    {"id": "s3", "name": "Amazon S3", "x": 650, "y": 340}
  ]
}
```

### Validation Rules for AI Agents

Before returning any diagram, verify:

1. **Position Validation:**
   ```python
   valid_x = [50, 200, 350, 500, 650, 800]
   valid_y = [60, 200, 340, 480, 620, 760]
   
   for service in services:
       assert service['x'] in valid_x, f"Invalid x: {service['x']}"
       assert service['y'] in valid_y, f"Invalid y: {service['y']}"
   ```

2. **Spacing Validation:**
   ```python
   for i, s1 in enumerate(services):
       for s2 in services[i+1:]:
           dx = abs(s1['x'] - s2['x'])
           dy = abs(s1['y'] - s2['y'])
           
           # Check vertical spacing
           if dx < 90:  # Same column
               assert dy >= 140, f"Vertical overlap: {s1['id']} and {s2['id']}"
           
           # Check horizontal spacing
           if dy < 110:  # Same row
               assert dx >= 150, f"Horizontal overlap: {s1['id']} and {s2['id']}"
   ```

3. **Uniqueness Validation:**
   ```python
   positions = [(s['x'], s['y']) for s in services]
   assert len(positions) == len(set(positions)), "Duplicate positions found"
   ```

### Error Prevention

**Common Mistakes to Avoid:**

❌ **WRONG:**
```json
{
  "services": [
    {"id": "s1", "x": 100, "y": 150},  // Not standard coordinates
    {"id": "s2", "x": 100, "y": 200}   // Only 50px gap - WILL OVERLAP!
  ]
}
```

✅ **CORRECT:**
```json
{
  "services": [
    {"id": "s1", "x": 50, "y": 60},    // Standard coordinates
    {"id": "s2", "x": 50, "y": 200}    // 140px gap - Perfect!
  ]
}
```

### Agent Response Template

```json
{
  "architecture": {
    "name": "Architecture Name",
    "description": "Brief description",
    "services": [
      {
        "id": "service1",
        "name": "AWS Service Name",
        "type": "aws",
        "icon": "ServiceIcon",
        "description": "Service description",
        "x": 50,
        "y": 200
      }
    ],
    "connections": [
      {
        "from": "service1",
        "to": "service2",
        "label": "connection type",
        "dashed": false
      }
    ],
    "validation": {
      "spacing_check": "PASSED",
      "position_check": "PASSED",
      "overlap_check": "PASSED"
    }
  }
}
```

### Integration with Backend

The backend will automatically validate and can auto-fix spacing issues:

```python
# Backend validation endpoint
@app.post("/api/diagrams/validate")
def validate_diagram(diagram: DiagramRequest):
    validator = DiagramValidator()
    is_valid, errors = validator.validate_diagram(diagram.services)
    
    if not is_valid:
        # Auto-fix spacing issues
        fixed_services = validator.auto_fix_spacing(diagram.services)
        return {
            "valid": False,
            "errors": errors,
            "fixed_services": fixed_services,
            "message": "Spacing issues detected and auto-fixed"
        }
    
    return {
        "valid": True,
        "message": "Diagram spacing is correct"
    }
```

### Summary for AI Agents

**When generating diagrams, you MUST:**

1. ✅ Use ONLY standard coordinates (x: 50, 200, 350, 500, 650, 800 | y: 60, 200, 340, 480, 620)
2. ✅ Ensure 140px minimum vertical spacing
3. ✅ Ensure 150px minimum horizontal spacing
4. ✅ Validate positions before returning
5. ✅ Include validation status in response

**Zero tolerance for:**

1. ❌ Random coordinates
2. ❌ Overlapping icons
3. ❌ Spacing violations
4. ❌ Unvalidated diagrams

**Result:**
- Professional, collision-free diagrams
- Consistent visual quality
- Production-ready output
- Happy users!

---

**This prompt template is MANDATORY for all diagram generation tasks.**
