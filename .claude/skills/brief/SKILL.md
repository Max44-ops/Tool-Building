---
name: brief
description: Create executive briefs and summaries for stakeholder communication
argument-hint: [topic or document] [--length:short|medium|long] [--audience:ceo|board|technical] [--german]
allowed-tools: Read, WebSearch, WebFetch
---

# Executive Brief Skill

Create concise, impactful briefs for executive stakeholders.

## Brief Types

Based on $ARGUMENTS, determine the brief type:

### 1. Topic Brief
Research and summarize a topic for executive consumption

### 2. Document Summary
Condense a longer document into executive summary

### 3. Decision Brief
Present options and recommendation for a decision

### 4. Status Update
Summarize project or initiative progress

## Length Guidelines

- **Short** (1 page): 250-400 words, 3-5 key points
- **Medium** (2 pages): 500-800 words, detailed analysis
- **Long** (3+ pages): Comprehensive with appendix

## Output Format

```markdown
# Executive Brief: [Topic]

**Date:** [Current date]
**Prepared for:** [Audience]
**Classification:** [If applicable]

---

## Bottom Line Up Front (BLUF)

[2-3 sentences capturing the essential message and any required action]

---

## Situation

[Brief context - what's happening and why it matters]

## Key Points

1. **[Point 1 Title]**
   [Supporting detail in 1-2 sentences]

2. **[Point 2 Title]**
   [Supporting detail in 1-2 sentences]

3. **[Point 3 Title]**
   [Supporting detail in 1-2 sentences]

## Implications

**For [Organization/Client]:**
- [Implication 1]
- [Implication 2]

## Recommendation

[Clear, actionable recommendation with rationale]

## Next Steps

| Action | Owner | Timeline |
|--------|-------|----------|
| [Action 1] | [Who] | [When] |
| [Action 2] | [Who] | [When] |

---

**Sources:** [Brief citation list]
```

## Audience Adaptations

### For CEO/C-Suite
- Lead with business impact
- Quantify in financial terms
- Focus on strategic implications
- Clear decision points
- One page maximum when possible

### For Board
- Governance perspective
- Risk and compliance focus
- Comparison to industry/peers
- Long-term strategic view

### For Technical Leadership
- Include technical feasibility
- Architecture implications
- Resource requirements
- Integration considerations

## Writing Standards

### Clarity
- One idea per sentence
- Active voice
- Specific numbers over vague qualifiers
- Define acronyms on first use

### Impact
- Start with the most important information
- Use "So what?" test for each point
- Quantify impact where possible

### Brevity
- Cut unnecessary words
- Use bullet points for lists
- Tables for comparisons
- No filler phrases

## Example: Short Brief

```markdown
# Executive Brief: EU AI Act Compliance Requirements

**Date:** January 2026
**Prepared for:** Chief Digital Officer

---

## Bottom Line Up Front

The EU AI Act enters full enforcement in August 2026. Our preliminary assessment identifies 3 high-risk AI systems requiring immediate compliance action and estimated investment of €500K-800K.

---

## Key Points

1. **Timeline is compressed**
   Full enforcement begins August 2026; high-risk AI registration required 6 months prior

2. **Three systems classified as high-risk**
   Customer credit scoring, HR recruitment tool, and fraud detection system require conformity assessments

3. **Compliance gap exists**
   Current documentation and monitoring practices insufficient for regulatory requirements

## Recommendation

Initiate compliance program in Q1 2026 with dedicated project team and external legal support.

## Next Steps

| Action | Owner | Timeline |
|--------|-------|----------|
| Complete AI system inventory | CTO | Feb 2026 |
| Engage legal counsel | Legal | Feb 2026 |
| Begin risk assessments | Compliance | Mar 2026 |

---

**Sources:** EU AI Act (Regulation 2024/1689), Gartner AI Regulation Guide 2025
```
