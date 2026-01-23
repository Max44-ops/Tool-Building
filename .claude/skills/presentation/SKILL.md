---
name: presentation
description: Create PowerPoint-ready slide outlines for strategy presentations
argument-hint: [topic] [--slides:N] [--audience:executive|technical] [--german]
allowed-tools: WebSearch, WebFetch, Read
---

# Presentation Outline Skill

Create structured, PowerPoint-ready outlines for AI strategy presentations.

## Input Processing

From $ARGUMENTS extract:
- **Topic**: Main subject of the presentation
- **Slide count**: Target number of slides (default: 10-12)
- **Audience**: Executive or technical focus
- **Language**: German if specified

## Presentation Structure

### Standard Strategy Presentation Flow

1. **Title Slide**
2. **Executive Summary / Key Messages** (1 slide)
3. **Context / Why Now** (1-2 slides)
4. **Current State / Situation Analysis** (2-3 slides)
5. **Options / Opportunities** (2-3 slides)
6. **Recommendation** (1-2 slides)
7. **Roadmap / Next Steps** (1-2 slides)
8. **Appendix** (as needed)

## Output Format

For each slide, provide:

```markdown
---

## Slide [N]: [Title - Max 8 Words]

**Key Message:** [Single sentence takeaway]

**Visual Suggestion:** [Chart type, diagram, or image concept]

### Content
- Bullet point 1 (max 12 words)
  - Sub-bullet if needed
- Bullet point 2 (max 12 words)
- Bullet point 3 (max 12 words)

**Speaker Notes:**
[2-3 sentences of additional context for the presenter]

**Data Needed:** [If any data visualization is suggested, note what data is required]

---
```

## Audience Adaptations

### For Executive Audience
- Focus on business impact and ROI
- Minimize technical details
- Emphasize strategic implications
- Include competitor/market context
- Clear decision points

### For Technical Audience
- Include architecture considerations
- Address integration requirements
- Cover security and compliance
- Technical feasibility assessment
- Implementation considerations

## Visual Recommendations

Suggest appropriate visuals:
- **Comparisons**: Side-by-side tables, bar charts
- **Processes**: Flow diagrams, timelines
- **Maturity**: Radar charts, maturity curves
- **Priorities**: 2x2 matrices (Impact vs. Effort)
- **Roadmaps**: Gantt-style timelines, swim lanes
- **Market data**: Pie charts, trend lines

## Quality Standards

Each slide should:
- Have ONE clear message
- Be readable in 3 seconds (titles and key points)
- Support the overall narrative arc
- Connect logically to adjacent slides

## Example Output

```markdown
# Presentation Outline: AI Strategy for [Organization]

**Target Audience:** Executive Board
**Estimated Length:** 12 slides (20 minutes)
**Key Objective:** Secure approval for AI pilot program

---

## Slide 1: Title

**AI-Powered Transformation: A Strategic Roadmap**

Subtitle: Recommendations for [Organization]
Date: [Month Year]
Presented by: Sopra Steria Next

---

## Slide 2: Executive Summary

**Key Message:** Three strategic AI initiatives can deliver €X value within 18 months

**Visual Suggestion:** Three-column layout with icons

### Content
- Initiative 1: [Name] - [Expected outcome]
- Initiative 2: [Name] - [Expected outcome]
- Initiative 3: [Name] - [Expected outcome]

**Speaker Notes:**
This slide provides the board with immediate clarity on our recommendation...

---
[Continue for all slides...]
```
