import streamlit as st
from openai import OpenAI
import os
import sys

# Настройка кодировки, чтобы Render больше никогда не выдавал ошибку ASCII
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

st.set_page_config(page_title="Global-Ready", layout="centered")
st.title("🛍️ Global-Ready")
st.write("Transform your product cards for the Chinese E-commerce Market")

# Берем токен строго из скрытых переменных окружения Render
api_key = os.environ.get("GITHUB_TOKEN", "")

product_name = st.text_input("Product Name (e.g., Oversize Hoodie)")
product_desc = st.text_area("Original Product Description (English)")
category = st.selectbox("Target Audience Category", [
    "Gen Z / Tech-savvy youth", 
    "Young professionals / Office workers", 
    "Parents / Family-oriented", 
    "Health & Wellness enthusiasts"
])

if st.button("Analyze & Localize"):
    if not api_key:
        st.error("Error: GITHUB_TOKEN is missing in Render environment variables.")
    elif not product_name or not product_desc:
        st.warning("Please fill in both the Product Name and Description.")
    else:
        with st.spinner("Analyzing..."):
            try:
                client = OpenAI(
                    base_url="https://models.inference.ai.azure.com", 
                    api_key=api_key
                )
                
                system_instruction = (
                    "You are an expert E-commerce Product Manager specializing in the Chinese market. "
                    "Adapt the product description for Chinese marketplaces like Taobao or JD. "
                    "Provide your response in English, structured with Markdown headers: "
                    "### 1. Adapted Text\n\n### 2. Marketplace Tips\n\n### 3. SEO Keywords."
                )
                
                user_content = f"Product: {product_name}\nDescription: {product_desc}\nAudience: {category}"
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ]
                )
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")