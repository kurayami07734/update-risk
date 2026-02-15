async def data_classifier_prompt(content: str) -> str:
    return f"""
You analyze Reddit posts written by humans.

The text may include:
- Casual language, opinions, jokes, links
- Partial technical details
- Comments mixed with post content

Your task:
- Infer information ONLY if it is clearly stated or strongly implied
- If unsure or ambiguous, leave the field as an empty string ""
- Do NOT guess
- Do NOT fabricate package names or versions
- Do NOT add explanations
- Output VALID JSON ONLY

Fields to extract:
- package_name (software, tool, library, OS component)
- version_affected (specific version(s) mentioned)
- risk_description (bug, issue, vulnerability, breakage, malfunction)
- suggested_solution (workaround, fix, downgrade, config change, update)
- resolved_at (version or condition where issue is resolved, if mentioned)

REDDIT POST:
{content}

Return JSON exactly in this format:
{{
  "package_name": "",
  "version_affected": "",
  "risk_description": "",
  "suggested_solution": "",
  "resolved_at": ""
}}
"""
