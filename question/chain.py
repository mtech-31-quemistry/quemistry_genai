import os
from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import VertexAI
from openai import api_key


def gen_byTopic_gemini() -> Runnable:
    """Return a chain"""
    # 1. Create prompt template
    #system_template = "Come up with {number} multiple choice question with answer and explanation for Cambridge GCSE level Chemistry, testing applications on following topics and out in json format with stem, options, answer and explanations :"
    template = "Design {number} multiple choice question for Cambridge A level Chemistry {topic}, {skill}. Provide answer and explanation for each options."
    prompt_template = PromptTemplate.from_template("Design {number} multiple choice question for Cambridge A level Chemistry {topic}, {skill}. Provide answer and explanation for each options.")

    # 2. Create model
    model = VertexAI(model="gemini-1.5-flash",
                     project=os.environ['GOOGLE_PROJECT_ID'],
                     api_key=os.environ['GOOGLE_API_KEY']
            )

    # 3. Create parser
    parser = StrOutputParser()

    # 4. Create chain
    return prompt_template | model | parser

def gen_byTopic_openai() -> Runnable:
    """Return a chain"""
    # 1. Create prompt template
    #system_template = "Come up with {number} multiple choice question with answer and explanation for Cambridge GCSE level Chemistry, testing applications on following topics and out in json format with stem, options, answer and explanations :"
    template = "Design {number} multiple choice question for Cambridge A level Chemistry {topic}, {skill}. Provide answer and explanation for each options."
    prompt_template = PromptTemplate.from_template("Design {number} multiple choice question for Cambridge A level Chemistry {topic}, {skill}. Provide answer and explanation for each options.")

    # 2. Create model
    model = ChatOpenAI()

    # 3. Create parser
    parser = StrOutputParser()

    # 4. Create chain
    return prompt_template | model | parser