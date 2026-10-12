# watsonx.ai (same sandbox credentials as lab 01)
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
PROJECT_ID = "skills-network"
LLM_MODEL_ID = "ibm/granite-4-h-small"
EMBED_MODEL_ID = "ibm/granite-embedding-278m-multilingual"
MAX_NEW_TOKENS = 900

# transcript chunking and retrieval
CHUNK_SIZE = 200
CHUNK_OVERLAP = 20
TOP_K = 7

# matches youtube.com/watch?v=<id> and youtu.be/<id>
YOUTUBE_URL_PATTERN = r"(?:youtube\.com/watch\?(?:.*&)?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"

# gradio
SERVER_NAME = "0.0.0.0"
SERVER_PORT = 7860
