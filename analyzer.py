"""
Analyzer Module
Statistik tahlil va insights
"""

import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats
from typing import Dict, List, Tuple

class DataAnalyzer:
    """Statistik tahlil va insights generator"""
    
    def __init__(self, lang: str = "uz"):
        self.lang = lang
        self.messages = {
            "uz": {
                "stats_title": "📊 Statistik Tahlil",
                "descriptive": "Tavsiflovchi Statistika",
                "correlation": "Korrelyatsiya Tahlili",
                "distribution": "Taqsimot Tahlili",
                "insights": "💡 Asosiy Topilmalar",
                "high_corr": "Yuqori korrelyatsiya",
                "skewness": "Skewness (Qiyalik)",
                "kurtosis": "Kurtosis",
                "normal_dist": "Normal taqsimot",
                "outliers_detected": "Outlierlar aniqlandi"
            },
            "en": {
                "stats_title": "📊 Statistical Analysis",
                "descriptive": "Descriptive Statistics",
                "correlation": "Correlation Analysis",
                "distribution": "Distribution Analysis",
                "insights": "💡 Key Insights",
                "high_corr": "High correlation",
                "skewness": "Skewness",
                "kurtosis": "Kurtosis",
                "normal_dist": "Normal distribution",
                "outliers_detected": "Outliers detected"
            }
        }
    
    def get_message(self, key: str) -> str:
        """Til bo'yicha xabarni olish"""
        return self.messages[self.lang].get(key, key)
    
    def descriptive_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Tavsiflovchi statistika (numeric ustunlar uchun)"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return pd.DataFrame()
        
        stats_df = df[numeric_cols].describe().T
        
        # Qo'shimcha metrikalar
        stats_df['median'] = df[numeric_cols].median()
        stats_df['skewness'] = df[numeric_cols].skew()
        stats_df['kurtosis'] = df[numeric_cols].kurtosis()
        stats_df['cv'] = (df[numeric_cols].std() / df[numeric_cols].mean() * 100).round(2)  # Coefficient of Variation
        
        return stats_df
    
    def correlation_analysis(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Korrelyatsiya tahlili
        
        Returns:
            (correlation_matrix, strong_correlations)
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return pd.DataFrame(), []
        
        corr_matrix = df[numeric_cols].corr()
        
        # Kuchli korrelyatsiyalarni topish (> 0.7 yoki < -0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': round(corr_value, 3)
                    })
        
        return corr_matrix, strong_correlations
    
    def distribution_analysis(self, df: pd.DataFrame, column: str) -> Dict:
        """
        Bir ustun uchun taqsimot tahlili
        
        Returns:
            taqsimot haqida ma'lumotlar
        """
        if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
            return {}
        
        data = df[column].dropna()
        
        # Agar ma'lumot bo'sh yoki juda kam bo'lsa
        if len(data) < 3:
            return {}
        
        # Skewness va Kurtosis
        try:
            skewness = stats.skew(data)
            kurtosis = stats.kurtosis(data)
        except:
            skewness = 0
            kurtosis = 0
        
        # Normallik testi (Shapiro-Wilk)
        # Faqat 5000 dan kam sample uchun
        is_normal = False
        try:
            if len(data) < 5000 and len(data) >= 3:
                _, p_value = stats.shapiro(data)
                is_normal = p_value > 0.05
            elif len(data) >= 5000:
                # Katta datasetlar uchun Anderson-Darling
                result = stats.anderson(data)
                is_normal = result.statistic < result.critical_values[2]  # 5% level
        except:
            is_normal = False
        
        # Outlierlarni aniqlash (IQR method)
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        
        # Nolga bo'linishdan himoya
        outliers_percentage = round(len(outliers) / len(data) * 100, 2) if len(data) > 0 else 0
        
        return {
            'skewness': round(skewness, 3),
            'kurtosis': round(kurtosis, 3),
            'is_normal': is_normal,
            'outliers_count': len(outliers),
            'outliers_percentage': outliers_percentage,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR
        }
    
    def categorical_analysis(self, df: pd.DataFrame, column: str) -> Dict:
        """Kategorik ustun tahlili"""
        if column not in df.columns:
            return {}
        
        value_counts = df[column].value_counts()
        
        return {
            'unique_count': len(value_counts),
            'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
            'most_common_count': value_counts.values[0] if len(value_counts) > 0 else 0,
            'most_common_pct': round(value_counts.values[0] / len(df) * 100, 2) if len(value_counts) > 0 else 0,
            'value_counts': value_counts.to_dict()
        }
    
    def generate_insights(self, df: pd.DataFrame, column_types: Dict) -> List[str]:
        """
        Ma'lumotlardan avtomatik insights generatsiya qilish
        """
        insights = []
        
        # Numeric ustunlar tahlili
        numeric_cols = column_types.get('numeric', [])
        for col in numeric_cols[:5]:  # Faqat birinchi 5 ta
            dist_info = self.distribution_analysis(df, col)
            
            if dist_info:
                # Outlierlar haqida
                if dist_info['outliers_percentage'] > 5:
                    insights.append(
                        f"⚠️ '{col}' ustunida {dist_info['outliers_percentage']}% outlierlar mavjud"
                    )
                
                # Skewness haqida
                if abs(dist_info['skewness']) > 1:
                    direction = "o'ng" if dist_info['skewness'] > 0 else "chap"
                    insights.append(
                        f"📊 '{col}' {direction} tomonga qiyalangan (skewness: {dist_info['skewness']})"
                    )
                
                # Normal taqsimot
                if dist_info['is_normal']:
                    insights.append(f"✅ '{col}' normal taqsimotga ega")
        
        # Korrelyatsiya tahlili
        _, strong_corr = self.correlation_analysis(df)
        for corr in strong_corr[:3]:  # Faqat birinchi 3 ta
            insights.append(
                f"🔗 '{corr['var1']}' va '{corr['var2']}' o'rtasida kuchli korrelyatsiya: {corr['correlation']}"
            )
        
        # Kategorik ustunlar
        categorical_cols = column_types.get('categorical', [])
        for col in categorical_cols[:3]:
            cat_info = self.categorical_analysis(df, col)
            if cat_info and cat_info['most_common_pct'] > 50:
                insights.append(
                    f"📈 '{col}' da '{cat_info['most_common']}' eng ko'p uchraydi ({cat_info['most_common_pct']}%)"
                )
        
        return insights
    
    def display_statistics(self, df: pd.DataFrame):
        """Statistikani ko'rsatish"""
        st.subheader(self.get_message("descriptive"))
        
        stats_df = self.descriptive_statistics(df)
        if not stats_df.empty:
            st.dataframe(stats_df.round(2), use_container_width=True)
        else:
            st.info("Ma'lumotlarda numeric ustunlar topilmadi")
    
    def display_correlation(self, df: pd.DataFrame):
        """Korrelyatsiyani ko'rsatish"""
        st.subheader(self.get_message("correlation"))
        
        corr_matrix, strong_corr = self.correlation_analysis(df)
        
        if not corr_matrix.empty:
            st.dataframe(corr_matrix.round(3), use_container_width=True)
            
            if strong_corr:
                st.write(f"**{self.get_message('high_corr')}:**")
                for corr in strong_corr:
                    st.write(f"- {corr['var1']} ↔️ {corr['var2']}: **{corr['correlation']}**")
        else:
            st.info("Korrelyatsiya tahlili uchun kamida 2 ta numeric ustun kerak")
    
    def display_insights(self, insights: List[str]):
        """Insightlarni ko'rsatish"""
        st.subheader(self.get_message("insights"))
        
        if insights:
            for insight in insights:
                st.write(insight)
        else:
            st.info("Hozircha maxsus topilmalar yo'q")