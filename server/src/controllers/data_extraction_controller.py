import time
from src.prompts.data_classifier_prompt import data_classifier_prompt
from src.services.groq_llm_service import groq_client


async def reddit_data_extraction(content_list, interval=5):
    results = []

    for idx, item in enumerate(content_list, start=1):
        content = item["content"]
        url = item["url"]


        prompt = data_classifier_prompt(content)
        llm_output = groq_client(
            prompt=prompt,
            temperature=0,
            model="openai/gpt-oss-120b",
            max_tokens=65535
            
        )

        output = {
            "summary": llm_output,
            "url": url
        }

        results.append(output)

        print(llm_output)

        time.sleep(interval)

    return results
