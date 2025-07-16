import streamlit as st 
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from langchain.agents import initialize_agent,AgentType
from langchain_groq import ChatGroq
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv
load_dotenv()

api_wrapper_wiki=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)
api_wrapper_Arxiv=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=250)
arxvi=ArxivQueryRun(api_wrapper=api_wrapper_Arxiv)
groq_api_key=os.getenv("GROQ_API_KEY")

Search=DuckDuckGoSearchRun(name="search")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {
            "role":"assistant",
            "content":"Hi, I am a chatbot who can search over the internet"
        }
    ]
    

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    
if prompt:=st.chat_input(placeholder="Share your thought"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    
    gorq_model=ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key,streaming=True)
    tools=[Search,arxvi,wiki]
    
    search_agent=initialize_agent(tools,gorq_model,agent=AgentType.z  ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)
    
    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)