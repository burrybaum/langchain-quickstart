import streamlit as st
from langchain.llms import OpenAI

st.set_page_config(page_title="DeepK PoC")
st.title('DeepK')

# Initialize session state for API key, query-result history, and selected history index
if 'show_api_key_input' not in st.session_state:
    st.session_state.show_api_key_input = True
if 'query_result_history' not in st.session_state:
    st.session_state.query_result_history = []
if 'selected_history_index' not in st.session_state:
    st.session_state.selected_history_index = None
if 'api_key' not in st.session_state:  # Ensure api_key is initialized
    st.session_state.api_key = ''  # Initialize with an empty string or a default value


# API Key Input Handling
def toggle_api_key_input():
    st.session_state.show_api_key_input = not st.session_state.show_api_key_input

if st.session_state.show_api_key_input:
    key_input = st.text_input('OpenAI API Key', key='api_key', value=st.session_state.api_key)
    hide_button = st.button('Hide API Key Input', on_click=toggle_api_key_input)
else:
    show_button = st.button('Show API Key Input', on_click=toggle_api_key_input)

# Sample Prompts and Button Click Handling
sample_prompts = [
    "(국가명)에서 (과목명)전공하고 싶은데 추천해줘",
    "()학교 ()학과 지원하려면 어떻게 준비해야해?",
    "()학교 ()학과 최대 장점에 대해서 알려줄 수 있어?",
    "()학교 ()학교 고민중인데 실제 생활은 어때? 안비싸?"
]

def on_prompt_click(prompt_text):
    st.session_state.selected_prompt = prompt_text

if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = "#대학(원) 입시 준비 #학교 학과 추천 #국내대학 #해외대학"

col1, col2 = st.columns(2)
with col1:
    for i in [0, 2]:
        st.button(sample_prompts[i], key=f"btn{i}", on_click=on_prompt_click, args=(sample_prompts[i],))
with col2:
    for i in [1, 3]:
        st.button(sample_prompts[i], key=f"btn{i}", on_click=on_prompt_click, args=(sample_prompts[i],))

# Form for user input and submission
with st.form('my_form', clear_on_submit=False):
    text = st.text_area('궁금한 점을 물어봐 주세요', value=st.session_state.selected_prompt, key='user_query')
    submitted = st.form_submit_button('Submit')


    

if submitted:
    openai_api_key = st.session_state.api_key
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠️')
    else:
        def generate_response(input_text):
            llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
            response = llm(input_text)  # Assuming this method correctly generates a response.
            return response
        
        response = generate_response(text)
        # Store query and response in session state
        st.session_state.query_result_history.append((text, response))
        st.info(response)

# Sidebar for query and result history
with st.sidebar:
    st.write("## Query and Result History")
    for query, result in reversed(st.session_state.query_result_history):
        st.write(f"**Query:** {query}")
        st.write(f"**Result:** {result}")
        st.write("---")
