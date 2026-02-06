import re
import json
import time
from groq import Groq
from src.config.config import GROQ_API_KEY
from typing import List, Dict, Any

TIMEOUT_CONFIG = 40.0
client = Groq(api_key=GROQ_API_KEY,timeout=TIMEOUT_CONFIG)

async def groq_client(prompt, temperature, model, max_tokens,call_id: str | None = None):
    try:
        start_time = time.time()

        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_completion_tokens=max_tokens,
            top_p=1,
            stream=False
        )


        result = completion.choices[0].message.content
        print(result)


        json_pattern = r'(\{.*\})'
        match = re.search(json_pattern, result, re.DOTALL)

        if match:
            json_str = match.group(0)
            try:
                extracted_content = json.loads(json_str)
                return extracted_content
            except json.JSONDecodeError:
                return {}

    except Exception as e:

        print(f"Groq error: {e}")
        return {}

    return {}
