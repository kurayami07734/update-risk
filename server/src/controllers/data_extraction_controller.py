

import asyncio
import json
from src.services.db_incident_service import save_incident
from src.prompts.data_classifier_prompt import data_classifier_prompt
from src.services.groq_llm_service import groq_client


async def reddit_data_extraction(content_list, interval=5):
    print(content_list)
    results = []

    for idx, item in enumerate(content_list, start=1):
        content = item["content"]
        print(content)
        url = item["url"]

        prompt = await data_classifier_prompt(content)
        # print("prompt reached")
        print(prompt)

        llm_output = await groq_client(
            prompt=prompt,
            temperature=0,
            model="openai/gpt-oss-120b",
            max_tokens=65535
        )
        print(llm_output)
        if isinstance(llm_output, dict):
            extracted = llm_output
        elif isinstance(llm_output, str):
            try:
                extracted = json.loads(llm_output)
                print(extracted)
            except json.JSONDecodeError:
                await asyncio.sleep(interval)
                continue
        else:
            await asyncio.sleep(interval)
            continue

        if not any(
            str(value).strip()
            for value in extracted.values()
            if value is not None
        ):
            await asyncio.sleep(interval)
            continue

        # results.append({
        #     "extracted_data": extracted,
        #     "url": url
        # })
        
        saved = await save_incident(extracted, url)
        
        if saved:
            results.append(saved)

        await asyncio.sleep(interval)

    return results
