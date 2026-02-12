import streamlit as st
import edge_tts
import asyncio
import os

# ၁. Page အပြင်အဆင် သတ်မှတ်ခြင်း
st.set_page_config(
    page_title="Burmese Voice AI",
    page_icon="🇲🇲",
    layout="centered"
)

# ၂. Custom CSS (ဒီဇိုင်းအလှဆင်ခြင်း)
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .stTextArea > div > div > textarea {
        background-color: #262730;
        color: white;
        border-radius: 10px;
    }
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF2B2B;
        border-color: #FF2B2B;
    }
    .css-1v0mbdj {
        display: flex;
        justify-content: center;
    }
    h1 {
        text-align: center;
        color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# ၃. ခေါင်းစဉ်အပိုင်း
st.markdown("# 🇲🇲 Burmese Voice AI")
st.markdown("### မြန်မာစာများကို အသံဖြင့် ဖတ်ပြပေးမည့် နည်းပညာ")
st.divider()

# ၄. ဘယ်/ညာ ခွဲပြီး နေရာချခြင်း (Columns)
col1, col2 = st.columns([2, 1])

with col1:
    st.info("အသံပြောင်းလိုသော စာသားကို အောက်တွင် ရိုက်ထည့်ပါ 👇")
    text_input = st.text_area("စာသားရိုက်ရန်နေရာ:", height=200, label_visibility="collapsed", placeholder="မင်္ဂလာပါ... ဒီနေရာမှာ စာရေးပါ...")

with col2:
    st.write("### ⚙️ ဆက်တင်များ")
    voice_option = st.radio(
        "အသံရွေးချယ်ပါ:",
        ("ကိုသီဟ (Male)", "မနီလာ (Female)")
    )
    
    # Speed ထိန်းညှိခြင်း (အပိုထည့်ပေးထားပါတယ်)
    speed_option = st.slider("အမြန်နှုန်း (Speed):", -50, 50, 0, step=10)
    
    # Gender to Voice ID mapping
    if "ကိုသီဟ" in voice_option:
        VOICE = "my-MM-ThihaNeural"
    else:
        VOICE = "my-MM-NilarNeural"

    # Speed string conversion
    speed_str = f"{speed_option:+d}%"

st.divider()

# ၅. အသံပြောင်း Function
async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(text, VOICE, rate=speed_str)
    await communicate.save(output_file)

# ၆. လုပ်ဆောင်ခလုတ် (Action Button)
if st.button("🔊 အသံဖိုင် ဖန်တီးမည် (Generate Audio)"):
    if text_input.strip() == "":
        st.error("⚠️ ကျေးဇူးပြု၍ စာသား တစ်ခုခု ရိုက်ထည့်ပေးပါ!")
    else:
        output_file = "generated_audio.mp3"
        
        with st.spinner('ခဏစောင့်ပါ... အသံဖိုင် ပြောင်းနေပါပြီ... 🔄'):
            try:
                # Run Async Function
                asyncio.run(text_to_speech(text_input, output_file))
                
                # Success Message
                st.success("✅ အောင်မြင်ပါတယ်! အောက်တွင် နားထောင်နိုင်ပါပြီ။")
                
                # Audio Player Style
                audio_file = open(output_file, 'rb')
                audio_bytes = audio_file.read()
                
                # Center the audio player visually
                st.audio(audio_bytes, format='audio/mp3')
                
                # Download Button
                col_d1, col_d2, col_d3 = st.columns([1,2,1])
                with col_d2:
                    st.download_button(
                        label="⬇️ MP3 ဒေါင်းလုဒ်ဆွဲမည်",
                        data=audio_bytes,
                        file_name="my_story.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"❌ Error ဖြစ်သွားပါတယ်: {e}")

# Footer
st.markdown("---")
st.caption("Developed with ❤️ Julian Evin")