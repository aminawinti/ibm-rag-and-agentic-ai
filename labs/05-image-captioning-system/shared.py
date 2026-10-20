import base64

import requests
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters

from config import (
    IMAGE_URLS, PROJECT_ID, SYSTEM_PROMPT, TEMPERATURE, TOP_P, VISION_MODEL_ID, WATSONX_URL,
)


def build_model():
    """ Llama 4 Maverick on watsonx.ai, configured for short, mostly deterministic answers. """
    return ModelInference(
        model_id=VISION_MODEL_ID,
        credentials=Credentials(url=WATSONX_URL),
        project_id=PROJECT_ID,
        params=TextChatParameters(temperature=TEMPERATURE, top_p=TOP_P),
    )


def encode_images(urls=IMAGE_URLS):
    """ Download each image and return it as a base64 string (None when the download fails). """
    # the chat request is JSON, which is text-only, so the raw bytes have to become a string
    encoded = []
    for url in urls:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            encoded.append(base64.b64encode(response.content).decode("utf-8"))
        else:
            print(f"Warning: failed to fetch {url} (status {response.status_code})")
            encoded.append(None)
    return encoded


def ask(model, encoded_image, query, system_prompt=SYSTEM_PROMPT):
    """ Send one image and one text query, return the model's answer as a string. """
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": system_prompt + query},
                # the lab labels every image as jpeg even though these are pngs, and it works
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + encoded_image}},
            ],
        }
    ]
    response = model.chat(messages=messages)
    return response["choices"][0]["message"]["content"]
