import streamlit as st
import edge_tts
import asyncio
import time

# --- ၁။ Page Setup ---
st.set_page_config(
    page_title="Burmese Voice AI",
    page_icon="🇲🇲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ၂။ CSS Design (Dark Mode + Improved Layout) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Padauk:wght@400;700&display=swap');

    /* Deploy Bar နှင့် Header များဖျောက်ခြင်း */
    .stAppHeader, header, footer { visibility: hidden; height: 0px; }
    #MainMenu { visibility: hidden; height: 0px; }
    
    .stApp {
        background-color: #1A1C24;
        color: #E0E0E0;
        font-family: 'Padauk', sans-serif;
        margin-top: -70px; /* အပေါ်သို့ ပိုကပ်စေရန် */
    }
    
    /* Header Container (အလံနှင့်စာသား တစ်တန်းတည်းဖြစ်စေရန်) */
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 10px 0;
    }

    h1 { color: #FFD700 !important; margin: 0; padding: 0; font-size: 32px !important; }
    .caption-text { color: #B0B3B8; font-size: 14px; margin-top: -5px; }

    /* Input & UI Elements */
    .stTextArea textarea {
        background-color: #2C2F38;
        color: #FFFFFF;
        border: 1px solid #4A4D55 !important;
        border-radius: 12px;
    }
    
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #1A1C24;
        border: none;
        padding: 0.7rem;
        border-radius: 10px;
        font-weight: bold;
        font-size: 18px !important;
    }

    .result-box {
        margin-top: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #FFD700;
        border-radius: 12px;
        text-align: center;
        color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ၃။ Inline Header (အလံနှင့် ခေါင်းစဉ် တစ်တန်းတည်း) ---
st.markdown(f"""
    <div class="header-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Flag_of_Myanmar.svg/320px-Flag_of_Myanmar.svg.png" width="60">
        <div>
            <h1>Burmese Voice AI</h1>
            <div class="caption-text">Professional Text-to-Speech Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-top: 1px solid #333;'>", unsafe_allow_html=True)

# --- ၄။ Settings & Input ---
col1, col2 = st.columns(2)
with col1:
    voice_option = st.selectbox("🗣️ အသံရွေးချယ်ပါ", ("ကိုရဲ (Male)", "မီမီ (Female)"))
with col2:
    speed = st.slider("🚀 အမြန်နှုန်း", -50, 50, 0, step=10)

SELECTED_VOICE = "my-MM-ThihaNeural" if "ကိုရဲ" in voice_option else "my-MM-NilarNeural"
speed_str = f"{speed:+d}%"

st.markdown("### 📝 စာသား ရိုက်ထည့်ပါ")
text_input = st.text_area("Label", height=180, placeholder="မင်္ဂလာပါ... အသံပြောင်းလိုသော စာသားကို ရိုက်ထည့်ပါ...", label_visibility="collapsed")

# --- ၅။ Logic ---
async def text_to_speech(text, voice, rate, output_file):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("အသံဖိုင် ဖန်တီးမည် (Generate) ✨"):
    if not text_input.strip():
        st.warning("⚠️ ကျေးဇူးပြု၍ စာသား ရိုက်ထည့်ပေးပါ။")
    else:
        output_file = f"audio_{int(time.time())}.mp3"
        with st.spinner('ခဏစောင့်ပါ...'):
            try:
                asyncio.run(text_to_speech(text_input, SELECTED_VOICE, speed_str, output_file))
                st.markdown('<div class="result-box">✅ အောင်မြင်ပါသည်။ နားထောင်နိုင်ပါပြီ။</div>', unsafe_allow_html=True)
                st.audio(output_file, format='audio/mp3')
                with open(output_file, 'rb') as f:
                    st.download_button("Download MP3 📥", f, file_name="burmese_voice.mp3", mime="audio/mp3", use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.markdown("<br><div style='text-align: center; color: #555; font-size: 12px;'>Developed - Julian Evin | 2026 </div>", unsafe_allow_html=True)
