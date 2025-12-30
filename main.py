import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# --- 1. AYARLAR VE ANAHTARLAR ---
# Buraya kendi API anahtarlarını yapıştır
os.environ["OPENAI_API_KEY"] = "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"

# Ajanların internette arama yapabilmesi için gerekli araç
search_tool = SerperDevTool()

# --- 2. AJANLARIN OLUŞTURULMASI ---

# 1. Duygu Ajanı: Kullanıcının ne hissettiğini anlar
duygu_ajani = Agent(
    role='Duygu Analisti',
    goal='Kullanıcının girdiği metindeki duyguyu ve gizli ihtiyacı tespit et.',
    backstory='Sen insan psikolojisinden anlayan, satır aralarını okuyan bir uzmansın. Kullanıcı sadece "sıkıldım" dese bile onun ne tür bir eğlence aradığını anlarsın.',
    verbose=True,
    allow_delegation=False,
    memory=True
)

# 2. Tema Ajanı: Duyguya uygun konsept belirler
tema_ajani = Agent(
    role='Tema Küratörü',
    goal='Analiz edilen duyguya en uygun kitap veya ürün temasını belirle.',
    backstory='Edebiyat dünyasına ve trendlere hakimsin. Hüzünlü birine neşeli bir kitap mı yoksa hüznüne eşlik edecek bir kitap mı gerektiğini bilirsin.',
    verbose=True,
    allow_delegation=False,
    memory=True
)

# 3. Öneri Ajanı (Fiyat ve Yorum Özelliği Burada): Ürünü bulur, fiyat karşılaştırır
oneri_ajani = Agent(
    role='Alışveriş ve Kitap Danışmanı',
    goal='Belirlenen temaya uygun en iyi 2 kitabı bul. Bunların güncel fiyatlarını (D&R, Amazon, Kitapyurdu) ve gerçek kullanıcı yorumlarını araştır.',
    backstory='Sen internetin altını üstüne getiren bir araştırmacısın. Asla hayali fiyat uydurmazsın, mutlaka internetten kontrol edersin.',
    verbose=True,
    tools=[search_tool], # Bu ajana internet yetkisi verdik!
    allow_delegation=False,
    memory=True
)

# 4. Alıntı Ajanı: Üründen bir söz çeker
alinti_ajani = Agent(
    role='Edebiyat Araştırmacısı',
    goal='Önerilen kitapların yazarından veya kitabın içinden can alıcı bir alıntı bul.',
    backstory='Geniş bir alıntı veritabanına ve edebi hafızaya sahipsin.',
    verbose=True,
    tools=[search_tool], # Alıntı bulmak için internete bakabilir
    allow_delegation=False,
    memory=True
)

# 5. Editör Ajanı: Hepsini toparlar
editor_ajani = Agent(
    role='Baş Editör',
    goal='Tüm ajanlardan gelen verileri (Duygu, Tema, Ürünler, Fiyatlar, Yorumlar, Alıntılar) birleştirip kullanıcıya mükemmel bir blog yazısı formatında sun.',
    backstory='Karmaşık verileri okuması zevkli, akıcı ve düzenli metinlere dönüştüren usta bir yazarsın. Türkçe dil bilgisi kurallarına çok dikkat edersin.',
    verbose=True,
    allow_delegation=False,
    memory=True
)

# --- 3. GÖREVLERİN (TASKS) TANIMLANMASI ---

print("Lütfen ruh halinizi veya ne aradığınızı yazın (Örn: Çok yorgunum, beni uzaklara götürecek bir macera istiyorum):")
user_input = input("Girişiniz: ")

task1_analiz = Task(
    description=f'Kullanıcı girdisini analiz et: "{user_input}". Kullanıcının ruh halini belirle.',
    expected_output='Kullanıcının duygu durumu (Örn: Melankolik, Maceracı vb.)',
    agent=duygu_ajani
)

task2_tema = Task(
    description='Duygu analizine dayanarak spesifik bir kitap/ürün teması belirle.',
    expected_output='Önerilecek tema başlığı (Örn: Distopik Bilim Kurgu Klasikleri).',
    agent=tema_ajani,
    context=[task1_analiz] # Bir önceki görevin sonucunu kullanır
)

task3_arastirma = Task(
    description='''
    Belirlenen temaya uygun, piyasada bulunan popüler 2 adet kitap öner.
    ÖNEMLİ:
    1. Her kitap için internette arama yap.
    2. Kitabın Amazon TR, D&R veya BKM Kitap fiyatlarını bul ve karşılaştır.
    3. Kitap hakkında yapılmış "gerçek" kullanıcı yorumlarından 1-2 cümlelik özet çıkar.
    ''',
    expected_output='Kitap Adı, Yazar, Fiyat Karşılaştırması ve Kullanıcı Yorum Özeti içeren liste.',
    agent=oneri_ajani,
    context=[task2_tema]
)

task4_alinti = Task(
    description='Önerilen bu kitaplardan veya yazarlarından etkileyici birer alıntı bul.',
    expected_output='Her kitap için bir alıntı sözü.',
    agent=alinti_ajani,
    context=[task3_arastirma]
)

task5_rapor = Task(
    description='Tüm bilgileri birleştir. Başlık, Giriş (Duygu analizi), Öneriler (Fiyat ve Yorum detaylarıyla), Alıntılar ve Sonuç bölümü olan şık bir Türkçe rapor yaz.',
    expected_output='Markdown formatında nihai blog yazısı.',
    agent=editor_ajani,
    context=[task1_analiz, task2_tema, task3_arastirma, task4_alinti]
)

# --- 4. EKİBİN ÇALIŞTIRILMASI ---

my_crew = Crew(
    agents=[duygu_ajani, tema_ajani, oneri_ajani, alinti_ajani, editor_ajani],
    tasks=[task1_analiz, task2_tema, task3_arastirma, task4_alinti, task5_rapor],
    process=Process.sequential # Ajanlar sırayla çalışsın
)

print("\n\n################ Ajanlar Çalışmaya Başlıyor ################\n")
result = my_crew.kickoff()

print("\n\n################ SONUÇ RAPORU ################\n")

print(result)
