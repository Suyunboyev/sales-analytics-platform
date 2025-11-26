"""
Data Loader Module
Ma'lumotlarni yuklash va validatsiya qilish
"""

import pandas as pd
import streamlit as st
from typing import Optional, Tuple

class DataLoader:
    """File yuklash va o'qish uchun class"""
    
    def __init__(self, lang: str = "uz"):
        self.lang = lang
        self.messages = {
            "uz": {
                "upload_prompt": "📁 CSV yoki XLSX faylni yuklang",
                "file_info": "Fayl ma'lumotlari",
                "rows": "Qatorlar soni",
                "cols": "Ustunlar soni",
                "size": "Fayl hajmi",
                "preview": "Ma'lumotlarning dastlabki ko'rinishi",
                "error_size": "❌ Fayl hajmi 50 MB dan oshmasligi kerak!",
                "error_read": "❌ Faylni o'qishda xatolik yuz berdi",
                "success": "✅ Fayl muvaffaqiyatli yuklandi!"
            },
            "en": {
                "upload_prompt": "📁 Upload CSV or XLSX file",
                "file_info": "File Information",
                "rows": "Number of rows",
                "cols": "Number of columns",
                "size": "File size",
                "preview": "Data Preview",
                "error_size": "❌ File size must not exceed 50 MB!",
                "error_read": "❌ Error reading file",
                "success": "✅ File uploaded successfully!"
            }
        }
    
    def get_message(self, key: str) -> str:
        """Til bo'yicha xabarni olish"""
        return self.messages[self.lang].get(key, key)
    
    def format_size(self, size_bytes: int) -> str:
        """Fayl hajmini formatlash"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def validate_file_size(self, file) -> bool:
        """Fayl hajmini tekshirish (max 50 MB)"""
        max_size = 50 * 1024 * 1024  # 50 MB in bytes
        if file.size > max_size:
            st.error(self.get_message("error_size"))
            return False
        return True
    
    def load_file(self, uploaded_file) -> Optional[pd.DataFrame]:
        """
        Faylni yuklash va DataFrame ga o'girish
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            pd.DataFrame yoki None (xatolik bo'lsa)
        """
        if uploaded_file is None:
            return None
        
        # Fayl hajmini tekshirish
        if not self.validate_file_size(uploaded_file):
            return None
        
        try:
            # Fayl kengaytmasini aniqlash
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Faylni o'qish
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            else:
                st.error("❌ Faqat CSV va XLSX formatlar qo'llab-quvvatlanadi!")
                return None
            
            st.success(self.get_message("success"))
            return df
            
        except Exception as e:
            st.error(f"{self.get_message('error_read')}: {str(e)}")
            return None
    
    def display_file_info(self, df: pd.DataFrame, file):
        """Fayl haqida ma'lumotlarni ko'rsatish"""
        st.subheader(self.get_message("file_info"))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(self.get_message("rows"), f"{len(df):,}")
        
        with col2:
            st.metric(self.get_message("cols"), len(df.columns))
        
        with col3:
            st.metric(self.get_message("size"), self.format_size(file.size))
    
    def display_preview(self, df: pd.DataFrame, n_rows: int = 10):
        """Ma'lumotlarning dastlabki qatorlarini ko'rsatish"""
        st.subheader(self.get_message("preview"))
        st.dataframe(df.head(n_rows), use_container_width=True)
    
    def get_column_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ustunlar haqida batafsil ma'lumot"""
        info_df = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.values,
            'Non-Null': df.count().values,
            'Null': df.isnull().sum().values,
            'Null %': (df.isnull().sum() / len(df) * 100).round(2).values,
            'Unique': [df[col].nunique() for col in df.columns]
        })
        return info_df