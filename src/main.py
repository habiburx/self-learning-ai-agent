from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from .tools import save_to_txt, search_tool, wiki_tool

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

class Report(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
)

# response = groq.invoke("Hello, how are you?\n")
# print(response.content)

parser = PydanticOutputParser(pydantic_object=Report)

#prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a search agent that will help generate a report.
            Answer the user query and use necessary tools.
            Wrap the output in this format and provide no other text \n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions())

agent_system_template = prompt.messages[0].prompt.template
agent_system_template = chr(10).join(
    agent_system_template.split("{format_instructions}")[0].splitlines()[:-1]
)
agent_prompt = ChatPromptTemplate.from_messages(
    [("system", agent_system_template), *prompt.messages[1:]]
)

tools = [search_tool, wiki_tool]
agent = create_tool_calling_agent(
    llm = llm,
    prompt = agent_prompt,
    tools =tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
)
query = input("How can I help you?\nWrite what you want: ")

raw_response = agent_executor.invoke({"query": query})
# print({raw_respone})

format_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{format_instructions}"),
        ("human", "{query}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

try:
    structured_response = (format_prompt | llm | parser).invoke(
        {"query": raw_response["output"]}
    )
    structured_response = structured_response.model_copy(
        update={
            "tools_used": list(
                dict.fromkeys(
                    action.tool
                    for action, _ in raw_response["intermediate_steps"]
                )
            )
        }
    )
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)
else:
    save_result = save_to_txt(structured_response.model_dump_json(indent=2))
    print(save_result)