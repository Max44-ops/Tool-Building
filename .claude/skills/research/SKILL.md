---
name: research
description: Deep research on AI topics with source synthesis for strategy consulting
argument-hint: [topic] [--sources] [--german]
allowed-tools: WebSearch, WebFetch, Read, Grep, Glob
---

# Research Skill for AI Strategy Consulting

You are conducting research for an AI strategy consultant. Deliver comprehensive, source-backed analysis.

## Research Process

### 1. Scope Definition
Based on $ARGUMENTS, identify:
- Core topic and subtopics
- Key questions to answer
- Relevant geographic/industry context

### 2. Source Categories
Search across these source types:
- **Analyst Reports**: Gartner, Forrester, IDC, McKinsey
- **Vendor Documentation**: Official product pages, pricing, capabilities
- **Regulatory**: EU AI Act, national guidelines, compliance requirements
- **Academic**: Recent papers on the topic (arXiv, IEEE)
- **News**: Recent developments and announcements
- **German Sources**: Bitkom, BMWi if relevant

### 3. Synthesis Approach
- Cross-reference claims across sources
- Note areas of consensus and disagreement
- Identify information gaps
- Flag outdated information

## Output Structure

```markdown
# Research: [Topic]

## Executive Summary
[3-5 bullet points with key findings]

## Key Findings

### [Finding 1 Title]
[Detailed explanation with source citations]

### [Finding 2 Title]
[Detailed explanation with source citations]

## Market/Vendor Landscape
[If applicable: key players, positioning, trends]

## Regulatory Considerations
[If applicable: relevant regulations, compliance requirements]

## Information Gaps
[What we couldn't find or needs deeper investigation]

## Sources
- [Source 1](URL) - Brief description
- [Source 2](URL) - Brief description

## Recommended Next Steps
1. [Action item]
2. [Action item]
```

## Special Instructions

### For Vendor Analysis
Include: Capabilities, pricing model, target market, strengths/weaknesses, recent announcements

### For Regulatory Research
Include: Current status, timeline, key requirements, penalties, industry impact

### For Market Trends
Include: Growth projections, adoption rates, regional differences, key drivers

### Language
- If `--german` flag: Output in German
- Otherwise: Match the language of the topic or default to English
