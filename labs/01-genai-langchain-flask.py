# Hands-on with GenAI: Choosing the Right Model

"""
step 1: create project directory

mkdir genai_flask_app
cd genai_flask_app
"""

"""
step 2: virtual env setup

python3.11 -m venv venv
source venv/bin/activate
"""

"""
step 3: install libraries

pip install Flask langchain-ibm langchain
"""

"""
step 4: config.py

this config file centralizes model settings, making it easier to manage.
"""

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Model parameters
PARAMETERS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 256,
}

# watsonx credentials
CREDENTIALS = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "project_id": "skills-network"
}

# Model ID: in this lab we used 3 models to compare their outputs.
# here, i put only llama model since code will become longer otherwise
MODEL_ID = "meta-llama/llama-3-2-11b-vision-instruct"

"""
step 5: model.py

this file handles AI model integration
"""
from langchain_ibm import ChatWatsonx
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import PARAMETERS, MODEL_ID
from pydantic import BaseModel, Field

# define JSON output structure
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")

# JSON output parser
# this ensures that the output returned by the AI is automatically validated and parsed into the AIResponse format.
json_parser = JsonOutputParser(pydantic_object=AIResponse)

# function to initialize a model. this promotes code reuse
def initialize_model(model_id):
    return ChatWatsonx(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        params=PARAMETERS
    )

# initialize model
llm = initialize_model(MODEL_ID)

# prompt template
template = PromptTemplate(
    template='''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
''',
    input_variables=["system_prompt", "user_prompt"]
)

# this function allows us to chain a prompt template and an AI model together.
# we use the pipe (|) to directly take the output of the template and use that as the input of the model.
# we add the json_parser to our chain, to respond in well-structured JSON as defined by the AIResponse class
def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke({'system_prompt':system_prompt, 'user_prompt':user_prompt, 'format_prompt':json_parser.get_format_instructions()})

"""
step 6: app.py

this file uses the AI capabilities
"""
from flask import render_template
from model import model, template, get_ai_response
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    message = data.get('message')
    model = data.get('model')
    
    if not message or not model:
        return jsonify({"error": "Missing message or model selection"}), 400
    
    system_prompt = "You are an AI assistant helping with customer inquiries. Provide a helpful and concise response."
    
    start_time = time.time()
    
    try:
        if model == 'llama':
            result = get_ai_response(model, template, system_prompt, message)
        else:
            return jsonify({"error": "Invalid model selection"}), 400
        
        result['duration'] = time.time() - start_time
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
# then we add index.html, styling, and JS to Flask (out-of-scope)