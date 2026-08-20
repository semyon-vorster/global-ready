import streamlit as st
import os
import urllib.request
import json

# --- КОНФИГУРАЦИЯ ---
VALID_KEYS = ['VIP_MEMBER_777', 'LOCAL_READY_PRO', 'SUPER_SELLER', 'SuperAdmin', 'itworks', 'HOPEYOULGETTHERE', 'SAYHITOME']

# Инициализация состояния сессии
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

st.title("🛍️ Global-Ready")
st.write("Transform your product cards for the Chinese E-commerce Market")

# --- PAYWALL LOGIC ---
if not st.session_state.is_pro and st.session_state.request_count >= 1:
    st.error("🚫 Free trial limit reached!")
    st.info("### 🔓 Get Unlimited PRO Access")
    st.write("Unlock advanced cultural risk assessment and professional localization for only 300 RUB.")
    st.link_button("Buy PRO Access (300 RUB)", "https://yoomoney.ru/fundraise/11STNB46009.260708")
    st.divider()
    st.write("1. Complete the payment via the link above.")
    st.write("2. Message me on Telegram @id405158563 (@shivaro) with your payment confirmation.")
    st.write("3. Get your instant activation key!")
    
    key_input = st.text_input("Enter your activation key:")
    if st.button("Activate"):
        if key_input in VALID_KEYS:
            st.session_state.is_pro = True
            st.success("PRO status activated! Please refresh.")
            st.rerun()
        else:
            st.error("Invalid Key")
    st.stop()

# --- ФОРМА ВВОДА ---
product_name = st.text_input("Product Name (e.g., Oversize Hoodie)")
product_desc = st.text_area("Original Product Description (English)")
category = st.selectbox("Target Audience Category", [
    "Gen Z / Tech-savvy youth", "Young professionals / Office workers",
    "Parents / Family-oriented", "Health & Wellness enthusiasts"
])

# --- ЛОГИКА ГЕНЕРАЦИИ ---
if st.button("Analyze & Localize"):
    if not product_name or not product_desc:
        st.warning("Please fill in both fields.")
    else:
        st.session_state.request_count += 1
        with st.spinner("Analyzing..."):
            try:
                # Берем ключ из настроек Render (GEMINI_API_KEY или GITHUB_TOKEN)
                gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GITHUB_TOKEN") or ""
                
                system_instruction = (
                    "You are an expert E-commerce Product Manager specializing in the chinese market. "
                    "Provide your response in English, structured with Markdown headers: "
                    "### 1. Adapted Text\n\n### 2. Marketplace Tips\n\n### 3. SEO Keywords."
                )

                if st.session_state.is_pro:
                    system_instruction += (
                        "\n\n### 4. PRO: Chinese Slang Translation\nTranslate the product name and description into Chinese using trending e-commerce slang."
                        "\n### 5. PRO: Cultural Risk Assessment\nAnalyze the text for any cultural taboos, censorship risks, or superstition concerns."
                    )

                user_content = f"Product: {product_name}\nDescription: {product_desc}\nAudience: {category}"

                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{system_instruction}\n\n{user_content}"}]
                    }]
                }

                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )

                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    text_output = res_data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(text_output)

            except Exception as e:
                st.error(f"Error: {e}")
