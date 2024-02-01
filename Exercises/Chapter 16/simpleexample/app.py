import streamlit as st
from mycomponent import mycomponent
value = mycomponent(input_url="hello there")
st.write("Received", value)