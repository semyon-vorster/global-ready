import streamlit as st
from openai import OpenAI
import os

# 1. Настройка внешнего вида сайта
st.set_page_config(
    page_title="Global-Ready | E-commerce AI Assistant",
    page_icon="🛍️",
    layout="centered"
)

# Безопасно берём ключ из переменных окружения сервера (для Render)
api_key = os.environ.get("GITHUB_TOKEN", "")

st.title("🛍️ Global-Ready")
st.subheader("Transform your product cards for the Chinese E-commerce Market")
st.write("This AI-powered assistant localizes your Western product descriptions, provides tactical platform tips, and optimizes your SEO strategy for platforms like Taobao, JD, and Douyin.")

st.divider()

# 2. Форма ввода данных на сайте
product_name = st.text_input("Product Name (e.g., Oversize Hoodie, Wireless Earbuds)", "")
product_desc = st.text_area("Original Product Description (English)", "", height=150)

# Выбор целевой категории
category = st.selectbox(
    "Target Audience Category",
    ["Gen Z / Tech-savvy youth", "Young professionals / Office workers", "Parents & Families", "Health & Fitness enthusiasts"]
)

# Кнопка запуска генерации
if st.button("Analyze & Localize"):
    if not api_key:
        st.warning("API Key is missing. Please configure GITHUB_TOKEN on the hosting server.")
    elif not product_name or not product_desc:
        st.error("Please fill in both the Product Name and Description.")
    else:
        with st.spinner("Analyzing market fit and generating localization strategy..."):
            try:
                # Подключение к серверам GitHub Models
                client = OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=api_key
                )
                
                system_instruction = (
                    "You are an expert E-commerce Product Manager specializing in cross-border trade and the Chinese digital market. "
                    "Your goal is to take a Western product description and adapt it completely to succeed on Chinese marketplaces (Taobao, JD, Douyin/TikTok). "
                    "Provide your response in English, structure it clearly using Markdown with the following exact headers:\n\n"
                    "### 🇨🇳 1. Adapted Text & Cultural Hooks\n"
                    "Provide localized selling hooks, slogans, or key text. Explain which emotional triggers work best for the chosen target audience in China.\n\n"
                    "### 📊 2. Marketplace & Platform Tips\n"
                    "Recommend specific platforms (Taobao, JD, Douyin, or Xiaohongshu) for this product and explain why. Give tactical advice on pricing or positioning.\n\n"
                    "### 🔍 3. SEO Keywords & Visual Recommendations\n"
                    "Provide 5 Chinese SEO keywords (with English translations) and describe what style of product photos or short videos will convert highest in China."
                )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": f"Product: {product_name}\nDescription: {product_desc}\nTarget Audience: {category}"}
                    ]
                )
                
                st.success("Analysis Complete!")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.divider()
st.caption("© 2026 Semyon Vorster. Built for Digital Management & E-commerce Portfolio.")
