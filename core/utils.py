import re

CASE_TEMPLATE = """# {title}

**Executive Summary**  
{summary}

## Problem / Need
{problem}

## Implementation Approach
{implementation}

## Benefits & Impact
{benefits}

## Key Learning Points
{learnings}

## Point of Contact
{poc}

## Suggested Visuals / Diagrams
{visuals}
"""

def build_case_study(title, summary, problem, implementation, benefits, learnings, poc, visuals):
    return CASE_TEMPLATE.format(**locals())

def parse_questions_list(text: str):
    items = re.findall(r"[-•]\s*(.+)", text)
    return [i.strip() for i in items[:10]] or [text.strip()[:120]]
