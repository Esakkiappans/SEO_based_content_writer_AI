import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from bs4 import BeautifulSoup
import requests

from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_text_chunks(row_text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,   # Character
        chunk_overlap=200  # Character
    )
    chunks = text_splitter.split_text(row_text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.5, "max_length": 512})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    unwanted_sections = soup.find_all(['script', 'style', 'meta', 'link', 'footer'])
    for section in unwanted_sections:
        section.decompose()

    # Extract main content
    main_content = soup.get_text(separator='\n')

    return main_content.strip()


# def clean_text(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')

#     # Find the article tag
#     article_tag = soup.find('article')

#     if article_tag:
#         # Remove unwanted sections within the article
#         unwanted_sections = article_tag.find_all(['script', 'style', 'meta', 'link', 'footer'])
#         for section in unwanted_sections:
#             section.decompose()

#         # Extract main content inside the article tag
#         main_content = article_tag.get_text(separator='\n')
#         return main_content.strip()
#     else:
#         return "No article tag found in the HTML content."


def main():
    load_dotenv()
    st.set_page_config(page_title="SEO Based Content Writer", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.header("SEO Based Content Writer:books:")
    
    url_input = st.text_input("Enter the URL to fetch data:")
    user_question = st.text_input("Ask a question about the document:")
    
    if st.button("Load Data"):
        with st.spinner("Loading data..."):
            if url_input:
                try:
   
                    response = requests.get(url_input)
                    response.raise_for_status()

                    cleaned_text = clean_text(response.text)
                    print (cleaned_text)


                    # Save loaded data 
                    st.session_state.loaded_data = cleaned_text

                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching data from the URL: {e}")
            else:
                st.warning("Please enter a valid URL.")

    # Process the loaded data
    if st.button("Process"):
        if "loaded_data" in st.session_state:
            with st.spinner("Processing"):
                # get the text chunks
                text_chunks = get_text_chunks(st.session_state.loaded_data)
                # create vector store
                vector_store = get_vectorstore(text_chunks)
                print(vector_store)

                if vector_store:
                    st.session_state.vector_store = vector_store
                    st.success("Data processed successfully.")
                else:
                    st.warning("Error creating vector store. Please check your data.")

        else:
            st.warning("Please load data before processing.")

    # Create content after loading
    if st.button("Create Content"):
        vector_store = st.session_state.vector_store
        print("mmmmmm,",vector_store)
        if vector_store:
            st.session_state.conversation = get_conversation_chain(vector_store)
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']

            for i, message in enumerate(st.session_state.chat_history):
                if i % 2 == 0:
                    st.write(user_template.replace(
                        "{{MSG}}", message.content), unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace(
                        "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.warning("Please load data and process it before creating content.")

if __name__ == "__main__":
    main()
