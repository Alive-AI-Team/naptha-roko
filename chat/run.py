# import requests
from chat.schemas import InputSchema
from chat.utils import get_logger
from chat.chroma.chroma_interface import ChromaInterface
import asyncio
from ollama import AsyncClient

logger = get_logger(__name__)

CHROMADB_COLLECTION_NAME = "roko-telegram"
OLLAMA_ENDPOINT = "http://localhost:5050/api/generate"


async def ollama_chat(model, messages):
    return await AsyncClient(host=OLLAMA_ENDPOINT).chat(model=model, messages=messages)


def run(job: InputSchema, cfg: dict = None, **kwargs):
    logger.info(f"Running job {job.model} {job.prompt}")
    logger.info(f"cfg: {cfg}")

    data = {
        "model": job.model,
        "prompt": job.prompt,
        "stream": False,
    }

    # Get content from vector db
    ci = ChromaInterface()
    results = ci.query(CHROMADB_COLLECTION_NAME, job.prompt, 10)
    # insert it into the prompt
    messages = []
    for doc in results["documents"][0]:
        messages.append({"role": "system", "content": doc})
    messages.append({"role": "user", "content": job.prompt})

    return asyncio.run(ollama_chat(job.model, messages))


if __name__ == "__main__":
    job = InputSchema(
        model="llama3",
        prompt="Where do I find information about the Uphold exchange?",
    )
    result = run(job)
    print(result)
