import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="蝦皮商品擷取工具 v3.0",
    layout="wide"
)

st.title("蝦皮商品擷取工具 v3.0")

st.info(
    "貼入蝦皮商品資料文字內容，可自動整理品牌、品名、價格，並下載 Excel"
)

raw_text = st.text_area(
    "貼上蝦皮商品內容",
    height=350
)

def get_brand(product_name):
    text = product_name.replace("【蝦皮直營】", "").strip()

    if not text:
        return ""

    return text.split()[0]

if st.button("開始整理"):

    if not raw_text.strip():
        st.warning("請先貼入資料")
        st.stop()

    lines = [
        x.strip()
        for x in raw_text.split("\n")
        if x.strip()
    ]

    products = []

    current_name = None

    for line in lines:

        if "【蝦皮直營】" in line:

            current_name = line

            continue

        if current_name:

            if line.isdigit():

                products.append({
                    "品牌": get_brand(current_name),
                    "品名": current_name,
                    "價格": line
                })

                current_name = None

    df = pd.DataFrame(products)

    st.success(f"共整理 {len(df)} 筆商品")

    st.dataframe(
        df,
        use_container_width=True
    )

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Shopee"
        )

    st.download_button(
        label="下載 Excel",
        data=excel_buffer.getvalue(),
        file_name="shopee_products.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
