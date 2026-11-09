from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from ddgs.exceptions import DDGSException
from requests.exceptions import JSONDecodeError
from datetime import datetime
from pathlib import Path

def save_to_txt(data: str, filename: str = "output/response.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Response ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    output_path = Path(filename)
    if not output_path.is_absolute():
        output_path = Path(__file__).resolve().parent / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {output_path}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured response data to a text file.",
)

search = DuckDuckGoSearchRun()

def run_search(query: str) -> str:
    try:
        return search.run(query)
    except DDGSException as error:
        return (
            f"Search is unavailable because of a DNS/network error: {error}. "
            "Do not claim search results were returned; use other available "
            "sources or explain this limitation."
        )

search_tool = Tool(
    name="search",
    func=run_search,
    description="Search the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wikipedia_search = WikipediaQueryRun(api_wrapper=api_wrapper)

def run_wikipedia(query: str) -> str:
    try:
        return wikipedia_search.run(query)
    except JSONDecodeError as error:
        return (
            f"Wikipedia is unavailable because its server returned an invalid "
            f"response: {error}. Do not claim Wikipedia results were returned."
        )

wiki_tool = Tool(
    name="wikipedia",
    func=run_wikipedia,
    description="Search Wikipedia for information",
)
