"""
Custom CSS styles for the Math Mentor UI.
"""


def get_custom_css() -> str:
    """Get custom CSS for the Streamlit app.
    
    Returns:
        CSS string.
    """
    return """
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    h2, h3 {
        color: #e2e8f0 !important;
    }
    
    /* Cards */
    .stExpander {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
    }
    
    /* Input cards */
    .input-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(145deg, #1e3a5f 0%, #1e293b 100%);
        border: 1px solid #3b82f6;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
    }
    
    /* Agent trace */
    .agent-trace {
        background-color: #0f172a;
        border-left: 4px solid #6366f1;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .agent-trace.success {
        border-left-color: #22c55e;
    }
    
    .agent-trace.error {
        border-left-color: #ef4444;
    }
    
    .agent-trace.hitl {
        border-left-color: #f59e0b;
    }
    
    /* Confidence bar */
    .confidence-bar {
        height: 8px;
        border-radius: 4px;
        background: linear-gradient(90deg, #ef4444 0%, #f59e0b 50%, #22c55e 100%);
        position: relative;
        overflow: hidden;
    }
    
    .confidence-indicator {
        position: absolute;
        top: -4px;
        width: 16px;
        height: 16px;
        background: white;
        border-radius: 50%;
        border: 2px solid #0f172a;
    }
    
    /* Source badge */
    .source-badge {
        display: inline-block;
        background: linear-gradient(90deg, #3b82f6, #6366f1);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 4px;
    }
    
    /* Feedback buttons */
    .feedback-btn {
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .feedback-btn.correct {
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: white;
    }
    
    .feedback-btn.incorrect {
        background: linear-gradient(90deg, #ef4444, #dc2626);
        color: white;
    }
    
    /* Step card */
    .step-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .step-number {
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
    }
    
    /* Math display */
    .math-display {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
    
    /* Toast notifications */
    .toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 16px 24px;
        border-radius: 8px;
        background: #1e293b;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        z-index: 1000;
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: '';
        animation: dots 1.5s infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60%, 100% { content: '...'; }
    }
    
    /* Mode selector tabs */
    .mode-tab {
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .mode-tab.active {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
    }
    
    .mode-tab:hover:not(.active) {
        background-color: #334155;
    }
    
    /* Streamlit overrides */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    .stTextInput > div > div > input {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        color: #e2e8f0;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        color: #e2e8f0;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background-color: #1e293b;
        border: 2px dashed #334155;
        border-radius: 12px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid #22c55e;
        border-radius: 8px;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        border-radius: 8px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #0f172a;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
    }
</style>
"""


def get_loading_animation() -> str:
    """Get HTML for loading animation.
    
    Returns:
        HTML string.
    """
    return """
<div style="text-align: center; padding: 40px;">
    <div style="display: inline-block; width: 50px; height: 50px; 
                border: 4px solid #334155; border-top-color: #6366f1; 
                border-radius: 50%; animation: spin 1s linear infinite;">
    </div>
    <p style="color: #94a3b8; margin-top: 16px;">Processing<span class="loading-dots"></span></p>
</div>
<style>
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
"""
