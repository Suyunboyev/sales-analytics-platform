"""
Visualizer Module
Plotly yordamida interaktiv vizualizatsiyalar
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import List, Dict

class DataVisualizer:
    """Interaktiv vizualizatsiyalar yaratish"""
    
    def __init__(self, lang: str = "uz"):
        self.lang = lang
        self.messages = {
            "uz": {
                "viz_title": "📈 Vizualizatsiyalar",
                "univariate": "Bir o'zgaruvchili Tahlil",
                "bivariate": "Ikki o'zgaruvchili Tahlil",
                "multivariate": "Ko'p o'zgaruvchili Tahlil",
                "select_column": "Ustunni tanlang",
                "select_x": "X o'qi",
                "select_y": "Y o'qi",
                "select_color": "Rang bo'yicha",
                "distribution": "Taqsimot",
                "boxplot": "Box Plot",
                "scatter": "Scatter Plot",
                "correlation_heatmap": "Korrelyatsiya Heatmap",
                "time_series": "Vaqt Seriyasi",
                "top_categories": "Top Kategoriyalar"
            },
            "en": {
                "viz_title": "📈 Visualizations",
                "univariate": "Univariate Analysis",
                "bivariate": "Bivariate Analysis",
                "multivariate": "Multivariate Analysis",
                "select_column": "Select Column",
                "select_x": "X Axis",
                "select_y": "Y Axis",
                "select_color": "Color By",
                "distribution": "Distribution",
                "boxplot": "Box Plot",
                "scatter": "Scatter Plot",
                "correlation_heatmap": "Correlation Heatmap",
                "time_series": "Time Series",
                "top_categories": "Top Categories"
            }
        }
    
    def get_message(self, key: str) -> str:
        """Til bo'yicha xabarni olish"""
        return self.messages[self.lang].get(key, key)
    
    def plot_histogram(self, df: pd.DataFrame, column: str, bins: int = 30) -> go.Figure:
        """Histogram - taqsimot grafigi"""
        fig = px.histogram(
            df, 
            x=column,
            nbins=bins,
            title=f"{self.get_message('distribution')}: {column}",
            labels={column: column, 'count': 'Count'},
            color_discrete_sequence=['#636EFA']
        )
        
        fig.update_layout(
            showlegend=False,
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig
    
    def plot_box(self, df: pd.DataFrame, column: str, group_by: str = None) -> go.Figure:
        """Box plot - outlierlarni ko'rish uchun"""
        if group_by:
            fig = px.box(
                df,
                x=group_by,
                y=column,
                title=f"{self.get_message('boxplot')}: {column} by {group_by}",
                color=group_by
            )
        else:
            fig = px.box(
                df,
                y=column,
                title=f"{self.get_message('boxplot')}: {column}",
                color_discrete_sequence=['#EF553B']
            )
        
        fig.update_layout(
            showlegend=False,
            template='plotly_white'
        )
        
        return fig
    
    def plot_bar_chart(self, df: pd.DataFrame, column: str, top_n: int = 10) -> go.Figure:
        """Bar chart - kategorik ma'lumotlar uchun"""
        value_counts = df[column].value_counts().head(top_n)
        
        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            title=f"{self.get_message('top_categories')}: {column} (Top {top_n})",
            labels={'x': column, 'y': 'Count'},
            color=value_counts.values,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_tickangle=-45,
            template='plotly_white'
        )
        
        return fig
    
    def plot_pie_chart(self, df: pd.DataFrame, column: str, top_n: int = 10) -> go.Figure:
        """Pie chart"""
        value_counts = df[column].value_counts().head(top_n)
        
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=f"{column} Distribution (Top {top_n})",
            hole=0.3  # Donut chart
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(template='plotly_white')
        
        return fig
    
    def plot_scatter(self, df: pd.DataFrame, x_col: str, y_col: str, 
                     color_col: str = None, size_col: str = None) -> go.Figure:
        """Scatter plot - ikki o'zgaruvchi orasidagi bog'lanish"""
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            size=size_col,
            title=f"{self.get_message('scatter')}: {x_col} vs {y_col}",
            trendline="ols",  # Regression line
            opacity=0.7
        )
        
        fig.update_layout(
            template='plotly_white',
            hovermode='closest'
        )
        
        return fig
    
    def plot_correlation_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Korrelyatsiya heatmap"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return None
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect='auto',
            title=self.get_message('correlation_heatmap'),
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1
        )
        
        fig.update_layout(template='plotly_white')
        
        return fig
    
    def plot_line_chart(self, df: pd.DataFrame, x_col: str, y_col: str, 
                        group_col: str = None) -> go.Figure:
        """Line chart - vaqt seriyasi uchun"""
        if group_col:
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                color=group_col,
                title=f"{self.get_message('time_series')}: {y_col} over {x_col}",
                markers=True
            )
        else:
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                title=f"{self.get_message('time_series')}: {y_col} over {x_col}",
                markers=True
            )
        
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    
    def plot_violin(self, df: pd.DataFrame, column: str, group_by: str = None) -> go.Figure:
        """Violin plot - taqsimot va outlierlarni birgalikda ko'rish"""
        if group_by:
            fig = px.violin(
                df,
                x=group_by,
                y=column,
                box=True,
                points='outliers',
                title=f"Violin Plot: {column} by {group_by}",
                color=group_by
            )
        else:
            fig = px.violin(
                df,
                y=column,
                box=True,
                points='outliers',
                title=f"Violin Plot: {column}"
            )
        
        fig.update_layout(
            showlegend=False,
            template='plotly_white'
        )
        
        return fig
    
    def plot_multiple_histograms(self, df: pd.DataFrame, columns: List[str]) -> go.Figure:
        """Bir nechta histogram birgalikda"""
        n_cols = len(columns)
        rows = (n_cols + 2) // 3
        cols = min(3, n_cols)
        
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=columns
        )
        
        for idx, col in enumerate(columns):
            row = idx // 3 + 1
            col_num = idx % 3 + 1
            
            fig.add_trace(
                go.Histogram(x=df[col], name=col, showlegend=False),
                row=row,
                col=col_num
            )
        
        fig.update_layout(
            height=300 * rows,
            title_text="Distribution of Numeric Variables",
            template='plotly_white'
        )
        
        return fig
    
    def create_auto_visualizations(self, df: pd.DataFrame, column_types: Dict) -> Dict[str, go.Figure]:
        """
        Avtomatik vizualizatsiyalar yaratish
        
        Returns:
            visualizatsiyalar dictionary
        """
        visualizations = {}
        
        # Numeric ustunlar uchun
        numeric_cols = column_types.get('numeric', [])
        if numeric_cols:
            # Birinchi 6 ta numeric ustun uchun histogram
            for col in numeric_cols[:6]:
                visualizations[f"hist_{col}"] = self.plot_histogram(df, col)
            
            # Korrelyatsiya heatmap
            if len(numeric_cols) >= 2:
                heatmap = self.plot_correlation_heatmap(df)
                if heatmap:
                    visualizations['correlation_heatmap'] = heatmap
        
        # Kategorik ustunlar uchun
        categorical_cols = column_types.get('categorical', [])
        for col in categorical_cols[:4]:
            if df[col].nunique() <= 20:  # Faqat kam kategoriyali ustunlar
                visualizations[f"bar_{col}"] = self.plot_bar_chart(df, col)
        
        # Datetime ustunlar bilan time series
        datetime_cols = column_types.get('datetime', [])
        if datetime_cols and numeric_cols:
            # Birinchi datetime va numeric ustunlarni olish
            visualizations['time_series'] = self.plot_line_chart(
                df, 
                datetime_cols[0], 
                numeric_cols[0]
            )
        
        return visualizations
    
    def display_visualization(self, fig: go.Figure, use_container_width: bool = True):
        """Vizualizatsiyani ko'rsatish"""
        st.plotly_chart(fig, use_container_width=use_container_width)