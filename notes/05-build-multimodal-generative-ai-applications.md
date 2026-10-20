# Course 5 - Build Multimodal Generative AI Applications

## Background note

Courses 2-4 were about text only: chunk it, embed it, retrieve it, feed it to an LLM. This course widens the pipeline to other data types: speech, images and video.

## What this course covered

- **Foundations of multimodal AI:** what it is, where it's used, and what makes it hard (alignment, imbalance between modalities, compute cost, bias)
- **Speech processing:** speech-to-text (STT) and text-to-speech (TTS), and how modern end-to-end models differ from the traditional pipeline
- **Vision and video with language:** text-to-image, image captioning, and text-to-video
- **Multimodal RAG (MM-RAG):** retrieval and generation across text, images and other data types
- **Multimodal chatbots and QA:** apps that answer questions about an image plus a text prompt

## Key concepts

**Multimodal AI.** Systems that process and combine several data types at once (text, speech, images, video). The main building blocks are text processing, computer vision, speech processing, TTS, and **multimodal fusion**, which is the step that merges the modalities into one representation.

**Image captioning with a multimodal LLM.** Three stages:

1. **Input processing:** receive the image and an optional text prompt
2. **Image validation and encoding:** check the image and convert it to a model-friendly format (Base64)
3. **Multimodal LLM processing:** the model fuses the visual and text information and writes the caption

Under the hood it relies on four components: visual encoders, text embeddings, fusion layers and language generation. The optional prompt is what lets you steer the caption instead of getting a generic description.

**Multimodal RAG (MM-RAG).** The same RAG idea from Courses 2-4, but the data and the query can be text, images, audio or video. It rests on three ideas: multimodal retrieval, **contrastive learning** to produce embeddings that put different modalities in a shared space, and a generative model that uses the retrieved multimodal context. The pipeline has four steps:

1. **Data indexing:** convert all data types to embeddings and store them in a vector database
2. **Data retrieval:** embed the user's query and fetch the closest multimodal items
3. **Augmentation:** combine the retrieved data with the original query
4. **Response generation:** produce an answer that blends all the modalities

**Multimodal chatbots and QA.** Systems that accept several input types, understand them together, and answer in context. A basic implementation is: set up the environment and imports, initialize the model, prepare the image, write the multimodal query function, then call it.

## What I actually built

Three modules, with labs along the way:

1. **Image Captioning System** with Meta's Llama 4 Maverick through IBM watsonx: encode the image, send it with a prompt, and extract the caption from the response.
2. **Style Finder**, an AI shopping assistant that uses multimodal retrieval to find and match fashion items from an image input.
3. **AI Nutrition Coach**, an image-based Flask web app that estimates calories and gives dietary recommendations from a food photo plus text.

See snippets from these apps at `labs/05-image-captioning-system/`, `labs/05-style-finder/` and `labs/05-ai-nutrition-system/`.

## Notes & things I'd do differently

- MM-RAG is Course 3-4's pipeline with a different embedding step: the vector database and retrieval logic stay the same, but the embeddings now have to put text and images in one shared space
- Flask shows up again here (it was my Course 1 tool), and it fits better than Gradio for the Nutrition Coach because I want a custom UI around image upload
- Data alignment and modality imbalance are the problems I want to watch for when I build the capstone on top of multiple data types
