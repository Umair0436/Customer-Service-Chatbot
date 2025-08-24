from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

load_dotenv()

# Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Load + Split Docs
loader = TextLoader("data.txt", encoding="utf-8")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# Embeddings + VectorStore
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Conversational Retrieval Chain (with memory)
conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=False
)

# ✅ Ask bot function
def ask_bot(query: str) -> str:
    try:
        response = conversational_chain.invoke({"question": query})
        return response["answer"]
    except Exception as e:
        return f"Error: {str(e)}"
