from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = ChatOpenAI(model="gpt-5-turbo", temperature=0.7)
embeddings = OpenAIEmbeddings()
qa_chain = None

def load_materials_to_vector_store(text):
    global qa_chain
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever)

def get_answer_from_material(question: str):
    if not qa_chain:
        return "Please upload materials first."
    response = qa_chain({"question": question, "chat_history": []})
    return response["answer"]
