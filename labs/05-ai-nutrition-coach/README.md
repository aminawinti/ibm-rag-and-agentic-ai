# AI Nutrition Coach

A Flask web app that estimates the calories and nutrients of a meal from a photo. This project uses Flask, IBM watsonx.ai and Meta's Llama 4 Maverick.

## Project Overview

The user uploads a photo of a meal and, optionally, edits the question. The image and a nutritionist prompt are sent to Llama 4 Maverick, which identifies the food items and returns a structured assessment. The app converts that answer to HTML and shows it under a preview of the uploaded image.

The estimates come from the model's own knowledge. There is no external nutrition database behind them, so they are approximate.

## Features

- Upload a meal photo, with a preview in the browser before submitting
- Ask your own question about the image (default: "How many calories are in this food?")
- Structured answer: identified items, portion size and calories per item, total calories, nutrient breakdown (protein, carbohydrates, fats, vitamins, minerals), a one-paragraph health evaluation and a fixed disclaimer
- Model output converted to HTML (headings, bullet lists, line breaks)
- Loading message while the model answers, and flash messages for errors such as a missing file

## Project Structure

```
05-ai-nutrition-coach/
├── requirements.txt           # Dependencies
├── app.py                     # Flask routes, image encoding, prompt, model call, response formatting
├── static/
│   └── style.css              # Page styling
└── templates/
    └── index.html             # Upload form, image preview and results
```

## Getting Started

### Installation & Running

```bash
pip install -r requirements.txt

python app.py
```

Open http://127.0.0.1:5000, choose a meal photo and click **Tell me the total calories**.

The project uses the course sandbox credentials (`skills-network`), which only work inside the course environment. To run it elsewhere, create your own watsonx.ai API key and project, then update the `Credentials` and `project_id` in `app.py`.

### Workflow

1. The form posts the image and the question to the Flask route
2. The image is read and encoded to a base64 string
3. The nutritionist prompt, the question and the image go into a single chat message, sent with `model.chat()` to Llama 4 Maverick on watsonx.ai
4. `format_response()` converts the answer (bold headings, `*` bullets, newlines) to HTML with regular expressions
5. The template renders the result, and the browser shows the image preview and a loading message in the meantime

## What I Have Learnt

- **Multimodal prompting:** an image and a text prompt in one chat message to Llama 4 Maverick
- **Prompt design for structured output:** a numbered template with examples makes the answer predictable enough to format
- **Post-processing LLM output:** turning Markdown-style text into HTML with regular expressions
- **Front-end touches:** an image preview with `FileReader` and a loading message shown on submit

## Technical Skills

- **Flask:** routing, templates, static files, form handling
- **watsonx.ai integration:** `ModelInference.chat()` and `TextChatParameters` from `ibm-watsonx-ai`
- **Llama 4 Maverick:** food recognition and nutritional estimation from images
- **HTML / CSS / JavaScript:** the upload form, styling and client-side preview

## Next Steps

- Let the user enter a health goal (weight loss, muscle gain) and tailor the advice to it
