import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("Google API key not found. Please add it to your Hugging Face Secrets.")

# ✅ Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

# ✅ Load + Split Docs
loader = TextLoader("data.txt", encoding="utf-8")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# ✅ Embeddings + VectorStore
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ✅ Conversational Retrieval Chain (with memory)
conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=False
)

# ✅ Ask bot function
def ask_bot(query: str) -> str:
    if not google_api_key:
        return "Error: API key is missing. Please add it to the Space secrets."
        
    try:
        response = conversational_chain.invoke({"question": query})
        return response["answer"]
    except Exception as e:
        return f"Error: {str(e)}"
