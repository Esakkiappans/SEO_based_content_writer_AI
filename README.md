# SEO Based Content Writer
  ┌─────────────────────────────────────────────────────────────┐
  │                       SEO-Based Content Writer                │
  └─────────────────────────────────────────────────────────────┘
                                 ▲
                                 │
                                 │ Enter URL
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────┐
  │                          Load Data                        │
  │           (Fetch and clean HTML content)                  │
  └───────────────────────────────────────────────────────────┘
                                 ▲
                                 │
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────┐
  │                          Process                         │
  │               (Create vector store from text)              │
  └───────────────────────────────────────────────────────────┘
                                 ▲
                                 │
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────┐
  │                          Ask Question                     │
  │               (Generate SEO-friendly content)              │
  └───────────────────────────────────────────────────────────┘
                                 ▲
                                 │
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────┐
  │                          Generate Content                  │
  │               (Use vector store to generate content)       │
  └───────────────────────────────────────────────────────────┘
                                 ▲
                                 │
                                 │
                                 ▼
  ┌───────────────────────────────────────────────────────────┐
  │                          Display Content                  │
  │               (Display SEO-friendly content to user)        │
  └───────────────────────────────────────────────────────────┘
## Overview

The "SEO Based Content Writer" project is an AI-powered tool that assists in generating SEO-friendly content based on a given URL and user questions. It utilizes natural language processing (NLP) techniques, conversation chains, and embeddings to create informative and engaging content.

 ws users to input a URL and ask questions related to the document fetched from the URL. The backend processing involves several stages:

1. **Data Fetch from URL**: The system fetches HTML content from the provided URL using the `requests` library. The HTML content is then cleaned and parsed to extract the main text content using BeautifulSoup.

2. **Text Pre-processing**: The main text content undergoes pre-processing, including chunking into smaller segments, to optimize for processing efficiency and to ensure accurate semantic analysis.

3. **Conversational Retrieval Chain**: The pre-processed text segments are embedded into vectors using Hugging Face Instruct Embeddings and stored in a vector store using FAISS. These embeddings are then used in a Conversational Retrieval Chain, which leverages a pre-trained language model (LLM) to respond to user questions in a conversational manner.

## Usage

1. Input a URL containing the content you want to analyze.
2. Ask questions related to the document fetched from the URL.
3. Click on the respective buttons to load data, process it, and generate content based on user questions.

## Installation

1. Clone the repository to your local machine:

git clone https://github.com/your_username/SEO-Based-Content-Writer.git


2. Install the required dependencies using pip:

pip install -r requirements.txt


3. Run the application using Streamlit:

streamlit run app.py


## Technologies Used

- Python
- Streamlit
- BeautifulSoup
- Hugging Face Instruct Embeddings
- FAISS
- LangChain (custom library)
- HTML/CSS

## Contributors

- [Esakkiappans](https://github.com/Esakkiappans)



