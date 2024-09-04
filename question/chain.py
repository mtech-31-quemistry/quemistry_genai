import os
from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import VertexAI, ChatVertexAI

outputSchema ={
    "title": "multiple choice question",
    "description": "question to test Cambridge A Level Chemistry topics",
    "type": "object",
    "properties": {
        "stem": {
            "type": "string",
            "description":"stem of question",
        },
        "options": {
            "type": "array",
            "description":"options",
            "items":{
                "type": "object",
                "properties":{
                    "text": {
                        "type": "string",
                        "description":"an option",
                    },
                    "explanation": {
                        "type": "string",
                        "description":"explanation for option",
                    },
                    "isAnswer": {
                        "type": "boolean",
                        "description":"is answer",
                    }
                }
            }
        }
    }
}
outputSchemaStr = '{{"stem": "string","options": [{{"text": "string", "explanation": "string","isAnswer": "boolean"}}]}}'

prompt_template = PromptTemplate.from_template(
    "Design {number} multiple choice question for Cambridge A level Chemistry testing application in {topic}, {skill}. There are 4 options and can only have 1 answer. Provide answer and explanation for each options.")
prompt_template_outputSchema = PromptTemplate.from_template(
    "Design {number} multiple choice question for Cambridge A level Chemistry testing application in {topic}, {skill}. There are 4 options and can only have 1 answer. Provide answer and explanation for each options. Output in the json format "+outputSchemaStr)


def gen_byTopic_gemini() -> Runnable:
    """Return a chain"""
    #model="gemini-1.5-flash",
    # 2. Create model
    model = ChatVertexAI(model="gemini-pro",
                     project=os.environ['GOOGLE_PROJECT_ID'],
                     api_key=os.environ['GOOGLE_API_KEY']
            )
    structured_llm = model.with_structured_output(outputSchema)
    # 3. Create parser
    #parser = StrOutputParser()
    parser = JsonOutputParser()

    # 4. Create chain
    result = prompt_template_outputSchema | model | parser
    return result

def gen_byTopic_openai() -> Runnable:
    """Return a chain"""
    # 2. Create model
    model = ChatOpenAI()
    structured_llm = model.with_structured_output(outputSchema)
    # 3. Create parser
    parser = JsonOutputParser()

    # 4. Create chain
    result = prompt_template_outputSchema | model | parser
    return result