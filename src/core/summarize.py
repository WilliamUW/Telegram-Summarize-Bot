import json
import os
import ollama

from helpers.nano_to_seconds import nano_to_seconds
from config.ollama import MODEL, SYSTEM_PROMPT
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def summarize(messages):
    messages_json = json.dumps(messages, indent=4, ensure_ascii=False)

    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': messages_json}

        ],
        temperature=0,
        stream=True  # this time, we set stream=True
    )

    response_content = ""

    for chunk in response:
        if (chunk):
            #print(chunk)
            currentChunk = chunk.choices[0].delta.content
            print(currentChunk)
            #print("****************")
            if (chunk.choices[0].delta.content == None):
                yield response_content
            else:
                response_content += currentChunk


    # stream = ollama.generate(
    #     model=MODEL,
    #     prompt=messages_json,
    #     system=SYSTEM_PROMPT,
    #     stream=True
    # )

    # try:
    #     response_content = ""

    #     for chunk in stream:
    #         response_chunk = chunk['response']
    #         is_done = chunk['done']
    #         response_content += response_chunk

    #         metadata = "\n\n---\n\n"

    #         if is_done:
    #             model = chunk['model']
    #             total_duration_sec = nano_to_seconds(chunk['total_duration'])
    #             load_duration_sec = nano_to_seconds(chunk['load_duration'])
    #             prompt_eval_duration_sec = nano_to_seconds(chunk['prompt_eval_duration'])
    #             eval_duration_sec = nano_to_seconds(chunk['eval_duration'])

    #             metadata += f"Model: {model}\n"
    #             metadata += f"Total duration: {total_duration_sec:.2f} seconds\n"
    #             metadata += f"Model load duration: {load_duration_sec:.2f} seconds\n"
    #             metadata += f"Prompt evaluation duration: {prompt_eval_duration_sec:.2f} seconds\n"
    #             metadata += f"Response evaluation duration: {eval_duration_sec:.2f} seconds"
    #         else:
    #             metadata += "Generating summary... Please wait."

    #         yield response_content + metadata
    # except Exception as e:
    #     yield f"An error occurred while generating the summary: {str(e)}"

