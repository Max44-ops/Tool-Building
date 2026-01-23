---
name: analyze
description: Analyze data and extract strategic insights for consulting deliverables
argument-hint: [data-source or topic] [--format:table|bullets|narrative] [--visual]
allowed-tools: Read, WebSearch, WebFetch, Glob, Grep
---

# Data Analysis Skill for Strategy Consulting

Analyze data and extract actionable insights for AI strategy deliverables.

## Analysis Framework

### 1. Data Understanding
From $ARGUMENTS, identify:
- Data source (file, topic for research, or inline data)
- Analysis objective
- Output format preference
- Visualization needs

### 2. Analysis Types

**Quantitative Analysis**
- Trend identification
- Comparison metrics
- Growth rates and projections
- Statistical summaries

**Qualitative Analysis**
- Theme extraction
- Pattern recognition
- Sentiment analysis
- Gap identification

**Strategic Analysis**
- SWOT components
- Competitive positioning
- Market opportunity sizing
- Risk assessment

## Output Structure

```markdown
# Analysis: [Topic/Data Source]

## Methodology
[Brief description of analysis approach]

## Key Insights

### Insight 1: [Title]
**Observation:** [What the data shows]
**Implication:** [What it means strategically]
**Recommendation:** [What to do about it]

### Insight 2: [Title]
[Same structure]

## Data Summary

| Metric | Value | Trend | Benchmark |
|--------|-------|-------|-----------|
| [Metric 1] | [Value] | [Up/Down/Stable] | [Industry avg] |

## Visualization Recommendations

**Recommended Chart 1:** [Chart type]
- Purpose: [What it would show]
- Data needed: [Specific data points]
- Key message: [What viewer should understand]

## Limitations
[Data quality issues, gaps, assumptions made]

## Next Steps
1. [Additional analysis needed]
2. [Data to collect]
```

## Specific Analysis Templates

### Vendor Comparison Analysis
```markdown
| Criteria | Vendor A | Vendor B | Vendor C | Weight |
|----------|----------|----------|----------|--------|
| Capability 1 | Score | Score | Score | X% |
| Capability 2 | Score | Score | Score | X% |
| Pricing | Score | Score | Score | X% |
| **Weighted Total** | **X** | **X** | **X** | 100% |
```

### Market Sizing Analysis
```markdown
## Total Addressable Market (TAM)
- Market definition: [Scope]
- TAM estimate: €[X]B
- Source: [Citation]

## Serviceable Addressable Market (SAM)
- Geographic/segment focus: [Scope]
- SAM estimate: €[X]M

## Serviceable Obtainable Market (SOM)
- Realistic target: €[X]M
- Assumptions: [List]
```

### Maturity Assessment
```markdown
| Dimension | Current State (1-5) | Target State | Gap | Priority |
|-----------|---------------------|--------------|-----|----------|
| Strategy | X | X | X | High/Med/Low |
| Data | X | X | X | High/Med/Low |
| Technology | X | X | X | High/Med/Low |
| People | X | X | X | High/Med/Low |
| Process | X | X | X | High/Med/Low |
```

### Use Case Prioritization
```markdown
| Use Case | Business Impact (1-5) | Feasibility (1-5) | Score | Priority |
|----------|----------------------|-------------------|-------|----------|
| UC1 | X | X | X | High |
| UC2 | X | X | X | Medium |
```

## Visualization Guidelines

When `--visual` flag is present, provide detailed specs:

```markdown
## Chart Specification: [Chart Name]

**Type:** [Bar/Line/Scatter/etc.]
**Title:** [Exact title text]
**X-Axis:** [Label and data]
**Y-Axis:** [Label and scale]
**Data Series:**
- Series 1: [Name, color suggestion, data points]
- Series 2: [Name, color suggestion, data points]
**Key Callouts:** [Annotations to highlight]
**Source Note:** [Data source for footer]
```
