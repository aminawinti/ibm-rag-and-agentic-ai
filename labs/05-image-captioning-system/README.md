# Image Captioning System with Llama 4

An image captioning and visual question answering tool built on Meta's Llama 4 Maverick. This project uses IBM watsonx.ai and a handful of sample images, so every answer can be checked against the picture.

## Project Overview

Llama 4 Maverick is natively multimodal: it takes text and images in the same request. That means one model and one function cover both tasks. This project will implement image captioning and visual question answering.

## Features

- Download images from URLs and encode them as base64 (AI-readable format)
- Caption every image with a one-sentence description
- Answer targeted questions about an image: counting objects, reading attributes, assessing damage, extracting text from a label
- Skip images that fail to download instead of crashing the run

## Project Structure

```
05-image-captioning-system/
├── requirements.txt           # Dependencies
├── config.py                  # Model, prompt, image URLs and questions
├── shared.py                  # Model setup, image encoding, ask()
└── app.py                     # Caption all four images & specific questions about these images
```

## Getting Started

### Installation & Running

```bash
pip install -r requirements.txt

python app.py
```

The project uses the course sandbox credentials (`skills-network`), which only work inside the course environment. To run it elsewhere, create your own watsonx.ai API key and project, then update `config.py`.

### Workflow

1. Each image is downloaded and encoded to a base64 string
2. The query and the image go into a single chat message (a `text` part and an `image_url` part)
3. `model.chat()` sends it to Llama 4 Maverick on watsonx.ai
4. The text of the first choice is the answer

## What I Have Learnt

- **Image encoding:** the request body is JSON, which is text-only, so images are sent as base64 strings. This is the AI-readable format.
- **Multimodal messages:** one user message holds both a text part and an image part, in the same chat format used for text-only models

## Technical Skills

- **Llama 4 Maverick:** multimodal prompting for captioning and visual Q&A
- **Image handling:** downloading with `requests` and base64 encoding

## Next Steps

- Add a Gradio interface to upload an image and ask questions about it
- Compare captions across different models available on watsonx.ai
