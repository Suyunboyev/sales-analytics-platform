"""
Data Cleaner Module
Avtomatik EDA va ma'lumotlarni tozalash
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple
from sklearn.preprocessing import LabelEncoder

class DataCleaner:
    """Ma'lumotlarni avtomatik tozalash va tahlil qilish"""
    
    def __init__(self, lang: str = "uz"):
        self.lang = lang
        self.messages = {
            "uz": {
                "cleaning_title": "🧹 Ma'lumotlarni Tozalash",
                "cleaning_progress": "Tozalash jarayoni...",
                "data_quality": "Ma'lumot Sifati",
                "missing_values": "Yetishmayotgan qiymatlar",
                "duplicates": "Dublikatlar",
                "outliers": "Outlier lar",
                "dtypes_optimization": "Ma'lumot Turlarini Optimallashtirish",
                "before": "Oldin",
                "after": "Keyin",
                "memory_saved": "Tejangan xotira",
                "cleaned_success": "✅ Ma'lumotlar muvaffaqiyatli tozalandi!",
                "no_issues": "✅ Ma'lumotlarda muammolar topilmadi"
            },
            "en": {
                "cleaning_title": "🧹 Data Cleaning",
                "cleaning_progress": "Cleaning in progress...",
                "data_quality": "Data Quality",
                "missing_values": "Missing Values",
                "duplicates": "Duplicates",
                "outliers": "Outliers",
                "dtypes_optimization": "Data Types Optimization",
                "before": "Before",
                "after": "After",
                "memory_saved": "Memory Saved",
                "cleaned_success": "✅ Data cleaned successfully!",
                "no_issues": "✅ No issues found in data"
            }
        }
        self.cleaning_report = {}
    
    def get_message(self, key: str) -> str:
        """Til bo'yicha xabarni olish"""
        return self.messages[self.lang].get(key, key)
    
    def analyze_data_quality(self, df: pd.DataFrame) -> Dict:
        """Ma'lumot sifatini tahlil qilish"""
        quality_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': {},
            'duplicates': 0,
            'memory_usage': df.memory_usage(deep=True).sum()
        }
        
        # Yetishmayotgan qiymatlar
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                quality_report['missing_values'][col] = {
                    'count': null_count,
                    'percentage': round(null_count / len(df) * 100, 2)
                }
        
        # Dublikatlar
        quality_report['duplicates'] = df.duplicated().sum()
        
        return quality_report
    
    def detect_column_types(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Ustun turlarini avtomatik aniqlash"""
        column_types = {
            'numeric': [],
            'categorical': [],
            'datetime': [],
            'text': []
        }
        
        for col in df.columns:
            # Datetime ustunlarini aniqlash
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col], errors='raise')
                    column_types['datetime'].append(col)
                    continue
                except (ValueError, TypeError):
                    pass
            
            # Numeric ustunlar
            if pd.api.types.is_numeric_dtype(df[col]):
                column_types['numeric'].append(col)
            
            # Categorical ustunlar (kam unique qiymatlar)
            elif df[col].dtype == 'object':
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.05 or df[col].nunique() < 20:
                    column_types['categorical'].append(col)
                else:
                    column_types['text'].append(col)
        
        return column_types
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Yetishmayotgan qiymatlar bilan ishlash"""
        df_cleaned = df.copy()
        
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().sum() > 0:
                # Numeric ustunlar uchun - median
                if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                    df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
                
                # Categorical ustunlar uchun - mode
                elif df_cleaned[col].dtype == 'object':
                    if df_cleaned[col].mode().size > 0:
                        df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)
                    else:
                        df_cleaned[col].fillna('Unknown', inplace=True)
        
        return df_cleaned
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Dublikatlarni olib tashlash"""
        return df.drop_duplicates()
    
    def detect_outliers(self, df: pd.DataFrame, column: str) -> pd.Series:
        """IQR usuli bilan outlierlarni aniqlash"""
        if not pd.api.types.is_numeric_dtype(df[column]):
            return pd.Series([False] * len(df))
        
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        return (df[column] < lower_bound) | (df[column] > upper_bound)
    
    def optimize_dtypes(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Ma'lumot turlarini optimallashtirish (xotirani tejash)"""
        df_optimized = df.copy()
        memory_before = df.memory_usage(deep=True).sum()
        optimization_report = {}
        
        for col in df_optimized.columns:
            col_type = df_optimized[col].dtype
            
            # Integer optimallashtirish
            if col_type == 'int64':
                c_min = df_optimized[col].min()
                c_max = df_optimized[col].max()
                
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df_optimized[col] = df_optimized[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df_optimized[col] = df_optimized[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df_optimized[col] = df_optimized[col].astype(np.int32)
            
            # Float optimallashtirish
            elif col_type == 'float64':
                df_optimized[col] = df_optimized[col].astype(np.float32)
            
            # Object -> Category (agar unique values kam bo'lsa)
            elif col_type == 'object':
                num_unique = df_optimized[col].nunique()
                num_total = len(df_optimized[col])
                if num_unique / num_total < 0.5:
                    df_optimized[col] = df_optimized[col].astype('category')
        
        memory_after = df_optimized.memory_usage(deep=True).sum()
        memory_saved = memory_before - memory_after
        
        optimization_report = {
            'memory_before': memory_before,
            'memory_after': memory_after,
            'memory_saved': memory_saved,
            'saved_percentage': round(memory_saved / memory_before * 100, 2)
        }
        
        return df_optimized, optimization_report
    
    def auto_clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Avtomatik to'liq tozalash jarayoni
        
        Returns:
            (tozalangan_df, hisobot)
        """
        with st.spinner(self.get_message("cleaning_progress")):
            # 1. Data quality tahlili
            quality_report = self.analyze_data_quality(df)
            
            # 2. Yetishmayotgan qiymatlar
            df_cleaned = self.handle_missing_values(df)
            
            # 3. Dublikatlar
            duplicates_removed = len(df_cleaned) - len(df_cleaned.drop_duplicates())
            df_cleaned = self.remove_duplicates(df_cleaned)
            
            # 4. Data types optimallashtirish
            df_cleaned, optimization_report = self.optimize_dtypes(df_cleaned)
            
            # 5. Column types aniqlash
            column_types = self.detect_column_types(df_cleaned)
            
            # Hisobot
            cleaning_report = {
                'quality': quality_report,
                'duplicates_removed': duplicates_removed,
                'optimization': optimization_report,
                'column_types': column_types,
                'final_shape': df_cleaned.shape
            }
            
            self.cleaning_report = cleaning_report
            
        return df_cleaned, cleaning_report
    
    def display_cleaning_report(self, report: Dict):
        """Tozalash hisobotini ko'rsatish"""
        st.subheader(self.get_message("data_quality"))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            missing_count = sum([v['count'] for v in report['quality']['missing_values'].values()])
            st.metric(
                self.get_message("missing_values"),
                missing_count,
                delta=f"-{missing_count}" if missing_count > 0 else "0",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                self.get_message("duplicates"),
                report['duplicates_removed'],
                delta=f"-{report['duplicates_removed']}" if report['duplicates_removed'] > 0 else "0",
                delta_color="normal"
            )
        
        with col3:
            memory_saved_mb = report['optimization']['memory_saved'] / (1024 * 1024)
            st.metric(
                self.get_message("memory_saved"),
                f"{memory_saved_mb:.2f} MB",
                delta=f"-{report['optimization']['saved_percentage']:.1f}%",
                delta_color="normal"
            )
        
        if missing_count == 0 and report['duplicates_removed'] == 0:
            st.success(self.get_message("no_issues"))
        else:
            st.success(self.get_message("cleaned_success"))