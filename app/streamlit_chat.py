import sys
import streamlit as st
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(ROOT_DIR)
)

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
    layout="centered"
)



# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown(
    """
<style>

.block-container{
    padding-top:0.5rem;
    padding-bottom:1rem;
}

[data-testid="stSidebar"]{
    border-right:1px solid #2d2d2d;
}

[data-testid="stMetric"]{
    background:#1f2937;
    border:1px solid #374151;
    border-radius:12px;
    padding:12px;
}

[data-testid="stExpander"]{
    border-radius:10px;
    border:1px solid #30363d;
}

.hero{
    padding:20px;
    border-radius:14px;
    background:#111827;
    border:1px solid #374151;
    margin-bottom:10px;
}

.tech-stack{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:14px;
    margin-top:18px;
}

.tech-card{
    background:#1f2937;
    border:1px solid #374151;
    border-radius:12px;
    padding:12px;
}

.tech-title{
    color:#9ca3af;
    font-size:12px;
    margin-bottom:6px;
}

.tech-value{
    color:white;
    font-weight:600;
    font-size:16px;
}

.hero h1{
    color:#4CAF50;
    font-size:clamp(32px,5vw,52px);

}

.hero p{
    color:#d1d5db;
    font-size:clamp(14px,2vw,18px);

}

.section-title{
    color:#60a5fa;
    font-weight:600;
    margin-top:12px;
    margin-bottom:8px;
}

[data-testid="stSidebarUserContent"]{
    margin-top:-2rem;
}

@media (max-width: 768px){

    .hero{
        padding:16px;
    }

    .tech-stack{
        grid-template-columns:1fr;
        gap:10px;
    }

    .tech-card{
        padding:14px;
    }

    .tech-value{
        font-size:20px;
    }

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
    
    st.markdown(
        """
        <hr style="
            margin:0px 0;
            border:0;
            border-top:3px solid #3b3b3b;
        ">
        """,
        unsafe_allow_html=True
    )

    st.write("### Runtime Upload")

    uploaded_files = st.file_uploader(
        "Upload PDF / TXT",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    use_uploaded_documents = st.toggle(
        "Use uploaded documents",
        key="use_uploaded_documents"
    )
        
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
        
    if "use_uploaded_documents" not in st.session_state:

        st.session_state.use_uploaded_documents = False 

    if uploaded_files:

        if uploaded_names != st.session_state.uploaded_names:
            
            with st.spinner("Building temporary vector store..."):
                
                uploaded_documents, loaded_count, failed_files = load_uploaded_documents(
                    uploaded_files
                )
                
                st.session_state.loaded_count = loaded_count
                st.session_state.failed_files = failed_files
                
                if uploaded_documents:

                    st.session_state.runtime_vector_store = create_temp_vector_store(
                        uploaded_documents
                    )

                else:

                    st.session_state.runtime_vector_store = None            

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

    st.markdown(
        """
        <hr style="
            margin:0px 0;
            border:0;
            border-top:2px solid #3b3b3b;
        ">
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### 📊 Statistics")

    uploaded_count = st.session_state.loaded_count

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Documents",
            len(documents)
        )

        st.metric(
            "Questions",
            len(st.session_state.chat_history)
        )

    with col2:

        st.metric(
            "Uploads",
            uploaded_count
        )
        
        st.metric(
            "Mode",
            "Runtime"
            if st.session_state.use_uploaded_documents
            and st.session_state.runtime_vector_store
            else "Local"
        )




# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.markdown(
    """
<div class="hero">

<h1>🤖 TestMind Chat</h1>

<p>Enterprise AI-Augmented RAG Chat</p>

<div class="tech-stack">

<div class="tech-card">
<div class="tech-title">🟢 LLM</div>
<div class="tech-value">llama3.1:8b</div>
</div>

<div class="tech-card">
<div class="tech-title">🔵 Embedding</div>
<div class="tech-value">all-MiniLM-L6-v2</div>
</div>

<div class="tech-card">
<div class="tech-title">🟣 Vector DB</div>
<div class="tech-value">FAISS</div>
</div>

<div class="tech-card">
<div class="tech-title">🟠 Retriever</div>
<div class="tech-value">Similarity Search</div>
</div>

</div>

</div>
""",
unsafe_allow_html=True
)

def run_example_question(question: str):

    active_vector_store = (
        st.session_state.runtime_vector_store
        if (
            st.session_state.use_uploaded_documents
            and st.session_state.runtime_vector_store
        )
        else vector_store
    )

    with st.spinner(f"🔎 Searching: {question}"):

        result = ask_question(
            question,
            active_vector_store
        )

        st.session_state.chat_history.insert(
            0,
            result
        )

    st.rerun()
 

if st.session_state.clear_input:

    st.session_state.question_input = ""
    st.session_state.clear_input = False    
   
    
    
    
# ---------------------------------------------------
# Search Area
# ---------------------------------------------------

with st.form("search_form"):
    
    question = st.text_input(
        "Question",
        key="question_input",
        placeholder="Ask a question...",
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button(
        "🔍 Search",
        use_container_width=True
    )

if submitted and question.strip():
      
    with st.spinner(
        "🔎 Searching documents and generating answer..."
    ):    

        active_vector_store = (
            st.session_state.runtime_vector_store
            if st.session_state.use_uploaded_documents and st.session_state.runtime_vector_store
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
        
if st.session_state.clear_input:

    st.session_state.question_input = ""
    st.session_state.clear_input = False    




# ---------------------------------------------------
# Quick Actions
# ---------------------------------------------------

show_runtime = (
    st.session_state.runtime_vector_store is not None
)

show_chat = (
    len(st.session_state.chat_history) > 0
)

if show_runtime or show_chat:

    if show_runtime and show_chat:

        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:

            if st.button(
                "🗑 Clear Runtime",
                use_container_width=True
            ):

                st.session_state.runtime_vector_store = None
                st.session_state.uploaded_names = ()
                st.session_state.loaded_count = 0
                st.session_state.failed_files = []

                st.rerun()

        with col2:

            if st.button(
                "🗑 Clear Chat",
                use_container_width=True
            ):

                st.session_state.chat_history = []

                st.rerun()

    elif show_runtime:

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            if st.button(
                "🗑 Clear Runtime",
                use_container_width=True
            ):

                st.session_state.runtime_vector_store = None
                st.session_state.uploaded_names = ()
                st.session_state.loaded_count = 0
                st.session_state.failed_files = []

                st.rerun()

    else:

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            if st.button(
                "🗑 Clear Chat",
                use_container_width=True
            ):

                st.session_state.chat_history = []

                st.rerun()




# ---------------------------------------------------
# No Conversation Yet & Example Questions
# ---------------------------------------------------

if not st.session_state.chat_history:

    st.info(
        "💬 No conversation yet. Upload documents or ask your first question."
    )

    st.markdown("### 💡 Example Questions")

    examples = [
        ("What is Playwright?", "example_playwright"),
        ("What is Python?", "example_python"),
        ("Tell me about health insurance?", "example_health"),
        ("Compare Selenium and Playwright", "example_selenium_playwright"),
    ]

    col1, col2 = st.columns(2)

    for index, (question, key) in enumerate(examples):

        column = col1 if index % 2 == 0 else col2

        with column:

            if st.button(
                question,
                key=key,
                use_container_width=True,
            ):
                run_example_question(question)
                
                
                
# ---------------------------------------------------
# Result & Chat History
# ---------------------------------------------------

if st.session_state.chat_history:

    for result in st.session_state.chat_history:
        
        st.markdown(
            """
        <hr style="
        margin-top:0px;
        margin-bottom:0px;
        border:0;
        border-top:1px solid #30363d;
        ">
        """,
            unsafe_allow_html=True
        )

        # ---------------------------------------
        # Answer
        # ---------------------------------------

        st.markdown(
            f"""
        <div style="
        background:#1f2937;
        padding:14px 18px;
        border-radius:12px;
        margin-top:8px;
        margin-bottom:10px;
        border:1px solid #374151;
        ">

        <div style="font-size:14px;color:#9ca3af;">
        👤 You
        </div>

        <div style="margin-top:4px;margin-left:24px; font-size:17px;">
        {result["question"]}
        </div>

        </div>
        """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
<div style="
background:#113322;
padding:16px 18px;
border-radius:12px;
border:1px solid #2f855a;
margin-bottom:8px;
">

<div style="
font-size:14px;
font-weight:600;
color:#9fe8b3;
margin-bottom:6px;
margin-left:8px;
">
🤖 TestMind
</div>

<div style="
font-size:16px;
line-height:1.7;
color:white;
margin-left:22px;
">
{result["answer"]}
</div>

</div>
""",
    unsafe_allow_html=True
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
                
                st.markdown(
                    f"""
                <div style="
                background:#1f2937;
                padding:10px;
                border-radius:8px;
                margin-bottom:8px;
                ">

                📄 {source}

                </div>
                """,
                    unsafe_allow_html=True
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
                                
                    col1, col2, col3 = st.columns(3)

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

                    left, right = st.columns(2)

                    with left:

                        st.caption(
                            f"📄 File : {doc['file_name']}"
                        )

                        st.caption(
                            f"📑 Type : {doc['file_type']}"
                        )

                    with right:

                        st.caption(
                            f"📄 Page : {doc['page']}"
                        )

                        st.caption(
                            f"🧩 Chunk : {doc['chunk_index']}/{doc['total_chunks']}"
                        )

                    st.caption(
                        f"🆔 {doc['chunk_id']}"
                    )

                    st.caption(
                        f"📂 {doc['source']}"
                    )

                    st.markdown(
                        """
                        <hr style="
                            margin:0px 0;
                            border:0;
                            border-top:1px solid #3b3b3b;
                        ">
                        """,
                        unsafe_allow_html=True
                    )
                    

                    st.markdown("**Retrieved Content**")

                    st.code(
                        doc["content"],
                        language="text"
                    )
                    
                    with col3:

                        st.metric(
                            "File",
                            doc["file_type"].upper()
                        )
                        
st.markdown(
    """
<hr style="
    margin:0px 0;
    border-top:1px solid #3b3b3b;
">
""",
    unsafe_allow_html=True
)


st.markdown(
    """
<div style="
text-align:center;
color:#9ca3af;
padding-bottom:18px;
">

TestMind AI-RAG Evaluator • Ollama • FAISS • LangChain • Streamlit

</div>
""",
    unsafe_allow_html=True
)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                