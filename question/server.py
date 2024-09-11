
from fastapi import FastAPI
from langserve import add_routes
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from question.chain import gen_by_topic_gemini, gen_by_topic_openai

_healthChecks = HealthCheckFactory()
app = FastAPI(title="Quemistry GenAI")

add_routes(app, gen_by_topic_gemini(), path="/genai/geminimcqbytopic")
add_routes(app, gen_by_topic_openai(), path="/genai/openaimcqbytopic")
app.add_api_route('/genai/health', healthCheckRoute(factory=_healthChecks))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)