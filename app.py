import streamlit as st
from openai import OpenAI
import os

# --- КОНФИГУРАЦИЯ ---
VALID_KEYS = ['VIP_MEMBER_777', 'LOCAL_READY_PRO', 'SUPER_SELLER']
st.set_page_config(page_title="Global-Ready", layout="centered")

# Инициализация состояния сессии
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

st.title("🛍️ Global-Ready")
st.write("Transform your product cards for the Chinese E-commerce Market")

# --- ЛОГИКА PAYWALL ---
if not st.session_state.is_pro and st.session_state.request_count >= 1:
    st.error("🚫 Free trial limit reached!")
    st.warning("Liked the result? To unlock unlimited access and exclusive PRO features (Slang Localization & Cultural Risk Assessment), text me on Telegram: [ТВОЯ_ССЫЛКА_НА_ТГ]. The price is just 300 rubles!")
    
    key_input = st.text_input("Enter your secret access key:")
    if st.button("Activate"):
        if key_input in VALID_KEYS:
            st.session_state.is_pro = True
            st.success("PRO status activated! Refreshing...")
            st.rerun()
        else:
            st.error("Invalid key.")
    st.stop() # Блокируем выполнение кода ниже

# --- ОСНОВНОЙ КОД ---
raw_token = os.environ.get("GITHUB_TOKEN", "")
api_key = "".join(c for c in raw_token if c.isalnum() or c == "_")

product_name = st.text_input("Product Name (e.g., Oversize Hoodie)")
product_desc = st.text_area("Original Product Description (English)")
category = st.selectbox("Target Audience Category", [
    "Gen Z / Tech-savvy youth", "Young professionals / Office workers", 
    "Parents / Family-oriented", "Health & Wellness enthusiasts"
])

# --- ЛОГИКА ПРОВЕРКИ КНОПКИ ---
if st.button("Analyze & Localize"):
    # 1. Сначала проверяем лимит
    if not st.session_state.is_pro and st.session_state.request_count >= 1:
        st.error("🚫 Free trial limit reached!")
        st.rerun() # Мгновенно перезапускаем, чтобы показать пейволл
    
    # 2. Если лимит не исчерпан, идем дальше
    elif not api_key:
        st.error("Error: GITHUB_TOKEN is missing.")
    elif not product_name or not product_desc:
        st.warning("Please fill in both fields.")
    else:
        # Увеличиваем счетчик ДО выполнения запроса
        st.session_state.request_count += 1
        with st.spinner("Analyzing..."):
            try:
                client = OpenAI(base_url="https://models.inference.ai.azure.com", api_key=api_key)
                
                # ... (здесь остальной код с промптом без изменений) ...
                system_instruction = (
                    "You are an expert E-commerce Product Manager specializing in the Chinese market. "
                    "Provide your response in English, structured with Markdown headers: "
                    "### 1. Adapted Text\n\n### 2. Marketplace Tips\n\n### 3. SEO Keywords."
                )
                
                if st.session_state.is_pro:
                    system_instruction += (
                        "\n\n### 4. PRO: Chinese Slang Translation\nTranslate the product name and description into Chinese using trending slang from Taobao/Dewu.\n"
                        "### 5. PRO: Cultural Risk Assessment\nAnalyze the text for any cultural taboos, censorship risks, or superstitions in China."
                    )
                
                user_content = f"Product: {product_name}\nDescription: {product_desc}\nAudience: {category}"
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_content}]
                )
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
                