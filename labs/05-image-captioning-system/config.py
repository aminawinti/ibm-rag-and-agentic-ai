WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
PROJECT_ID = "skills-network"  # course sandbox project, replace with your own outside the course environment
VISION_MODEL_ID = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"

# low temperature + low top_p: short factual answers, little randomness
TEMPERATURE = 0.2
TOP_P = 0.5

# prepended to every query, keeps answers to one sentence
SYSTEM_PROMPT = "You are a helpful assistant. Answer the following user query in 1 sentence: "

# four sample images from the course, numbered 1-4 in the order below
IMAGE_URLS = [
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/5uo16pKhdB1f2Vz7H8Utkg/image-1.png",  # city street
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/fsuegY1q_OxKIxNhf6zeYg/image-2.png",  # woman running
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/KCh_pM9BVWq_ZdzIBIA9Fw/image-3.png",  # flooded farm
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/VaaYLw52RaykwrE3jpFv7g/image-4.png",  # nutrition label
]

CAPTION_QUERY = "Describe the photo"

# (image number, question): same model and prompt as captioning, only the query changes
QUESTIONS = [
    (2, "How many cars are in this image?"),                       # counting objects
    (2, "What is the color of the woman's jacket?"),               # visual attributes
    (3, "How severe is the damage in this image?"),                # damage assessment (insurance-style)
    (4, "How much cholesterol is in this product? In grams and in %"),  # reading text from a label
]
