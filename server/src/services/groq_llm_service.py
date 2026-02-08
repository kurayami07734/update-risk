import re
import json
import time

from groq import Groq

from src.config import CONFIG


client = Groq(api_key=CONFIG.GROQ_LLM_API_KEY, timeout=40.0)


async def groq_client(
    prompt,
    temperature,
    model,
    max_tokens,
    call_id: str | None = None,
):
    try:

        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_completion_tokens=max_tokens,
            top_p=1,
            stream=False,
        )

        result = completion.choices[0].message.content

        json_pattern = r"(\{.*\})"
        match = re.search(json_pattern, result, re.DOTALL)

        if match:
            json_str = match.group(0)
            try:
                extracted_content = json.loads(json_str)
                return extracted_content
            except json.JSONDecodeError:
                return {}

    except Exception as e:
        return {}

    return {}
