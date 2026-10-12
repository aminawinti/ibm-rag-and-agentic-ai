from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_ibm import WatsonxEmbeddings, WatsonxLLM

from config import EMBED_MODEL_ID, LLM_MODEL_ID, MAX_NEW_TOKENS, PROJECT_ID, WATSONX_URL


def build_llm():
    return WatsonxLLM(
        model_id=LLM_MODEL_ID,
        url=WATSONX_URL,
        project_id=PROJECT_ID,
        params={
            GenParams.DECODING_METHOD: DecodingMethods.GREEDY,  # deterministic, same video gives the same summary
            GenParams.MAX_NEW_TOKENS: MAX_NEW_TOKENS,
        },
    )

def build_embeddings():
    return WatsonxEmbeddings(model_id=EMBED_MODEL_ID, url=WATSONX_URL, project_id=PROJECT_ID)
