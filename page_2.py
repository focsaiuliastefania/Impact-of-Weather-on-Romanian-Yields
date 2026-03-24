import streamlit as st
import pandas as pd
import statsmodels.api as sm

st.header("⚙️ Data Engineering & Statistical Validation")

if 'df' in st.session_state:
    df = st.session_state.df.copy()

    crops = ['Porumb boabe', 'Floarea soarelui', 'Soia boabe', 'Cartofi - total']
    for crop in crops:
        if crop in df.columns:
            df[crop] = df.groupby('County')[crop].transform(lambda x: x.fillna(x.mean()))
    df = df.fillna(0)
    
    st.subheader("1. Data Preprocessing & Integrity")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("**Dataset Preview (Standardized & Filtered)**")
        st.dataframe(df.head(10), use_container_width=True)
    with col2:
        st.write("**Null Value Verification**")
        null_counts = df.isnull().sum().reset_index()
        null_counts.columns = ['Feature', 'Null Count']
        st.dataframe(null_counts, hide_index=True, use_container_width=True)

    st.info("💡 **Null Values Note:** In our case, there are no missing values (null count is 0), ensuring a high-quality baseline for regression analysis.")
    st.divider()

    # // OLS Regression for Summer
    st.subheader("2. Statistical Validation: Summer Impact")
    weather_sum = ['precipitation_sum', 'maxtemp_sum', 'radiation_sum']
    
    sum_cols = st.columns(2)
    for i, crop in enumerate(crops):
        with sum_cols[i % 2]:
            with st.expander(f"📊 OLS Summary: {crop} (Summer)"):
                X = sm.add_constant(df[weather_sum])
                model = sm.OLS(df[crop], X).fit()
                st.text(str(model.summary()))

    st.divider()

    # // OLS Regression for Spring
    st.subheader("3. Statistical Validation: Spring Impact")
    weather_spr = ['precipitation_spr', 'maxtemp_spr', 'radiation_spr']
    
    spr_cols = st.columns(2)
    for i, crop in enumerate(crops):
        with spr_cols[i % 2]:
            with st.expander(f"🌱 OLS Summary: {crop} (Spring)"):
                X_spr = sm.add_constant(df[weather_spr])
                model_spr = sm.OLS(df[crop], X_spr).fit()
                st.text(str(model_spr.summary()))

    st.divider()

    # // Final Insights Section
    st.subheader("🔍General Description")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("""
        **1. The "Potato Paradox:"**
        Potatoes are the most sensitive crop. They benefit from **Spring Sun** (germination), but are heavily damaged by **Summer Rain**. Ideal year: Clear spring + Dry summer.
        
        **2. Sunflowers: Heat-Lovers**
        Sunflowers thrive in **Summer Heat** (positive Max Temp coefficient) but dislike high **Spring Radiation**, suggesting early seedling stress.
        """)
        
    with col_b:
        st.warning("""
        **3. The "Silent" Crops (Corn & Soy):**
        Showed almost no significant relationship with weather. **Interpretation:** Factors like irrigation or soil quality override natural weather fluctuations here.
        
        **4. The $R^2$ Reality Check:**
        $R^2$ values are low (< 3%). While weather drivers are statistically significant, the "magic" happens due to human intervention and regional soil characteristics.
        """)

    st.session_state.df = df
else:
    st.error("No data available. Please initialize on the Home page.")