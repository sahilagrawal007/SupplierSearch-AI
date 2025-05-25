from llm import ask_deepseek
from mfg_scrap import scrap_mfg
from scrap import scrap_suppliers
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Supplier Agent",
    page_icon="🤖",
    layout="centered",
)

# Custom CSS for sleek UI
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
    }
    .stTextInput, .stButton > button {
        border-radius: 15px;
        font-size: 18px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("<h2 style='text-align: center;'>AI Supplier Agent</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask me about commodities and I will find the best suppliers for you!</p>", unsafe_allow_html=True)

# User Input
query = st.text_input("Enter the commodity or process you're looking for:", placeholder="e.g., Die casting, stamping, forging. etc.")

# Send Button
if st.button("Send"):
    if query.strip() == "":
        st.warning("Please enter a valid query!")
    else:
        # ######### LLM CODE START
        # with st.spinner("Thinking..."):
        #     # Get response from deepseek() function
        #     response = ask_deepseek(query)

        #     if type(response) == str:
        #         st.error(response)
        #     else:
        #         st.success(f"Following commodities are majorly involved in {query}:")
        #         st.write(response)
        #         for item in response:
        #             supplier_data = scrap_suppliers(item)
        #             st.success(f"Supplier data for {item}:")
        #             st.write(supplier_data)
        # ######### LLM CODE END



        ########## MFG CODE START
        with st.spinner("Thinking..."):
            # Get response from deepseek() function
            mfg_data = scrap_mfg(query)
            st.success(f"MFG data for {query}:")
            st.write(mfg_data)
        ########## MFG CODE END




#Sidebar
st.sidebar.markdown("### About")
st.sidebar.info(
    "This AI agent connects buyers and suppliers by providing information about various commodities. "
    "Powered by Streamlit and a sophisticated scraping & LLM pipeline."
)

st.sidebar.markdown("### Contact")
st.sidebar.write("For inquiries or collaboration, contact [Sahil Agrawal](mailto:sahilagrawal8090@gmail.com).")
