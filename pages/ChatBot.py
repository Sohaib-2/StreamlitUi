import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI

col1, col2 = st.columns([7.5, 1])

with col1:
    st.header("ChatBot")
with col2:
    if st.button("Logout"):
        del st.session_state['username']
        st.experimental_rerun()

if 'username' in st.session_state:
    st.subheader(f"Welcome, {st.session_state['username']}!")
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []


    def get_text():
        input_text = st.text_input("You:", st.session_state["input"], key="input",
                                   placeholder="Your AI assistant here! Ask me anything ...",
                                   label_visibility='hidden')
        return input_text


    def new_chat():
        save = []
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            save.append("User:" + st.session_state["past"][i])
            save.append("Bot:" + st.session_state["generated"][i])
        st.session_state["stored_session"].append(save)
        st.session_state["generated"] = []
        st.session_state["past"] = []
        st.session_state["input"] = ""


    with st.sidebar.expander("🛠️ Bot Setting", expanded=False):
        MODEL = st.selectbox(label='Model',
                             options=['gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002', 'code-davinci-002'])
        K = st.number_input(' (#)Summary of prompts to consider', min_value=3, max_value=1000)

    st.title("🤖 Chat Bot with 🧠")

    API_O = st.sidebar.text_input("API-KEY", type="password")

    if API_O:
        llm = ChatOpenAI(temperature=0, openai_api_key=API_O, model_name=MODEL, verbose=False)

        if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K)

        Conversation = ConversationChain(llm=llm, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
                                         memory=st.session_state.entity_memory)
    else:
        st.sidebar.warning('API key required to try this app. The API key is not stored in any form.')

    st.sidebar.button("New Chat", on_click=new_chat, type='primary')
    user_input = get_text()

    if st.button("Submit"):
        try:
            output = Conversation.run(input=user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)
        except:
            st.error("Enter Valid Api key first")

    download_str = []

    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            st.info(st.session_state["past"][i], icon="🧐")
            st.success(st.session_state["generated"][i], icon="🤖")
            download_str.append(st.session_state["past"][i])
            download_str.append(st.session_state["generated"][i])

        download_str = '\n'.join(download_str)
        if download_str:
            st.download_button('Download', download_str)

    for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label=f"Conversation-Session:{i}"):
            st.write(sublist)

    if st.session_state.stored_session:
        if st.sidebar.checkbox("Clear-all"):
            del st.session_state.stored_session
            st.experimental_rerun()

else:
    st.warning("Login to continue")
