# watsonx.ai (same sandbox credentials as lab 01)
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
PROJECT_ID = "skills-network"  # course sandbox project, replace with your own outside the course environment
LLM_MODEL_ID = "ibm/granite-4-h-small"
LLM_TEMPERATURE = 0.9

# local embedding model, runs on cpu
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# ten documents. deliberately short and overlapping,
# so every retrieval result can be read and judged by eye
SAMPLE_DOCUMENTS = [
    "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data.",
    "Deep learning uses neural networks with multiple layers to model and understand complex patterns in data.",
    "Natural language processing enables computers to understand, interpret, and generate human language.",
    "Computer vision allows machines to interpret and understand visual information from the world.",
    "Reinforcement learning is a type of machine learning where agents learn to make decisions through rewards and penalties.",
    "Supervised learning uses labeled training data to learn a mapping from inputs to outputs.",
    "Unsupervised learning finds hidden patterns in data without labeled examples.",
    "Transfer learning leverages knowledge from pre-trained models to improve performance on new tasks.",
    "Generative AI can create new content including text, images, code, and more.",
    "Large language models are trained on vast amounts of text data to understand and generate human-like text.",
]
