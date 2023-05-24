import streamlit as st
import openai
import time
import random

openai.api_key = st.secrets["api_key"]

# Put local background
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('background.png')

# Set character
POSI = st.secrets["POSI"]
NEGA = st.secrets["NEGA"]
Name_guy = random.choice(["Liam", "Noah", "Oliver", "Ethan", "Lucas", "Jack", "Harry", "George", "James", "Charlie", "Minsoo"])
Name_lady = random.choice(["Emma", "Olivia", "Ava", "Isabella", "Mia", "Sophia", "Grace", "Lily", "Charlotte", "Amelia"])

st.title("Two GPT having a conversation")

with st.form("form"):    
    First_model_C = st.selectbox("First model's character (Set its character and click the Set button)", ["- Select -", "Positive", "Negative", "Custom"]) #First model's character
    next_button = st.form_submit_button("Set")
    if First_model_C == "Custom":
        First_model_C = st.text_area("Custom: (After customizing click Set button again.)", key="first_custom_input")
    else:
        First_model_C = POSI if First_model_C == "Positive" else NEGA

with st.form("form_2"):
    Second_model_C = st.selectbox("Second model's character", ["- Select -", "Positive", "Negative", "Custom"])
    next_button = st.form_submit_button("Set")
    if Second_model_C == "Custom":
        Second_model_C = st.text_area("Custom: (After customizing click set button again.)", key="second_custom_input")
    else:
        Second_model_C = POSI if Second_model_C == "Positive" else NEGA
    
with st.form("form_3"):
    Language_set = st.text_input("Set Language")
    Conversation_lan = st.selectbox("How many times would you like to proceed with the conversation?", [3, 5, 7, 10])
    Topic = st.text_input("Set the topic for conversation or discussion")
    submit = st.form_submit_button("Submit")
    
if Language_set and Conversation_lan and Topic and submit:
    model = "gpt-3.5-turbo"
    
    with st.spinner(f"{Name_guy} is thinking..."):
        model1 = openai.ChatCompletion.create(
            model = model,
            messages=[
                {"role":"system", "content":f"{First_model_C}. You must reply in two simple sentences with {Language_set}."},
                {"role":"user", "content":f"Let's have a discussion. Give a specific answer to this {Topic}. Make a any question about that topic."}
            ]
        )
    
    st.write(f"{Name_guy} : ", model1.choices[0].message.content)

    for i in range(int(Conversation_lan)):
        time.sleep(1)
        with st.spinner(f"{Name_lady} is thinking..."):
            model2 = openai.ChatCompletion.create(
                model = model,
                messages=[
                    {"role":"system", "content":f"{Second_model_C}. You must reply in two simple sentences with {Language_set}. You should ask a question which is related previous answer and {Topic} with reason. The answer should not be off the {Topic}."},
                    {"role":"user", "content":model1.choices[0].message.content}
                ]
            )
        
        st.write(f"{Name_lady} : ", model2.choices[0].message.content)
        
        time.sleep(1)
        with st.spinner(f"{Name_guy} is thinking..."):
            model1 = openai.ChatCompletion.create(
                model = model,
                messages=[
                    {"role":"system", "content":f"{First_model_C}. You must reply in two simple sentences with {Language_set}. You should ask a question which is related previous answer and {Topic} with reason. The answer should not be off the {Topic}."},
                    {"role":"user", "content":model2.choices[0].message.content}
                ]
            )
        
        st.write(f"{Name_guy} : ", model1.choices[0].message.content+"\n")
        
# Feel free to ask me about the code!!