"""
UI Components for the Math Mentor Streamlit app.
"""

import streamlit as st
from typing import Dict, Any, List, Optional


def render_input_selector() -> str:
    """Render input mode selector tabs.
    
    Returns:
        Selected mode: 'text', 'image', or 'audio'.
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⌨️ Text", key="mode_text", use_container_width=True):
            st.session_state.input_mode = "text"
    
    with col2:
        if st.button("📷 Image", key="mode_image", use_container_width=True):
            st.session_state.input_mode = "image"
    
    with col3:
        if st.button("🎤 Audio", key="mode_audio", use_container_width=True):
            st.session_state.input_mode = "audio"
    
    return st.session_state.get("input_mode", "text")


def render_extraction_preview(
    text: str,
    confidence: float,
    editable: bool = True
) -> str:
    """Render extraction preview with confidence.
    
    Args:
        text: Extracted text.
        confidence: Confidence score (0-1).
        editable: Whether text is editable.
        
    Returns:
        Edited text (or original if not editable).
    """
    st.markdown("### 📝 Extracted Text")
    
    # Confidence bar
    render_confidence_bar(confidence, "Extraction Confidence")
    
    if editable:
        edited = st.text_area(
            "Review and edit if needed:",
            value=text,
            height=150,
            key="extraction_preview"
        )
        
        if confidence < 0.6:
            st.warning("⚠️ Low confidence extraction. Please review carefully.")
        
        return edited
    else:
        st.markdown(f"```\n{text}\n```")
        return text


def render_agent_trace(traces: List[Dict[str, Any]]) -> None:
    """Render agent execution trace.
    
    Args:
        traces: List of trace dictionaries.
    """
    st.markdown("### 🔄 Agent Trace")
    
    for trace in traces:
        status = trace.get("status", "success")
        icon = "✅" if status == "success" else "⚠️" if status == "hitl_triggered" else "❌"
        
        status_color = {
            "success": "#22c55e",
            "hitl_triggered": "#f59e0b",
            "error": "#ef4444"
        }.get(status, "#6366f1")
        
        st.markdown(f"""
        <div style="
            background-color: #1e293b;
            border-left: 4px solid {status_color};
            padding: 12px 16px;
            margin: 8px 0;
            border-radius: 0 8px 8px 0;
        ">
            <strong>{icon} {trace.get('agent', 'Agent')}</strong>
            <span style="color: #94a3b8; margin-left: 12px;">
                {trace.get('duration', 'N/A')}
            </span>
            <br/>
            <span style="color: #cbd5e1; font-size: 14px;">
                {trace.get('summary', '')}
            </span>
        </div>
        """, unsafe_allow_html=True)


def render_context_panel(sources: List[Dict[str, Any]]) -> None:
    """Render retrieved context panel.
    
    Args:
        sources: List of source dictionaries.
    """
    if not sources:
        return
    
    st.markdown("### 📚 Retrieved Context")
    
    for source in sources:
        with st.expander(f"📄 {source.get('topic', 'Source')} ({source.get('relevance', 'N/A')})"):
            st.markdown(f"**Category:** {source.get('category', 'N/A')}")
            st.markdown(f"**Source:** `{source.get('source', 'N/A')}`")
            st.markdown("---")
            st.markdown(source.get('preview', ''))


def render_solution_display(
    answer: str,
    explanation: Dict[str, Any],
    markdown_explanation: str
) -> None:
    """Render solution and explanation.
    
    Args:
        answer: Final answer.
        explanation: Explanation dictionary.
        markdown_explanation: Markdown formatted explanation.
    """
    st.markdown("### 🎯 Solution")
    
    # Answer box
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1e3a5f 0%, #1e293b 100%);
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 16px 0;
    ">
        <span style="color: #94a3b8; font-size: 14px;">FINAL ANSWER</span>
        <h2 style="color: #f8fafc; margin: 8px 0;">{answer}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed explanation
    st.markdown("### 📖 Step-by-Step Explanation")
    
    steps = explanation.get("steps", [])
    for step in steps:
        render_step_card(step)
    
    # Tips and concepts
    concepts = explanation.get("concepts", [])
    tips = explanation.get("tips", [])
    warnings = explanation.get("warnings", [])
    
    if concepts:
        st.markdown("#### 💡 Key Concepts")
        for concept in concepts:
            st.markdown(f"- {concept}")
    
    if tips:
        st.markdown("#### 🎓 Tips")
        for tip in tips:
            st.info(tip)
    
    if warnings:
        st.markdown("#### ⚠️ Watch Out")
        for warning in warnings:
            st.warning(warning)


def render_step_card(step: Dict[str, Any]) -> None:
    """Render a single solution step.
    
    Args:
        step: Step dictionary.
    """
    step_num = step.get("number", "?")
    title = step.get("title", f"Step {step_num}")
    content = step.get("content", "")
    math = step.get("math", "")
    
    st.markdown(f"""
    <div style="
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    ">
        <span style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            color: white;
            border-radius: 50%;
            font-weight: 700;
            margin-right: 12px;
        ">{step_num}</span>
        <strong style="color: #f8fafc;">{title}</strong>
        <p style="color: #cbd5e1; margin: 12px 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if math:
        st.code(math, language="")


def render_confidence_bar(confidence: float, label: str = "Confidence") -> None:
    """Render a confidence progress bar.
    
    Args:
        confidence: Confidence score (0-1).
        label: Label for the bar.
    """
    percentage = int(confidence * 100)
    
    color = "#22c55e" if confidence >= 0.8 else "#f59e0b" if confidence >= 0.6 else "#ef4444"
    
    st.markdown(f"""
    <div style="margin: 8px 0;">
        <span style="color: #94a3b8; font-size: 14px;">{label}: {percentage}%</span>
        <div style="
            height: 8px;
            background-color: #334155;
            border-radius: 4px;
            margin-top: 4px;
            overflow: hidden;
        ">
            <div style="
                height: 100%;
                width: {percentage}%;
                background-color: {color};
                border-radius: 4px;
                transition: width 0.5s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_feedback_buttons(problem_id: str) -> Optional[str]:
    """Render feedback buttons.
    
    Args:
        problem_id: ID of the problem for feedback.
        
    Returns:
        Feedback value or None.
    """
    st.markdown("### 📝 Was this solution helpful?")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    feedback = None
    
    with col1:
        if st.button("✅ Correct", key=f"correct_{problem_id}", use_container_width=True):
            feedback = "correct"
    
    with col2:
        if st.button("❌ Incorrect", key=f"incorrect_{problem_id}", use_container_width=True):
            feedback = "incorrect"
    
    if feedback == "incorrect":
        with col3:
            comment = st.text_input(
                "What was wrong?",
                key=f"comment_{problem_id}",
                placeholder="Please describe the issue..."
            )
            st.session_state.feedback_comment = comment
    
    return feedback


def render_hitl_interface(
    trigger_reason: str,
    original_text: str,
    requires_edit: bool = True
) -> Dict[str, Any]:
    """Render the HITL intervention interface.
    
    Args:
        trigger_reason: Reason for HITL trigger.
        original_text: Original text to review.
        requires_edit: Whether editing is required.
        
    Returns:
        Dict with user's response.
    """
    st.warning(f"🔔 **Review Required:** {trigger_reason}")
    
    response = {"approved": False, "edited_text": original_text, "action": None}
    
    if requires_edit:
        edited = st.text_area(
            "Edit the text:",
            value=original_text,
            height=150,
            key="hitl_edit"
        )
        response["edited_text"] = edited
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Approve & Continue", use_container_width=True):
                response["approved"] = True
                response["action"] = "approve"
        
        with col2:
            if st.button("🔄 Re-process", type="secondary", use_container_width=True):
                response["action"] = "reprocess"
    else:
        st.markdown(f"**Content to review:**\n\n{original_text}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Approve", use_container_width=True):
                response["approved"] = True
                response["action"] = "approve"
        
        with col2:
            if st.button("❌ Reject", type="secondary", use_container_width=True):
                response["action"] = "reject"
        
        with col3:
            if st.button("🔄 Re-check", type="secondary", use_container_width=True):
                response["action"] = "recheck"
    
    return response


def render_memory_sidebar(stats: Dict[str, Any]) -> None:
    """Render memory statistics in sidebar.
    
    Args:
        stats: Memory statistics dictionary.
    """
    st.sidebar.markdown("### 🧠 Memory")
    
    st.sidebar.metric("Problems Solved", stats.get("total_problems", 0))
    
    feedback = stats.get("by_feedback", {})
    correct = feedback.get("correct", 0)
    incorrect = feedback.get("incorrect", 0)
    
    if correct + incorrect > 0:
        accuracy = correct / (correct + incorrect)
        st.sidebar.metric("Accuracy", f"{accuracy:.1%}")
    
    st.sidebar.metric("Learned Patterns", stats.get("total_corrections", 0))
    
    # Topic distribution
    topics = stats.get("by_topic", {})
    if topics:
        st.sidebar.markdown("#### Topics Covered")
        for topic, count in sorted(topics.items(), key=lambda x: -x[1])[:5]:
            st.sidebar.text(f"{topic}: {count}")
