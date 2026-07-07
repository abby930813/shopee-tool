import streamlit as st

st.title("蝦皮商品擷取工具 v3.0")

url = st.text_input("貼上蝦皮網址")

if st.button("開始擷取"):
    st.write("網址：", url)
