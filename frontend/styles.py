CSS = """
<style>
.main {
    background-color: #f0f0f0;
}
.big-font {
    font-size: 40px !important;
    font-weight: bold;
    color: #4B0082;
    text-align: center;
}
.stButton > button {
    display: inline-block;
    padding: 10px 24px;
    font-size: 16px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: #fff !important;
    background-color: #4B0082 !important;
    border: none !important;
    border-radius: 5px !important;
}
.stButton > button:hover {
    background-color: #3a006c !important;
}
.stButton > button:active {
    background-color: #2d0052 !important;
}
.summary-box {
    background-color: #f8f9fa;
    border-radius: 5px;
    padding: 20px;
    border-left: 5px solid #4B0082;
    margin: 10px 0;
    width: calc(100% - 20px);  /* Ensures the width matches the input text area */
    max-width: 100%;
    overflow-y: auto;  /* Allow scrolling if the text exceeds the area */
}
.stTextArea, .summary-box {
    display: block;
    width: 100%;
}
</style>
"""