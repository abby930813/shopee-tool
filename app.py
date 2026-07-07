import streamlit as st
import pandas as pd
from io import BytesIO
import requests
import re

st.set_page_config(page_title="Shopee Tool v4.0", layout="wide")

st.title("蝦皮商品擷取工具 v4.0")

url = st.text_input(
    "貼上蝦皮網址",
    placeholder="https://shopee.tw/shopee_choice_hl?page=0..."
)

def get_brand(title):
    title = title.replace("【蝦皮直營】", "").strip()

    if not title:
        return ""

    return title.split()[0]

if st.button("開始擷取"):

    if not url:
        st.warning("請輸入網址")
        st.stop()

    result = []

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        html = requests.get(
            url,
            headers=headers,
            timeout=30
        ).text

        pattern = r'"name":"(.*?)".*?"price":(\d+)'

        matches = re.findall(
            pattern,
            html
        )

        for item in matches:

            title = item[0]

            price = round(
                int(item[1]) / 100000
            )

            result.append({
                "品牌": get_brand(title),
                "品名": title,
                "價格": price,
                "商品網址": url
            })

        df = pd.DataFrame(result)

        df = df.drop_duplicates()

        st.success(
            f"共抓取 {len(df)} 筆商品"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        st.download_button(
            "下載 Excel",
            output.getvalue(),
            "shopee_products.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(str(e))
