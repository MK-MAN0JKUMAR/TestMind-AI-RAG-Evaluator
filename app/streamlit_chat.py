import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(ROOT_DIR)
)

import streamlit as st

from src.document_loader import (
    load_documents
)

from src.vector_store import (
    update_vector_store
)

from src.rag_pipeline import (
    ask_question
)



# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="TestMind Chat",
    page_icon="🤖",
    layout="wide"
)



# ---------------------------------------------------
# CSS
# ---------------------------------------------------

st.markdown(
    """
<style>

.block-container {
    padding-top: 1rem;
}

h1{
    color:#4CAF50;
}

div[data-testid="stMetric"]{
    background-color:#1e1e1e;
    border-radius:10px;
    padding:10px;
}

div[data-testid="stExpander"]{
    border-radius:10px;
    border:1px solid #333;
}

[data-testid="stSidebarUserContent"] {
    margin-top: -5rem;
}

</style>
""",
    unsafe_allow_html=True
)



# ---------------------------------------------------
# Session State
# ---------------------------------------------------    
    
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

if "clear_input" not in st.session_state:

    st.session_state.clear_input = False

if "question_input" not in st.session_state:

    st.session_state.question_input = ""    
 
 
    
# ---------------------------------------------------
# Load RAG
# ---------------------------------------------------

@st.cache_resource
def initialize_rag():

    documents = load_documents(
        "documents"
    )

    vector_store = update_vector_store(
        documents
    )

    return documents, vector_store

documents, vector_store = initialize_rag()



# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("⚙️ TestMind")

    st.write("### Configuration")

    st.success(
        "LLM : llama3.1:8b"
    )

    st.success(
        "Embeddings : all-MiniLM-L6-v2"
    )

    st.info(
        "Vector DB : FAISS"
    )

    st.info(
        "Documents : TXT + PDF"
    )

    st.divider()

    st.write("### Statistics")

    st.write(
        f"Documents Loaded : {len(documents)}"
   )

    st.write(
        f"Questions Asked : {len(st.session_state.chat_history)}"
    )

    if st.button(
        "🗑 Clear Chat History"
    ):

        st.session_state.chat_history = []

        st.rerun()



# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title(
    "🤖 TestMind Chat"
)

st.caption(
    "Fast RAG Chat"
)

if st.session_state.clear_input:

    st.session_state.question_input = ""

    st.session_state.clear_input = False



# ---------------------------------------------------
# Search Area
# ---------------------------------------------------

with st.form(
        "search_form",
):
    
    question = st.text_input(
        "Ask a question",
        key="question_input"
    )

    submitted = st.form_submit_button(
        "Search"
    )

if submitted and question.strip():

    with st.spinner(
            "Thinking..."
    ):

        result = ask_question(
            question,
            vector_store
        )

        st.session_state.chat_history.insert(
            0,
            result
        )
        
        st.session_state.clear_input = True
        
        st.rerun()



# ---------------------------------------------------
# Results
# ---------------------------------------------------

if st.session_state.chat_history:

    for result in st.session_state.chat_history:

        st.divider()
        
        st.markdown(
            f"### Q. {result['question']}"
        )


        # ---------------------------------------
        # Answer
        # ---------------------------------------

        st.success(
            result["answer"]
        )


        # ---------------------
        # Sources
        # ---------------------

        tab1, tab2 = st.tabs(
            [
                "📄 Sources",
                "🧩 Retrieved Chunks"
            ]
        )


        # ---------------------
        # Sources
        # ---------------------

        with tab1:

            for source in result["sources"]:

                st.write(
                   f"📄 {source}"
                )


        # ---------------------
        # Retrieved Chunks
        # ---------------------

        with tab2:
            
            st.subheader(
                "Retrieved Chunks"
            )

            for index, doc in enumerate(
                    result["retrieved_docs"],
                    start=1
            ):
                
                distance = doc["score"]

                similarity_percent = max(
                    0,
                    round(
                        (1 - distance / 2) * 100,
                        1
                    )
                )
                
                with st.expander(
                        f"Rank #{index}"
                ):
                                
                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Similarity",
                            f"{similarity_percent}%"
                        )

                    with col2:

                        st.metric(
                            "Chunk ID",
                            doc["chunk_id"]
                        )

                    st.write(
                        f"📄 Source : {doc['source']}"
                    )

                    st.divider()

                    st.code(
                        doc["content"]
                    )

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                