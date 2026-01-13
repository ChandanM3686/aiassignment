"""
Math Mentor - AI-Powered JEE Math Tutor
Main Streamlit Application

A multimodal AI application that solves JEE-style math problems with:
- Image, Audio, and Text input support
- RAG-enhanced problem solving
- Multi-agent architecture
- Human-in-the-Loop validation
- Self-learning memory
"""

import streamlit as st
import uuid
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import get_settings
from ui.styles import get_custom_css
from ui.components import (
    render_extraction_preview,
    render_agent_trace,
    render_context_panel,
    render_solution_display,
    render_confidence_bar,
    render_feedback_buttons,
    render_hitl_interface,
    render_memory_sidebar,
)
from ui.agent_trace import AgentTraceManager

# Page configuration
st.set_page_config(
    page_title="Math Mentor - AI JEE Tutor",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "text"
    if "current_problem_id" not in st.session_state:
        st.session_state.current_problem_id = None
    if "result" not in st.session_state:
        st.session_state.result = None
    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = ""
    if "extraction_confidence" not in st.session_state:
        st.session_state.extraction_confidence = 1.0
    if "hitl_pending" not in st.session_state:
        st.session_state.hitl_pending = False
    if "memory_initialized" not in st.session_state:
        st.session_state.memory_initialized = False
    if "rag_initialized" not in st.session_state:
        st.session_state.rag_initialized = False


def get_memory_store():
    """Get or create memory store."""
    if "memory_store" not in st.session_state:
        from memory.memory_store import MemoryStore
        st.session_state.memory_store = MemoryStore()
    return st.session_state.memory_store


def get_orchestrator():
    """Get or create agent orchestrator."""
    if "orchestrator" not in st.session_state:
        from agents.orchestrator import AgentOrchestrator
        st.session_state.orchestrator = AgentOrchestrator()
    return st.session_state.orchestrator


def initialize_rag():
    """Initialize RAG pipeline if not done."""
    if not st.session_state.rag_initialized:
        try:
            from rag.knowledge_base import is_knowledge_base_initialized
            
            # Check if already built (prevents API calls)
            if is_knowledge_base_initialized():
                st.session_state.rag_initialized = True
                return
            
            # Not built - continue without RAG (no warning shown)
            st.session_state.rag_initialized = True
            
        except Exception as e:
            st.session_state.rag_initialized = True  # Continue anyway


def process_image_input(uploaded_file):
    """Process uploaded image."""
    from input_handlers.image_handler import ImageHandler
    
    handler = ImageHandler()
    image_data = uploaded_file.read()
    
    with st.spinner("Extracting text from image..."):
        result = handler.process_image(image_data)
    
    return result.text, result.confidence, result.needs_review


def process_audio_input(uploaded_file):
    """Process uploaded audio."""
    from input_handlers.audio_handler import AudioHandler
    
    handler = AudioHandler()
    audio_data = uploaded_file.read()
    extension = uploaded_file.name.split('.')[-1]
    
    with st.spinner("Transcribing audio..."):
        result = handler.process_audio(audio_data, extension)
    
    return result.transcript, result.confidence, result.needs_review


def process_text_input(text):
    """Process text input."""
    from input_handlers.text_handler import TextHandler
    
    handler = TextHandler()
    result = handler.process_text(text)
    
    return result.text, 1.0, False


def solve_problem(problem_text, input_type, confidence):
    """Solve the math problem using the agent orchestrator."""
    orchestrator = get_orchestrator()
    
    with st.spinner("🧠 Solving problem..."):
        result = orchestrator.solve(
            raw_input=problem_text,
            input_type=input_type,
            input_confidence=confidence
        )
    
    return result


def save_to_memory(result, input_type, raw_input, feedback=None, comment=None):
    """Save result to memory."""
    from memory.memory_store import MemoryStore, ProblemMemory
    from rag.embeddings import GeminiEmbeddings
    
    memory_store = get_memory_store()
    
    # Generate embedding for similarity search
    embeddings = GeminiEmbeddings()
    embedding = embeddings.embed_text(result.parsed_problem.get("problem_text", ""))
    
    memory = ProblemMemory(
        id=st.session_state.current_problem_id,
        timestamp=datetime.now(),
        input_type=input_type,
        raw_input=raw_input,
        parsed_question=result.parsed_problem.get("problem_text", ""),
        topic=result.parsed_problem.get("topic", ""),
        subtopic=result.parsed_problem.get("subtopic", ""),
        retrieved_context=str(result.retrieved_sources),
        solution=str(result.solution),
        explanation=result.explanation_markdown,
        final_answer=result.final_answer,
        verifier_confidence=result.confidence,
        user_feedback=feedback or "",
        user_comment=comment or "",
        embedding=embedding
    )
    
    memory_store.save_problem(memory)


def render_input_section():
    """Render the input section."""
    st.markdown("## 📥 Enter Your Math Problem")
    
    # Mode selector
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⌨️ Text Input", 
                     use_container_width=True,
                     type="primary" if st.session_state.input_mode == "text" else "secondary"):
            st.session_state.input_mode = "text"
            st.rerun()
    
    with col2:
        if st.button("📷 Image Upload", 
                     use_container_width=True,
                     type="primary" if st.session_state.input_mode == "image" else "secondary"):
            st.session_state.input_mode = "image"
            st.rerun()
    
    with col3:
        if st.button("🎤 Audio Input", 
                     use_container_width=True,
                     type="primary" if st.session_state.input_mode == "audio" else "secondary"):
            st.session_state.input_mode = "audio"
            st.rerun()
    
    st.markdown("---")
    
    # Input based on mode
    problem_text = None
    input_confidence = 1.0
    needs_review = False
    
    if st.session_state.input_mode == "text":
        problem_text = st.text_area(
            "Type your math problem:",
            height=150,
            placeholder="e.g., Find the roots of x² - 5x + 6 = 0"
        )
        input_confidence = 1.0
        needs_review = False
        
    elif st.session_state.input_mode == "image":
        uploaded_file = st.file_uploader(
            "Upload an image of your math problem",
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, JPEG, PNG"
        )
        
        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            with col2:
                if st.button("🔍 Extract Text", use_container_width=True):
                    problem_text, input_confidence, needs_review = process_image_input(uploaded_file)
                    st.session_state.extracted_text = problem_text
                    st.session_state.extraction_confidence = input_confidence
                
                if st.session_state.extracted_text:
                    problem_text = render_extraction_preview(
                        st.session_state.extracted_text,
                        st.session_state.extraction_confidence,
                        editable=True
                    )
                    input_confidence = st.session_state.extraction_confidence
                    needs_review = input_confidence < 0.6
    
    elif st.session_state.input_mode == "audio":
        uploaded_file = st.file_uploader(
            "Upload an audio recording of your question",
            type=["wav", "mp3", "m4a", "ogg"],
            help="Supported formats: WAV, MP3, M4A, OGG"
        )
        
        if uploaded_file:
            st.audio(uploaded_file)
            
            if st.button("🎙️ Transcribe Audio", use_container_width=True):
                problem_text, input_confidence, needs_review = process_audio_input(uploaded_file)
                st.session_state.extracted_text = problem_text
                st.session_state.extraction_confidence = input_confidence
            
            if st.session_state.extracted_text:
                problem_text = render_extraction_preview(
                    st.session_state.extracted_text,
                    st.session_state.extraction_confidence,
                    editable=True
                )
                input_confidence = st.session_state.extraction_confidence
                needs_review = input_confidence < 0.7
    
    return problem_text, input_confidence, needs_review


def render_result_section(result):
    """Render the result section."""
    if result is None:
        return
    
    st.markdown("---")
    
    # Check for HITL
    if result.needs_hitl:
        st.session_state.hitl_pending = True
        hitl_response = render_hitl_interface(
            result.hitl_reason,
            result.parsed_problem.get("problem_text", ""),
            requires_edit=True
        )
        
        if hitl_response["action"] == "approve":
            st.session_state.hitl_pending = False
            # Re-solve with corrected text if edited
            if hitl_response["edited_text"] != result.parsed_problem.get("problem_text", ""):
                orchestrator = get_orchestrator()
                result = orchestrator.solve_with_correction(
                    hitl_response["edited_text"],
                    result.parsed_problem
                )
                st.session_state.result = result
                st.rerun()
        elif hitl_response["action"]:
            return  # Wait for user action
    
    # Agent trace
    with st.expander("🔄 Agent Execution Trace", expanded=False):
        traces = [
            {
                "agent": t.agent_name,
                "action": t.action,
                "summary": t.output_summary,
                "status": t.status,
                "duration": f"{t.duration_ms:.0f}ms"
            }
            for t in result.traces
        ] if hasattr(result, 'traces') else []
        
        if traces:
            render_agent_trace(traces)
        else:
            trace_summary = getattr(result, 'get_trace_summary', lambda: [])
            if callable(trace_summary):
                render_agent_trace(trace_summary())
    
    # Retrieved sources
    with st.expander("📚 Retrieved Knowledge Base Context", expanded=False):
        render_context_panel(result.retrieved_sources)
    
    # Solution
    render_solution_display(
        result.final_answer,
        result.explanation if isinstance(result.explanation, dict) else {},
        result.explanation_markdown
    )
    
    # Confidence
    st.markdown("### 📊 Solution Confidence")
    render_confidence_bar(result.confidence, "Overall Confidence")
    
    # Feedback
    feedback = render_feedback_buttons(st.session_state.current_problem_id)
    
    if feedback:
        comment = st.session_state.get("feedback_comment", "")
        save_to_memory(result, st.session_state.input_mode, 
                      st.session_state.extracted_text or "", feedback, comment)
        
        if feedback == "correct":
            st.success("✅ Thank you! This solution has been saved as correct.")
        else:
            st.info("📝 Thank you for the feedback. We'll use this to improve.")


def render_sidebar():
    """Render the sidebar."""
    st.sidebar.markdown("# 🧮 Math Mentor")
    st.sidebar.markdown("*AI-Powered JEE Math Tutor*")
    st.sidebar.markdown("---")
    
    # Topics covered
    st.sidebar.markdown("### 📚 Topics Covered")
    st.sidebar.markdown("""
    - Algebra (Quadratics, Polynomials)
    - Probability & Statistics
    - Calculus (Limits, Derivatives)
    - Linear Algebra (Matrices, Vectors)
    """)
    
    st.sidebar.markdown("---")
    
    # Memory stats
    try:
        memory_store = get_memory_store()
        stats = memory_store.get_stats()
        render_memory_sidebar(stats)
    except Exception:
        pass
    
    st.sidebar.markdown("---")
    
    # Settings
    st.sidebar.markdown("### ⚙️ Settings")
    
    if st.sidebar.button("🔄 Reset Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # About
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    Math Mentor uses:
    - 🤖 Multi-Agent AI System
    - 📚 RAG for Knowledge Retrieval
    - 👤 Human-in-the-Loop Validation
    - 🧠 Self-Learning Memory
    """)


def main():
    """Main application function."""
    initialize_session_state()
    
    # Initialize RAG on first run
    initialize_rag()
    
    # Render sidebar
    render_sidebar()
    
    # Main header
    st.markdown("""
    <h1 style="text-align: center; margin-bottom: 0;">
        🧮 Math Mentor
    </h1>
    <p style="text-align: center; color: #94a3b8; margin-top: 0;">
        AI-Powered JEE Math Tutor with Multimodal Input
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input section
    problem_text, input_confidence, needs_review = render_input_section()
    
    # Solve button
    if problem_text and st.button("🚀 Solve Problem", use_container_width=True, type="primary"):
        # Generate problem ID
        st.session_state.current_problem_id = str(uuid.uuid4())
        
        # Solve
        result = solve_problem(
            problem_text,
            st.session_state.input_mode,
            input_confidence
        )
        
        st.session_state.result = result
    
    # Display result
    if st.session_state.result:
        render_result_section(st.session_state.result)


if __name__ == "__main__":
    main()
