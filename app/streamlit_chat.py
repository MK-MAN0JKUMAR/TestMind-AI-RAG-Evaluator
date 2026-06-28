import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(ROOT_DIR)
)

import streamlit as st

from src.document_loader import (
    load_documents,
    load_uploaded_documents
)

from src.vector_store import (
    update_vector_store,
    create_temp_vector_store
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
 
if "runtime_vector_store" not in st.session_state:

    st.session_state.runtime_vector_store = None
 
    
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

    st.write("### Runtime Upload")

    uploaded_files = st.file_uploader(
        "Upload PDF / TXT",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    use_uploaded_documents = st.toggle(
        "Use uploaded documents",
        value=False
    )

    runtime_vector_store = None
        
    uploaded_names = tuple(
        file.name
        for file in uploaded_files
    ) if uploaded_files else ()

    if "uploaded_names" not in st.session_state:

        st.session_state.uploaded_names = ()
        
    if "loaded_count" not in st.session_state:

        st.session_state.loaded_count = 0

    if "failed_files" not in st.session_state:

        st.session_state.failed_files = []    

    if uploaded_files:

        if uploaded_names != st.session_state.uploaded_names:
            
            with st.spinner("Building temporary vector store..."):
                
                uploaded_documents, loaded_count, failed_files = load_uploaded_documents(
                    uploaded_files
                )
                
                st.session_state.loaded_count = loaded_count
                st.session_state.failed_files = failed_files

                st.session_state.runtime_vector_store = create_temp_vector_store(
                    uploaded_documents
                )
            

            st.session_state.uploaded_names = uploaded_names
        
        if st.session_state.failed_files:
            
            st.warning(
                f"Loaded: {st.session_state.loaded_count} | Failed: {len(st.session_state.failed_files)}"
            )

            st.caption(
                "Skipped: " + ", ".join(st.session_state.failed_files)
            )

        else:

            st.success(
                f"Loaded {st.session_state.loaded_count} uploaded file(s)"
            ) 

    st.divider()

    st.write("### Statistics")
    
    uploaded_count = len(uploaded_files) if uploaded_files else 0

    st.write(
        f"Base Documents : {len(documents)}"
    )

    st.write(
        f"Uploaded Files : {uploaded_count}"
    )

    st.write(
        "Active Source : Runtime Upload"
        if use_uploaded_documents and st.session_state.runtime_vector_store
        else "Active Source : Documents Folder"
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

        active_vector_store = (
            st.session_state.runtime_vector_store
            if use_uploaded_documents and st.session_state.runtime_vector_store
            else vector_store
        )

        result = ask_question(
            question,
            active_vector_store
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
                        f"📄 File : {doc['file_name']}"
                    )

                    st.write(
                        f"📑 Type : {doc['file_type']}"
                    )

                    st.write(
                        f"📄 Page : {doc['page']}"
                    )

                    st.write(
                        f"🧩 Chunk : {doc['chunk_index']}/{doc['total_chunks']}"
                    )

                    st.write(
                        f"📂 Source : {doc['source']}"
                    )

                    st.divider()

                    st.code(
                        doc["content"]
                    )

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                