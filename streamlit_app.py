import openai
import streamlit as st

with st.sidebar:
    st.title('🤖ChatBPT')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided! You are good to go!', icon='✅')
        openai.api_key= st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key= st.text_input('Enter OpenAI token:', type='password')   
        if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
            st.warning('Please enter a valid OpenAI token!',icon='⚠️') 
        else:
            st.success("Now don't waste my time! I'm Hungry!", icon='😋')    


if 'messages' not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('Feed me questions!'):
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        message_placeholder= st.empty()
        full_response= '' 
        for response in openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role':m['role'], 'content':m['content']}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get('content','')
            message_placeholder.markdown(full_response + '')
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({'role':'assistant','content':full_response})


