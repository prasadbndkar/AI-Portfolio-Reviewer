#Import Necessary Libraries

from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from dotenv import load_dotenv
import os,glob
import streamlit as st

load_dotenv()

@st.cache_resource
def buildChain():

   #-------------------Build RAG Chain-----------------------------#
    @st.cache_resource
    def Feed(Chat):        #Initiate Feed

        Files_list=glob.glob(f'{os.getenv("FILE_PATH")}/*.pdf')   #List of Source Files Path

        question=Chat["question"]                    #User's Query

        chat_history=Chat.get("chat_history",[])     #Chat History

        #-------------------------------Extract Candidates Metadata------------------------------#

        def extract_candidate(question,chat_history):

            history_text= "\n".join([f"Human :{msg.content}" if msg.type=="human" else f"AI :{msg.content}" for msg in chat_history])        #Summarizing Previous Conversation

            print("History Text:",history_text)

            extraction_prompt=f"""You are a strict text-processing unit. 
                                  TASK: Identify which name from the List below is being discussed in the Conversation.
                                  LIST OF VALID NAMES: {Files_list}
                                  CONVERSATION:{history_text}
                                  CURRENT QUESTION: {question}

                                  RULES:
                                    - Output ONLY the name from the list.
                                    - DO NOT write Python code.
                                    - DO NOT explain your answer.
                                    - If no name from the list is found, output 'None'.
                                    RESULT:"""
            
            return ChatOllama(model="llama3.2:3b").invoke(extraction_prompt)
        
        candidate_name=extract_candidate(question,chat_history)

        #-----------------------Load the KnowledgeBase of Specific Candidate------------------------------#

        docs=DirectoryLoader(path=f'{os.getenv("FILE_PATH")}',glob=f"./{candidate_name.content}.pdf",loader_cls=PyPDFLoader).load()

        #-----------------------Convert Documents into Chunks-----------------------------#

        chunks=CharacterTextSplitter(chunk_size=1000,chunk_overlap=200).split_documents(docs)

        #-----------------------Store Chunks as Embeddings in VectorStore---------------#

        vector=Chroma.from_documents(documents=chunks,embedding=OllamaEmbeddings(model="llama3.2:3b"))

        #----------------------Revectorize using Flashrerank and Contextual Compression Retriever--------------#

        Revector=ContextualCompressionRetriever(base_compressor=FlashrankRerank(top_n=3),base_retriever=vector.as_retriever())

        return {"context":"\n\n".join([doc.page_content for doc in Revector.invoke(Chat["question"])]),
                "question":Chat["question"],
                "chat_history":Chat.get("chat_history",[])}

    #------------------------Initiate Prompt---------------------------#

    Prompt=ChatPromptTemplate.from_messages([("system","You are fully authorized AI Portfolio Reviewer, you can access and reviews any portfolio"\
                                                        "which is in PDF, Word, Image format.If asked list down certifications"\
                                                        "Answer only on the {context}.Do not assume anything else."\
                                                        "Answer only in following format"  \
                                                        "Answer :"),
                                                        MessagesPlaceholder(variable_name="chat_history"),
                                                        ("human","{question}")])
    #-----------------------Initiate LLM Model-------------------------#

    Model=ChatOllama(model="llama3.2:3b")

    #----------------------Parse Output--------------------------------#

    Parser=StrOutputParser()
    #----------------------BASE RAGCHAIN PIPELINE----------------------#

    RAGChain=Feed | Prompt | Model | Parser

    return RAGChain

#--------------------------Set session configurations------------------#

config={"configurable":{"session_id":"user_123"}}

#-------------------------Inject Historical COnversation------------------------#

if "Store" not in st.session_state:
    st.session_state["Store"]={}

def get_history(session_id : str):
    if session_id not in st.session_state.Store:
        st.session_state.Store[session_id]=ChatMessageHistory()
    return st.session_state.Store[session_id]

RAGChain_with_memory=RunnableWithMessageHistory(buildChain(),get_history,input_messages_key="question",history_messages_key="chat_history")

#---------------------INITIATE CONVERSATION--------------------------------#

st.title("AI Portfolio Reviewer")

user_input=st.text_input("Ask a question :")

#---------------------FETCH RESULT-----------------------------------------#
if user_input:
    Chat=RAGChain_with_memory.invoke({"question":user_input},config=config)
    st.write(Chat)