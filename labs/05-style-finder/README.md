# Style Finder: Multimodal Fashion Retrieval and Search

A fashion analysis app that identifies the garments in an outfit photo and returns matching items with prices and purchase links. This project uses PyTorch, scikit-learn, IBM watsonx.ai and Gradio.

## Project Overview

This is a multimodal RAG pipeline. An uploaded photo is turned into a feature vector, compared against a dataset of outfit embeddings, and the items of the closest outfit are given to Llama 4 Maverick as context together with the photo. The model describes what it sees, and the retrieved items (name, price, link) make the answer specific.

The dataset is curated from taylorswiftstyle.com. Each row is one fashion item with its name, price, purchase link, the outfit image it appears in, and a precomputed image embedding.

## Features

- Encode an uploaded photo as base64 (for the LLM) and as a ResNet50 feature vector (for search)
- Find the closest outfit in the dataset with cosine similarity
- Treat a match as exact above a similarity of 0.8, otherwise list the items as similar
- Generate a catalog-style analysis of the photo, with the retrieved items as context
- Always show the item list, even if the model refuses or the request fails
- Gradio web interface with optional example images

## Project Structure

```
05-style-finder-using-multimodal-retrieval-and-search/
├── requirements.txt           # Dependencies
├── config.py                  # Central settings
├── app.py                     # Pipeline and Gradio interface
├── models/
│   ├── image_processor.py     # ResNet50 embeddings, base64 encoding, similarity search
│   └── llm_service.py         # Llama 4 Maverick on watsonx.ai, catalog-analysis prompts
└── utils/
    └── helpers.py             # Dataset loading, item lookup, response cleanup
```

## Getting Started

### Installation & Running

```bash
pip install -r requirements.txt

python app.py
```

Open http://localhost:7860 and upload an outfit photo. The first run downloads the dataset to `data/swift-style-embeddings.pkl`. It is a pickle file. Sample photos named `test-1.png` to `test-3.png` in `examples/` show up as clickable examples, and are skipped if missing.

The project uses the course sandbox credentials (`skills-network`), which only work inside the course environment. To run it elsewhere, create your own watsonx.ai API key and project, then update `config.py`.

### RAG Workflow

1. The photo is encoded: a base64 JPEG for the LLM and a ResNet50 vector for the search
2. Cosine similarity against every embedding in the dataset gives the closest outfit
3. All items of that outfit are looked up by their image URL
4. The photo, the items and a catalog-analysis prompt (exact or similar match, depending on the threshold) go to Llama 4 Maverick
5. The response is cleaned up for display (escaped dollar signs, headings, bullets)

## What I Have Learnt

- **Image embeddings:** a pretrained CNN turns an image into a vector, and the dataset and the query must go through the exact same model and preprocessing to be comparable
- **Multimodal RAG:** the LLM gets both the image and the retrieved structured data, so its answer is grounded in real items
- **Prompting and fallbacks:** the prompt is framed as a retail catalog task, and the item list is added back if the model refuses or skips it
- **User interface:** wrapping the pipeline in a Gradio app

## Technical Skills

- **PyTorch / torchvision:** ResNet50 feature extraction and image preprocessing
- **scikit-learn:** cosine similarity
- **watsonx.ai integration:** Llama 4 Maverick image + text chat through `ibm-watsonx-ai`
- **pandas:** loading and filtering a pickled dataset with embeddings
- **Gradio:** building an interactive web UI

## Next Steps

- Find alternatives at different price points with a shopping search API
- Compare ResNet50 with an image-text embedding model such as CLIP
