import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

# --- 1. SAYFA AYARLARI VE TASARIM (CSS) ---
st.set_page_config(page_title="Agentic AI Book Hub", page_icon="🤖", layout="wide")

def local_css():
    st.markdown("""
    <style>
    /* Arka Plan Görseli */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://images.unsplash.com/photo-1507842217343-583bb7270b66?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
    }
    
    /* Kart Efekti (Glassmorphism) */
    .main-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    /* Başlık Fontu */
    h1, h2, h3 {
        font-family: 'Trebuchet MS', sans-serif;
        color: #FFD700 !important; /* Altın Sarısı */
        text-shadow: 2px 2px 4px #000000;
    }
    
    /* Buton Tasarımı */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: black !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. GİRİŞ / KAYIT SİSTEMİ (BASİT MODEL) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_screen():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.header("👤 Kullanıcı Girişi")
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        
        with tab1:
            user = st.text_input("Kullanıcı Adı")
            pwd = st.text_input("Şifre", type="password")
            if st.button("Giriş"):
                if user == "admin" and pwd == "1234": # Demo için
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Hatalı kullanıcı adı veya şifre.")
        
        with tab2:
            st.text_input("E-posta Adresi")
            st.text_input("Yeni Şifre", type="password")
            st.button("Hesap Oluştur")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. ANA UYGULAMA ---
if not st.session_state['logged_in']:
    login_screen()
else:
    # API Ayarları
    os.environ["OPENAI_API_KEY"] = "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"
    os.environ["SERPER_API_KEY"] = "854b3a3e7b17a112569127fdc86e920ad60499a5"
    asistan_beyni = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    search_tool = SerperDevTool()

    # Üst Menü
    col_l, col_r = st.columns([8,1])
    with col_r:
        if st.button("Çıkış Yap"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.title("🤖 Multi-Agent AI: Akıllı Kitap Asistanı")
    
    # Giriş Alanı
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    user_input = st.text_area("Ruh halinizi veya aradığınız konuyu tarif edin:", 
                              placeholder="Örn: Bugün kendimi bir dedektif gibi hissediyorum, gizemli bir olay çözmek istiyorum...")
    
    if st.button("Ajanları Harekete Geçir 🚀"):
        with st.spinner('Ajanlar iş başında... Lütfen bekleyin.'):
            try:
                # Ajanlar ve Görevler (Aynı kalıyor)
                duygu_ajani = Agent(role='Duygu Analisti', goal='Duygu tespiti', backstory='Psikolog.', llm=asistan_beyni)
                tema_ajani = Agent(role='Tema Küratörü', goal='Tema belirleme', backstory='Edebiyatçı.', llm=asistan_beyni)
                oneri_ajani = Agent(role='Pazar Araştırmacısı', goal='Fiyat/Yorum bul', backstory='Araştırmacı.', tools=[search_tool], llm=asistan_beyni)
                editor_ajani = Agent(role='Baş Editör', goal='Final raporu', backstory='Yazar.', llm=asistan_beyni)

                task1 = Task(description=f'Analiz: {user_input}', expected_output='Duygu.', agent=duygu_ajani)
                task2 = Task(description='Tema belirle.', expected_output='Tema.', agent=tema_ajani, context=[task1])
                task3 = Task(description='2 kitap bul, fiyat ve yorum getir.', expected_output='Detaylı liste.', agent=oneri_ajani, context=[task2])
                task4 = Task(description='Markdown rapor oluştur.', expected_output='Final raporu.', agent=editor_ajani, context=[task1, task2, task3])

                crew = Crew(agents=[duygu_ajani, tema_ajani, oneri_ajani, editor_ajani], tasks=[task1, task2, task3, task4])
                result = crew.kickoff()
                
                st.markdown("### 📋 Analiz Sonuçları")
                st.success("Ajanlar raporu tamamladı!")
                st.info(result)
            except Exception as e:
                st.error(f"Hata: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

