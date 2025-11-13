# 📊 Data Analytics Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

Interaktiv ma'lumotlar tahlili va vizualizatsiya platformasi - CSV va Excel fayllar uchun avtomatik EDA va tozalash

## 🌐 Live Demo

**[🚀 Platformani Ochish](https://your-app-url.streamlit.app)**

> **Eslatma**: Deploy qilgandan keyin yuqoridagi URL ni o'zingiznikiga almashtiring

## 🎯 Xususiyatlar

### ✅ Asosiy Funksiyalar
- **File Upload**: CSV va XLSX formatlarini qo'llab-quvvatlash (maksimal 50 MB)
- **Avtomatik EDA**: 
  - Yetishmayotgan qiymatlarni aniqlash va to'ldirish
  - Dublikatlarni olib tashlash
  - Data type larni optimallashtirish
  - Outlier detection
- **Statistik Tahlil**:
  - Descriptive statistics
  - Correlation analysis
  - Distribution analysis
  - Automated insights generation
- **Interaktiv Vizualizatsiyalar**:
  - Histogram, Box Plot, Scatter Plot
  - Correlation Heatmap
  - Time Series Analysis
  - Bar Charts va Pie Charts
- **Eksport**: Tozalangan ma'lumotlarni CSV yoki Excel formatda saqlash
- **Multi-language**: O'zbek va Ingliz tillarini qo'llab-quvvatlash

## 📁 Loyiha Strukturasi

```
sales-analytics-platform/
├── app.py                 # Asosiy Streamlit ilovasi
├── requirements.txt       # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── data_loader.py    # File yuklash moduli
│   ├── data_cleaner.py   # EDA va tozalash moduli
│   ├── analyzer.py       # Statistik tahlil moduli
│   └── visualizer.py     # Vizualizatsiya moduli
└── README.md
```

## 🚀 O'rnatish va Ishga Tushirish

### 1. Repository ni clone qilish
```bash
git clone <repository-url>
cd sales-analytics-platform
```

### 2. Virtual environment yaratish
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Dependencies ni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Ilovani ishga tushirish
```bash
streamlit run app.py
```

Brauzer avtomatik ochiladi va ilova `http://localhost:8501` da ochiladi.

## 📖 Foydalanish Qo'llanmasi

### 1. Ma'lumot Yuklash
- "Ma'lumot Yuklash" bo'limiga o'ting
- CSV yoki XLSX faylni tanlang (maksimal 50 MB)
- Fayl avtomatik yuklandi va preview ko'rsatiladi

### 2. Tozalash va EDA
- "Tozalash va EDA" bo'limiga o'ting
- "Avtomatik Tozalash va Tahlil Boshlash" tugmasini bosing
- Platforma quyidagilarni avtomatik bajaradi:
  - NaN qiymatlarni to'ldirish (numeric uchun median, categorical uchun mode)
  - Dublikatlarni olib tashlash
  - Data type larni optimallashtirish
  - Statistik tahlil va insights generatsiya

### 3. Vizualizatsiya
- "Vizualizatsiya" bo'limiga o'ting
- Avtomatik yaratilgan grafiklarni ko'ring
- Yoki maxsus vizualizatsiya yarating:
  - Vizualizatsiya turini tanlang
  - Kerakli ustunlarni tanlang
  - "Yaratish" tugmasini bosing

### 4. Eksport
- "Eksport" bo'limiga o'ting
- Format tanlang (CSV yoki Excel)
- Tozalangan ma'lumotlarni yuklab oling

## 🛠️ Texnologiyalar

- **Frontend/Backend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Statistics**: SciPy, Scikit-learn
- **File Handling**: OpenPyXL

## 📊 Qo'llab-quvvatlanadigan Vizualizatsiyalar

1. **Histogram** - Numeric ma'lumotlar taqsimoti
2. **Box Plot** - Outlierlarni aniqlash
3. **Scatter Plot** - Ikki o'zgaruvchi orasidagi bog'lanish
4. **Line Chart** - Vaqt seriyasi tahlili
5. **Bar Chart** - Kategorik ma'lumotlar
6. **Pie Chart** - Ulush ko'rinishi
7. **Correlation Heatmap** - O'zgaruvchilar orasidagi korrelyatsiya
8. **Violin Plot** - Taqsimot va outlierlar birgalikda

## 🌐 Til Qo'llab-quvvatlash

Platforma 2 ta tilni qo'llab-quvvatlaydi:
- 🇺🇿 O'zbek
- 🇬🇧 English

Tilni sidebar dan o'zgartirish mumkin.

## 🔧 Konfiguratsiya

### Fayl Hajmi Limiti
Default: 50 MB

O'zgartirish uchun `data_loader.py` da:
```python
max_size = 50 * 1024 * 1024  # bytes
```

### Vizualizatsiya Ranglari
Plotly default color scheme ishlatiladi. O'zgartirish uchun `visualizer.py` da color parametrlarini tahrirlang.

## 📝 To-Do / Kelajakdagi Yangilanishlar

- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] Advanced ML insights (clustering, classification)
- [ ] Real-time data streaming
- [ ] User authentication
- [ ] Export to PDF report
- [ ] More statistical tests
- [ ] Custom color themes

## 🤝 Hissa Qo'shish

Pull request lar qabul qilinadi! Katta o'zgarishlar uchun avval issue oching.

## 📄 License

MIT License

## 👥 Muallif

Your Team - Data Analytics Platform

## 📞 Aloqa

Savollar yoki takliflar bo'lsa:
- Email: your.email@example.com
- GitHub: @yourusername

---

**Eslatma**: Bu platforma educational maqsadlarda yaratilgan. Production muhitda ishlatishdan oldin qo'shimcha xavfsizlik va optimizatsiya choralari ko'ring.
