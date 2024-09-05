
from fastapi import FastAPI
from langserve import add_routes

from question.chain import gen_by_topic_gemini, gen_by_topic_openai
app = FastAPI(title="Quemistry GenAI")

add_routes(app, gen_by_topic_gemini(), path="/geminimcqbytopic")
add_routes(app, gen_by_topic_openai(), path="/openaimcqbytopic")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)