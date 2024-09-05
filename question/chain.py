from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import SafetySetting
from langchain_google_genai import GoogleGenerativeAI

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

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

def gen_by_topic_gemini() -> Runnable:
    """Return a chain"""
    #model="gemini-1.5-flash",
    model = GoogleGenerativeAI(model="gemini-1.5-pro-001")
    #structured_llm = model.with_structured_output(outputSchema)
    parser = JsonOutputParser()

    result = prompt_template_outputSchema | model | parser
    return result

def gen_by_topic_openai() -> Runnable:
    """Return a chain"""
    model = ChatOpenAI(model="gpt-4o")
    #structured_llm = model.with_structured_output(outputSchema)
    parser = JsonOutputParser()

    result = prompt_template_outputSchema | model | parser
    return result