import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.cluster import KMeans

st.header("📈 Visual Insights")

if 'df' in st.session_state:
    df = st.session_state.df
    crop_cols = ['Porumb boabe', 'Cartofi - total', 'Floarea soarelui', 'Soia boabe']
    
    try:
        romania_map = gpd.read_file('romania.geojson')
        geojson_available = True
    except:
        geojson_available = False

    tab_summer, tab_spring = st.tabs(["☀️ Summer Analysis", "🌱 Spring Analysis"])

    # =========================================================================
    # TAB 1: SUMMER
    # =========================================================================
    with tab_summer:
        st.subheader("Summer Climate vs. Yields")

        if geojson_available:
            st.write("### 1. Regional Yield Distribution (Summer Context)")
            map_cols = st.columns(2)
            for i, crop in enumerate(crop_cols):
                with map_cols[i % 2]:
                    avg_yield = df.groupby('County')[crop].mean().reset_index()
                    merged = romania_map.merge(avg_yield, left_on='name', right_on='County')
                    fig, ax = plt.subplots(figsize=(6, 4))
                    merged.plot(column=crop, ax=ax, legend=True, cmap='YlGn', edgecolor='0.5')
                    ax.set_title(f"Yield Distribution: {crop}")
                    ax.axis('off')
                    st.pyplot(fig)
            
            st.success("""**Economic interpretation of results:** The maps highlight a clear "Productivity Corridor". For our expansion, this is a green light for Infrastructure Investment. Instead of scattered farms, we should focus on these high-yield "dark zones" to build collection centers. This geographic focus reduces transport costs and creates an "Economy of Scale," where multiple farms in a small area can share resources and logistics, significantly increasing the overall profit margin.""")
        
        st.divider()

        st.write("### 2. Summer Precipitation Anomalies")
        Q1_sum = df['precipitation_sum'].quantile(0.25)
        Q3_sum = df['precipitation_sum'].quantile(0.75)
        IQR_sum = Q3_sum - Q1_sum
        low_sum, up_sum = Q1_sum - 1.5 * IQR_sum, Q3_sum + 1.5 * IQR_sum
        
        col_out1, col_out2 = st.columns(2)
        with col_out1:
            fig, ax = plt.subplots()
            sns.boxplot(x=df['precipitation_sum'], color='skyblue', ax=ax)
            st.pyplot(fig)
        with col_out2:
            df_f_sum = df[(df['precipitation_sum'] >= low_sum) & (df['precipitation_sum'] <= up_sum)]
            fig, ax = plt.subplots()
            sns.boxplot(x=df_f_sum['precipitation_sum'], color='blue', ax=ax)
            st.pyplot(fig)
        
        st.info("""**Economic interpretation of results**

Summer Precipitation Analysis: The initial distribution (light blue) revealed 1 climatic outlier—extreme rainfall events that could skew our statistical results. By applying the IQR method (blue), we removed the anomality to ensure our expansion strategy is based on consistent weather trends rather than non-representative, extreme flooding events.""")

        st.divider()

        st.write("### 3. K-Means Segmentation (Summer)")
        cl_cols = st.columns(2)
        for i, crop in enumerate(crop_cols):
            with cl_cols[i % 2]:
                X = df[['precipitation_sum', 'maxtemp_sum', crop]].dropna()
                km = KMeans(n_clusters=3, random_state=42, n_init=10)
                X['Cluster'] = km.fit_predict(X)
                fig, ax = plt.subplots()
                sns.scatterplot(data=X, x='precipitation_sum', y=crop, hue='Cluster', palette='viridis', ax=ax)
                ax.set_title(f"Clusters: {crop}")
                st.pyplot(fig)
        
        st.warning("""**Economic interpretation of results for summer**

1. Corn (Porumb boabe)
Cluster 1 (teal) shows that moderate precipitation levels are associated with the highest yields. In contrast, Cluster 2 (yellow) represents counties with high summer rainfall that often results in lower-than-average corn production.

2. Potatoes (Cartofi - total)
The majority of high-yielding counties are grouped in Cluster 0 (purple), which favors lower precipitation levels. Cluster 2 (yellow) highlights a clear trend where excessive summer rain negatively impacts potato yields.

3. Sunflower (Floarea soarelui)
Cluster 1 (teal) identifies the "sweet spot" for sunflowers, where moderate rainfall leads to peak performance. Cluster 0 (purple) shows that high precipitation does not translate to better yields for this crop, often leading to average or poor results.

4. Soybeans (Soia boabe)
Similar to sunflowers, soybeans perform best in Cluster 1 (teal) under balanced rainfall conditions. Cluster 0 (purple) indicates that counties with the highest summer precipitation actually see a decline in soybean productivity.""")

        st.divider()

        st.write("### 4. Summer Weather Impact: Correlation Matrix")
        summer_weather = ['radiation_sum', 'meantemp_sum', 'maxtemp_sum', 'precipitation_sum', 'humidity_sum', 'windspeed_sum']
        summer_corr = df[summer_weather + crop_cols].corr()
        subset_summer = summer_corr.loc[summer_weather, crop_cols]
        
        fig_h_sum, ax_h_sum = plt.subplots(figsize=(10, 6))
        sns.heatmap(subset_summer, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax_h_sum)
        st.pyplot(fig_h_sum)

        st.info("""**Economic interpretation for Summer:** We used this heatmap to identify how weather variables impact crop yields. 

*Here is what the colours tell us:*

**Sun and Heat (+):** Shown in red. This means that, in general, high temperatures and solar radiation help increase production.

**Rain and Humidity (-):** Shown in blue. In this dataset, excess water appears to harm crops (possibly due to disease or rot).

**In our case, there is a low impact (values below 0.20):** All of these correlations are very weak. This tells us that summer weather matters, but it’s not the only factor. Soil quality, fertilizers, and pests likely have a much greater impact on the final harvest.""")

    # =========================================================================
    # TAB 2: SPRING
    # =========================================================================
    with tab_spring:
        st.subheader("Spring Climate vs. Yields")

        if geojson_available:
            st.write("### 1. Regional Yield Distribution (Spring Context)")
            map_cols_sp = st.columns(2)
            for i, crop in enumerate(crop_cols):
                with map_cols_sp[i % 2]:
                    avg_yield = df.groupby('County')[crop].mean().reset_index()
                    merged = romania_map.merge(avg_yield, left_on='name', right_on='County')
                    fig, ax = plt.subplots(figsize=(6, 4))
                    merged.plot(column=crop, ax=ax, legend=True, cmap='BuGn', edgecolor='0.5')
                    ax.set_title(f"Yield Distribution: {crop}")
                    ax.axis('off')
                    st.pyplot(fig)
            st.success("""We visualized the corn yield across Romania using geopandas.
High-Yield Regions: The darker green areas represent the most productive counties. These are the primary targets for our organization's expansion.
Low-Yield Regions: The lighter areas indicate regions where the weather conditions or soil types analyzed earlier result in lower average yields.
Strategic Insight: This maps confirm that geographic location is a major factor in agricultural success, allowing us to focus our resources on high-performance clusters.""")

        st.divider()

        st.write("### 2. Spring Precipitation Anomalies")
        Q1_spr = df['precipitation_spr'].quantile(0.25)
        Q3_spr = df['precipitation_spr'].quantile(0.75)
        IQR_spr = Q3_spr - Q1_spr
        low_spr, up_spr = Q1_spr - 1.5 * IQR_spr, Q3_spr + 1.5 * IQR_spr

        col_out3, col_out4 = st.columns(2)
        with col_out3:
            fig, ax = plt.subplots()
            sns.boxplot(x=df['precipitation_spr'], color='lightpink', ax=ax)
            st.pyplot(fig)
        with col_out4:
            df_f_spr = df[(df['precipitation_spr'] >= low_spr) & (df['precipitation_spr'] <= up_spr)]
            fig, ax = plt.subplots()
            sns.boxplot(x=df_f_spr['precipitation_spr'], color='red', ax=ax)
            st.pyplot(fig)
        
        st.info("""**Spring Precipitation Analysis:** The initial distribution (light pink) identified several climatic outliers—extreme rainfall events that could skew our statistical results and misrepresent the typical planting season. By applying the IQR (Interquartile Range) method (red), we isolated these anomalies to ensure our agricultural strategy is based on consistent weather trends rather than rare, non-representative flooding events that could distort our yield predictions.""")

        st.divider()

        st.write("### 3. K-Means Segmentation (Spring)")
        cl_cols_sp = st.columns(2)
        for i, crop in enumerate(crop_cols):
            with cl_cols_sp[i % 2]:
                X_sp = df[['precipitation_spr', 'maxtemp_spr', crop]].dropna()
                km_sp = KMeans(n_clusters=3, random_state=42, n_init=10)
                X_sp['Cluster'] = km_sp.fit_predict(X_sp)
                fig, ax = plt.subplots()
                sns.scatterplot(data=X_sp, x='precipitation_spr', y=crop, hue='Cluster', palette='magma', ax=ax)
                ax.set_title(f"Spring Clusters: {crop}")
                st.pyplot(fig)
        
        st.warning("""**Economic interpretation of results for spring**

1. Corn (Porumb boabe) Cluster 1 (pink) clearly represents the highest-performing counties, showing that corn yield is less sensitive to spring precipitation and more dependent on other cluster-specific factors. Clusters 0 (black) and 2 (yellow) mostly contain counties with average to below-average yields regardless of rainfall.

2. Potatoes (Cartofi - total) Cluster 0 (black) identifies the top-performing counties, which tend to favor lower spring precipitation for better yields. Conversely, Cluster 1 (pink) shows that high precipitation in spring often correlates with lower potato productivity.

3. Sunflower (Floarea soarelui) Similar to corn, Cluster 1 (pink) groups the most productive counties, which maintain high yields across a wide range of spring rainfall. Clusters 0 and 2 show a dense concentration of average yields, suggesting these counties are less optimized for sunflower production.

4. Soybean (Soia boabe) The highest yields are found in Cluster 1 (pink), particularly in counties with low to moderate spring precipitation. Cluster 2 (yellow) highlights a group of counties where higher spring rainfall does not lead to significant yield improvements, staying mostly below average.""")

        st.divider()

        st.write("### 4. Spring Weather Impact: Correlation Matrix")
        spring_weather = ['radiation_spr', 'meantemp_spr', 'maxtemp_spr', 'precipitation_spr', 'humidity_spr', 'windspeed_spr']
        spring_corr = df[spring_weather + crop_cols].corr()
        subset_spring = spring_corr.loc[spring_weather, crop_cols]
        
        fig_h_spr, ax_h_spr = plt.subplots(figsize=(10, 6))
        sns.heatmap(subset_spring, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax_h_spr)
        st.pyplot(fig_h_spr)

        st.info("""**Economic interpretation for Spring:** We used this heatmap to identify how weather variables impact crop yields. 

*Here is what the colours tell us:*

**Green (Positive Correlation):** Higher values in these weather factors tend to increase crop yields. In spring, precipitation shows a general positive trend for most crops (except potatoes), meaning early-season rain is beneficial for growth.

**Purple (Negative Correlation):** Higher values here tend to decrease yields. Humidity is consistently purple across all crops, suggesting that excessive dampness in spring might lead to mold or soil issues that hinder development.

**The "Potato" Exception:** Unlike other crops, potatoes show a positive link with solar radiation (0.10) but a negative link with spring rain. This suggests potatoes prefer a drier, sunnier spring to establish themselves.

**Weak Impact (Values < 0.15):** Just like in summer, these correlations are statistically weak. This implies that while spring weather matters, the final yield is much more dependent on other factors like soil preparation, fertilization, and pest control.""")

else:
    st.error("No data found. Go to Home.")