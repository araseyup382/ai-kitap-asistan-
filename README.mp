# 📚 Agentic AI: Akıllı Kitap ve İçerik Asistanı

Bu proje, **Çoklu Ajan Sistemleri (Multi-Agent Systems)** mimarisi kullanılarak geliştirilmiş profesyonel bir karar destek mekanizmasıdır. Kullanıcının ruh halini analiz ederek ona en uygun içeriği bulur, pazar araştırması yapar ve gerçek verilerle sunar.

## 🚀 Özellikler
- **Duygu Analizi:** Kullanıcı metinlerindeki derin anlamı ve psikolojik durumu tespit eder.
- **Otonom Ajanlar:** CrewAI altyapısı ile birbirleriyle haberleşen 4 farklı uzman ajan.
- **Gerçek Zamanlı Veri:** Serper API ile internet üzerinden güncel fiyat karşılaştırması ve gerçek kullanıcı yorumları.
- **Modern Arayüz:** Streamlit ile geliştirilmiş, kullanıcı dostu ve estetik web arayüzü.

## 🤖 Kullanılan Ajanlar
1. **Duygu Analisti:** Kullanıcının ruh halini belirler.
2. **Tema Küratörü:** Analize uygun edebi/içerik konseptini tasarlar.
3. **Pazar Araştırmacısı:** En uygun 2 ürünü bulur, fiyatlarını (Amazon, D&R, vb.) karşılaştırır.
4. **Baş Editör:** Tüm verileri profesyonel bir rapor haline getirir.

## 🛠️ Teknoloji Yığını
- **Dil:** Python 3.10+
- **AI Framework:** CrewAI, LangChain
- **LLM:** OpenAI GPT-4o-mini
- **Arayüz:** Streamlit (Custom CSS ile)
- **Veri:** Google Serper API

## 📋 Kurulum
```bash
# Depoyu klonlayın
git clone [DEPO_LINKINIZ]

# Kütüphaneleri kurun
pip install -r requirements.txt

# Uygulamayı çalıştırın
streamlit run app.py