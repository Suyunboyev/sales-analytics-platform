"""
Sales Analytics Platform
Interaktiv ma'lumotlar tahlili va vizualizatsiya platformasi
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Utils modullarini import qilish
try:
    from utils.data_loader import DataLoader
    from utils.data_cleaner import DataCleaner
    from utils.analyzer import DataAnalyzer
    from utils.visualizer import DataVisualizer
except ImportError as e:
    st.error(f"❌ Modullarni import qilishda xatolik: {e}")
    st.info("📁 Iltimos, `utils` papkasi va barcha fayllar to'g'ri joyda ekanligini tekshiring")
    st.stop()

# Page config
st.set_page_config(
    page_title="Data Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'df_original' not in st.session_state:
    st.session_state.df_original = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'cleaning_report' not in st.session_state:
    st.session_state.cleaning_report = None
if 'language' not in st.session_state:
    st.session_state.language = 'uz'

def main():
    """Asosiy funksiya"""
    
    # Sidebar - Language selector va navigation
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/bar-chart.png", width=80)
        
        # Til tanlash
        lang_options = {
            "🇺🇿 O'zbek": "uz",
            "🇬🇧 English": "en"
        }
        selected_lang = st.selectbox(
            "🌐 Til / Language",
            options=list(lang_options.keys()),
            index=0 if st.session_state.language == 'uz' else 1
        )
        st.session_state.language = lang_options[selected_lang]
        
        st.divider()
        
        # Navigation
        if st.session_state.language == 'uz':
            st.markdown("### 📋 Navigatsiya")
            page = st.radio(
                "Bo'limni tanlang:",
                ["📤 Ma'lumot Yuklash", "🧹 Tozalash va EDA", "📊 Vizualizatsiya", "💾 Eksport"]
            )
        else:
            st.markdown("### 📋 Navigation")
            page = st.radio(
                "Select Section:",
                ["📤 Data Upload", "🧹 Cleaning & EDA", "📊 Visualization", "💾 Export"]
            )
        
        st.divider()
        
        # Info
        st.markdown("---")
        st.markdown("**Developed by:** Suyunboyev Olim, Xaydarova Gularo")
        st.markdown("**Version:** 1.0.0")
    
    # Header
    if st.session_state.language == 'uz':
        st.markdown('<div class="main-header">📊 Ma\'lumotlar Tahlili Platformasi</div>', 
                   unsafe_allow_html=True)
        st.markdown("*CSV va XLSX fayllarni yuklang va avtomatik tahlil qiling*")
    else:
        st.markdown('<div class="main-header">📊 Data Analytics Platform</div>', 
                   unsafe_allow_html=True)
        st.markdown("*Upload CSV or XLSX files and analyze automatically*")
    
    st.divider()
    
    # Modullarni yaratish
    loader = DataLoader(lang=st.session_state.language)
    cleaner = DataCleaner(lang=st.session_state.language)
    analyzer = DataAnalyzer(lang=st.session_state.language)
    visualizer = DataVisualizer(lang=st.session_state.language)
    
    # Page routing
    if "Ma'lumot Yuklash" in page or "Data Upload" in page:
        show_upload_page(loader)
    
    elif "Tozalash va EDA" in page or "Cleaning & EDA" in page:
        show_cleaning_page(cleaner, analyzer)
    
    elif "Vizualizatsiya" in page or "Visualization" in page:
        show_visualization_page(visualizer)
    
    elif "Eksport" in page or "Export" in page:
        show_export_page()


def show_upload_page(loader: DataLoader):
    """Ma'lumot yuklash sahifasi"""
    
    if loader.lang == 'uz':
        st.header("📤 Ma'lumot Yuklash")
        st.write("CSV yoki XLSX formatdagi faylni yuklang (maksimal 50 MB)")
    else:
        st.header("📤 Data Upload")
        st.write("Upload a CSV or XLSX file (max 50 MB)")
    
    uploaded_file = st.file_uploader(
        loader.get_message("upload_prompt"),
        type=['csv', 'xlsx', 'xls'],
        help="Faqat CSV va Excel fayllar qo'llab-quvvatlanadi"
    )
    
    if uploaded_file is not None:
        # Faylni yuklash
        df = loader.load_file(uploaded_file)
        
        if df is not None:
            st.session_state.df_original = df
            
            # Fayl ma'lumotlari
            loader.display_file_info(df, uploaded_file)
            
            st.divider()
            
            # Preview
            loader.display_preview(df)
            
            st.divider()
            
            # Column info
            if loader.lang == 'uz':
                st.subheader("📋 Ustunlar Ma'lumoti")
            else:
                st.subheader("📋 Column Information")
            
            col_info = loader.get_column_info(df)
            st.dataframe(col_info, use_container_width=True)
            
            # Next step button
            st.divider()
            if loader.lang == 'uz':
                st.success("✅ Fayl muvaffaqiyatli yuklandi! Endi 'Tozalash va EDA' bo'limiga o'ting.")
            else:
                st.success("✅ File uploaded successfully! Now go to 'Cleaning & EDA' section.")


def show_cleaning_page(cleaner: DataCleaner, analyzer: DataAnalyzer):
    """Tozalash va EDA sahifasi"""
    
    if st.session_state.df_original is None:
        st.warning("⚠️ Avval ma'lumot yuklab oling!")
        return
    
    df = st.session_state.df_original
    
    if cleaner.lang == 'uz':
        st.header("🧹 Ma'lumotlarni Tozalash va EDA")
    else:
        st.header("🧹 Data Cleaning and EDA")
    
    # Auto clean button
    if st.session_state.df_cleaned is None:
        if st.button("🚀 Avtomatik Tozalash va Tahlil Boshlash" if cleaner.lang == 'uz' 
                    else "🚀 Start Automatic Cleaning and Analysis", 
                    type="primary"):
            
            # Tozalash
            df_cleaned, report = cleaner.auto_clean(df)
            st.session_state.df_cleaned = df_cleaned
            st.session_state.cleaning_report = report
            st.rerun()
    
    # Agar tozalash bajarilgan bo'lsa
    if st.session_state.df_cleaned is not None:
        df_cleaned = st.session_state.df_cleaned
        report = st.session_state.cleaning_report
        
        # Tozalash hisoboti
        cleaner.display_cleaning_report(report)
        
        st.divider()
        
        # Statistik tahlil
        st.header(analyzer.get_message("stats_title"))
        
        tab1, tab2, tab3 = st.tabs([
            analyzer.get_message("descriptive"),
            analyzer.get_message("correlation"),
            analyzer.get_message("insights")
        ])
        
        with tab1:
            analyzer.display_statistics(df_cleaned)
        
        with tab2:
            analyzer.display_correlation(df_cleaned)
        
        with tab3:
            insights = analyzer.generate_insights(df_cleaned, report['column_types'])
            analyzer.display_insights(insights)
        
        st.divider()
        
        # Tozalangan ma'lumotlar preview
        if cleaner.lang == 'uz':
            st.subheader("✨ Tozalangan Ma'lumotlar")
        else:
            st.subheader("✨ Cleaned Data")
        
        st.dataframe(df_cleaned.head(20), use_container_width=True)


def show_visualization_page(visualizer: DataVisualizer):
    """Vizualizatsiya sahifasi"""
    
    if st.session_state.df_cleaned is None:
        st.warning("⚠️ Avval ma'lumotlarni tozalang!")
        return
    
    df = st.session_state.df_cleaned
    report = st.session_state.cleaning_report
    
    st.header(visualizer.get_message("viz_title"))
    
    # Avtomatik vizualizatsiyalar
    with st.spinner("Vizualizatsiyalar yaratilmoqda..."):
        auto_viz = visualizer.create_auto_visualizations(df, report['column_types'])
    
    if auto_viz:
        st.success(f"✅ {len(auto_viz)} ta vizualizatsiya yaratildi!")
        
        # Vizualizatsiyalarni ko'rsatish
        for viz_name, fig in auto_viz.items():
            st.plotly_chart(fig, use_container_width=True)
            st.divider()
    
    # Interaktiv vizualizatsiya yaratish
    st.header("🎨 Maxsus Vizualizatsiya Yaratish" if visualizer.lang == 'uz' 
             else "🎨 Create Custom Visualization")
    
    viz_type = st.selectbox(
        "Vizualizatsiya turini tanlang:",
        ["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Bar Chart"]
    )
    
    numeric_cols = report['column_types'].get('numeric', [])
    categorical_cols = report['column_types'].get('categorical', [])
    all_cols = df.columns.tolist()
    
    if viz_type == "Histogram" and numeric_cols:
        col = st.selectbox("Ustunni tanlang:", numeric_cols)
        bins = st.slider("Bins soni:", 10, 100, 30)
        if st.button("Yaratish"):
            fig = visualizer.plot_histogram(df, col, bins)
            visualizer.display_visualization(fig)
    
    elif viz_type == "Box Plot" and numeric_cols:
        col = st.selectbox("Ustunni tanlang:", numeric_cols)
        group_by = st.selectbox("Guruhlash (optional):", [None] + categorical_cols)
        if st.button("Yaratish"):
            fig = visualizer.plot_box(df, col, group_by)
            visualizer.display_visualization(fig)
    
    elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
        x_col = st.selectbox("X o'qi:", numeric_cols)
        y_col = st.selectbox("Y o'qi:", [c for c in numeric_cols if c != x_col])
        color_col = st.selectbox("Rang (optional):", [None] + categorical_cols)
        if st.button("Yaratish"):
            fig = visualizer.plot_scatter(df, x_col, y_col, color_col)
            visualizer.display_visualization(fig)
    
    elif viz_type == "Line Chart":
        x_col = st.selectbox("X o'qi:", all_cols)
        y_col = st.selectbox("Y o'qi:", numeric_cols)
        if st.button("Yaratish"):
            fig = visualizer.plot_line_chart(df, x_col, y_col)
            visualizer.display_visualization(fig)
    
    elif viz_type == "Bar Chart" and categorical_cols:
        col = st.selectbox("Ustunni tanlang:", categorical_cols)
        top_n = st.slider("Top N:", 5, 20, 10)
        if st.button("Yaratish"):
            fig = visualizer.plot_bar_chart(df, col, top_n)
            visualizer.display_visualization(fig)


def show_export_page():
    """Eksport sahifasi"""
    
    if st.session_state.df_cleaned is None:
        st.warning("⚠️ Avval ma'lumotlarni tozalang!")
        return
    
    df = st.session_state.df_cleaned
    lang = st.session_state.language
    
    st.header("💾 Ma'lumotlarni Eksport Qilish" if lang == 'uz' else "💾 Export Data")
    
    # Export format
    export_format = st.selectbox(
        "Format tanlang:" if lang == 'uz' else "Select Format:",
        ["CSV", "Excel (XLSX)"]
    )
    
    if export_format == "CSV":
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 CSV yuklab olish" if lang == 'uz' else "📥 Download CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
    
    else:
        # Excel uchun buffer kerak
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        
        st.download_button(
            label="📥 Excel yuklab olish" if lang == 'uz' else "📥 Download Excel",
            data=buffer.getvalue(),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.divider()
    
    # Summary report
    if lang == 'uz':
        st.subheader("📊 Xulosa Hisoboti")
    else:
        st.subheader("📊 Summary Report")
    
    report = st.session_state.cleaning_report
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Original Rows", report['quality']['total_rows'])
        st.metric("Final Rows", report['final_shape'][0])
        st.metric("Duplicates Removed", report['duplicates_removed'])
    
    with col2:
        st.metric("Columns", report['final_shape'][1])
        st.metric("Missing Values Handled", 
                 sum([v['count'] for v in report['quality']['missing_values'].values()]))
        memory_saved = report['optimization']['memory_saved'] / (1024 * 1024)
        st.metric("Memory Saved", f"{memory_saved:.2f} MB")


if __name__ == "__main__":
    main()