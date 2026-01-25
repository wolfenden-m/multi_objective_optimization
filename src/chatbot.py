import bs4
from langchain.agents import AgentState, create_agent
from langchain_community.document_loaders import WebBaseLoader
from langchain.messages import MessageLikeRepresentation
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
import ollama
import os
from langchain.chat_models import init_chat_model
from langchain_ollama import OllamaEmbeddings

# model
with open('groq_api.txt', 'r') as file: GROQ_API_KEY = file.read()

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
model = init_chat_model("groq:qwen/qwen3-32b")

# embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# vector store
vector_store = InMemoryVectorStore(embeddings)


# load data

# text
from langchain_community.document_loaders import TextLoader

reference_loader = TextLoader(
    "mcdm_moo_reference_for_rag.md",
    encoding="utf-8"
)

reference_docs = reference_loader.load()



from langchain_community.document_loaders import NotebookLoader
file_paths = ['00_preprocessing.ipynb', '01_introduction.ipynb', '02_moo_algorithms.ipynb', '03_modm_methods.ipynb', '04_rag_llm_model.ipynb']
script_docs = []
for path in file_paths:
    if path.endswith('.ipynb'):
        notebook_loader = NotebookLoader(path, remove_newline=True)
    script_docs.extend(notebook_loader.load())



# website
web_loader = WebBaseLoader("https://www.1000minds.com/decision-making/what-is-mcdm-mcda")
website_docs = web_loader.load()


# splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n## ",     # section headers
        "\n### ",
        "\n\n",
        "\n",
        " "
    ]
)

docs = text_splitter.split_documents(
    reference_docs + script_docs + website_docs
)


# metadata
for doc in docs:
    if "Pareto" in doc.page_content:
        doc.metadata["concept"] = "pareto"

    if "NSGA-II" in doc.page_content:
        doc.metadata["algorithm"] = "NSGA-II"

    if "SPEA-2" in doc.page_content:
        doc.metadata["algorithm"] = "SPEA-2"

    if "SMS-EMOA" in doc.page_content:
        doc.metadata["algorithm"] = "SMS-EMOA"

    if "MOEA/D" in doc.page_content:
        doc.metadata["algorithm"] = "MOEA-D"

    if "CMOPSO" in doc.page_content:
        doc.metadata["algorithm"] = "CMOPSO"

    if "MOPSO-CD" in doc.page_content:
        doc.metadata["algorithm"] = "MOPSO-CD"

    if "what should I do" in doc.page_content.lower():
        doc.metadata["question_type"] = "decision-guidance"

    if "suitcase" in doc.page_content.lower():
        doc.metadata["example"] = "suitcase"


# retriever 
retriever = vector_store.as_retriever()

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 6,
        "fetch_k": 20
    }
)


def classify_query(query: str) -> str:
    q = query.lower()

    if any(w in q for w in ["why", "difference", "compare"]):
        return "why"

    if any(w in q for w in ["what should i do", "recommend", "best approach"]):
        return "decision"

    return "explain"


# prompts
WHY_PROMPT = """You are analyzing the behavior of multi-objective algorithms.

When asked why one algorithm performs differently from another:
1. Identify the algorithms being compared
2. Explain each algorithm’s design bias
3. Connect that bias to observed objective differences
4. Emphasize that differences reflect tradeoffs, not errors
5. Avoid judging performance without stated preferences

Use the suitcase example when possible.
"""

EXPLAIN_PROMPT = """You are an assistant explaining multi-objective optimization (MOO) and
multi-criteria decision making (MCDM) concepts.

Your goals:
- Explain concepts clearly and intuitively
- Use the suitcase packing example when helpful
- Avoid unnecessary mathematical formalism unless requested
- Emphasize tradeoffs and Pareto optimality
- Clarify distinctions between optimization and decision making

When applicable:
- Define key terms
- Provide small illustrative examples
- State practical implications

Do NOT:
- Claim a single method is universally best
- Overfit explanations to one algorithm
"""

DECISION_PROMPT = """You are helping a user choose an appropriate multi-objective
optimization or decision-making approach.

Follow this structure:
1. Restate the user’s problem in decision-theoretic terms
2. Identify whether the task is optimization or decision making
3. Identify preference information (explicit or implicit)
4. Recommend one or more suitable methods
5. Explain why each method fits
6. Offer a simple next step the user can take

Be practical and preference-aware.
Do not prescribe a method without justification.
"""

from langchain_core.prompts import chat
from langchain_core.prompts import ChatPromptTemplate

PROMPTS = {
    "explain": ChatPromptTemplate.from_template(EXPLAIN_PROMPT),
    "why": ChatPromptTemplate.from_template(WHY_PROMPT),
    "decision": ChatPromptTemplate.from_template(DECISION_PROMPT),
}


# decision rubric
SYSTEM_CONTEXT = """
You are reasoning using a structured multi-objective
decision-making rubric:

1. Classify problem as MOO or MCDM
2. Identify preferences
3. Determine output type
4. Match algorithm bias to goals
5. Recommend workflow
"""


# Construct a tool for retrieving context
from langchain.tools import tool
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

tools = [retrieve_context]

agent = create_agent(model, tools, system_prompt=SYSTEM_CONTEXT)

def ask_model(query):
    for step in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()