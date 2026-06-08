import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --------------------------------------------------------------
# Consistent, clean styling for a professional blog post feel
# 1. Define your blog's brand color palette
BRAND_COLORS = {
    "primary": "#E66145",     # Premium Coral / Terracotta (Great for main bars/lines)
    "secondary": "#2B5C8F",   # Deep Slate Blue (For comparison categories)
    "accent": "#F4A261",      # Muted Amber (For highlighting specific data points)
    "text_dark": "#111111",   # Editorial Title Black
    "text_muted": "#555555",  # Soft Charcoal for labels and captions
    "grid": "#EFEFEF"         # Ultra-light gray for clean gridlines
}
def apply_blog_theme(fig, title_text="Automotive Fuel Economy Predictor"):
    """
    Applies a uniform, professional, blog-ready aesthetic to any Plotly figure.
    """
    fig.update_layout(
        title={
            'text': f"<b>{title_text}</b>",
            'y': 0.95,
            'x': 0.0,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': dict(size=18, color=BRAND_COLORS["text_dark"])
        },
        template='plotly_white',
        hovermode='closest',
        margin=dict(l=50, r=30, t=70, b=50), # Breathing room around elements
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',       # Transparent background to blend into the app
        plot_bgcolor='rgba(0,0,0,0)',
    )
    # Clean up X-axis (Remove harsh lines, keep it minimalist)
    fig.update_xaxes(
        showgrid=False,
        linecolor='#CCCCCC',
        linewidth=1,
        title_font=dict(size=12, color=BRAND_COLORS["text_muted"]),
        tickfont=dict(size=11, color=BRAND_COLORS["text_muted"])
    )

    # Clean up Y-axis (Soft horizontal lines only to guide the eye)
    fig.update_yaxes(
        showgrid=True,
        gridcolor=BRAND_COLORS["grid"],
        linecolor='rgba(0,0,0,0)', # Hide solid vertical axis line
        title_font=dict(size=12, color=BRAND_COLORS["text_muted"]),
        tickfont=dict(size=11, color=BRAND_COLORS["text_muted"])
    )
    return fig
# ---------------------------------------------------------------------

# Script to provide uniform indentation and proper alignment of text
st.markdown("""
    <style>
    /* Improve blockquote styling */
    blockquote {
        border-left: 4px solid #FF4B4B !important;
        background-color: #F0F2F6;
        padding: 10px 20px;
        font-style: italic;
        border-radius: 4px;
    }
    /* Increase line spacing for comfortable blog reading */
    .stMarkdown p {
        line-height: 1.6 !important;
        font-size: 1.05rem;
    }
    /* Smooth edges for images and charts */
    img, .stPlotlyChart {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------
# Read the data
df = pd.read_csv("data/auto-mpg.csv")
# Set page title
st.markdown("## Automotive Fuel Economy Predictor")
st.caption("Published on May 17, 2026 • 5 min read")
# Premium gradient underline that fades out to the right
st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------------
def show_explore_page():
        st.write("""
    Understanding and predicting fuel efficiency is a challenge that combines science, engineering, and a
    touch of curiosity. Imagine a world where every drop of fuel is maximized, where cars glide effortlessly
    with minimal environmental impact. This project embarks on a journey to unravel the secrets behind fuel 
    efficiency, exploring how key vehicle attributes like weight, acceleration, and cylinder count shape the 
    story of every mile traveled.

    The dataset at the heart of this analysis is a treasure trove of insights, capturing the essence of what 
    makes a car efficient. Weight, for instance, acts as a silent antagonist; the heavier the car, the more 
    fuel it demands. Cylinders, too, play their part in this narrative, with higher-cylinder engines often 
    guzzling more fuel. Acceleration and horsepower add layers of complexity, influencing how energy is 
    consumed in various driving scenarios. Through the lens of EDA, we delve into these elements, uncovering 
    patterns and correlations that bring the data to life.

    This report is a collection of findings through thourgh exploratory data analysis. Each trend, each 
    relationship among vehicle attributes and fuel efficiency, paints a picture of innovation and possibility. 
    """)

        st.markdown("#### Which engine is dominating the roads? Are less number of cylinders more preferrable.")
        st.markdown(
        """
        <hr style="
            border: none;
            height: 3px;
            background-color: #2C2A9D;
            margin-top: -10px;
            margin-bottom: 25px;
            border-radius: 2px;
        ">
        """, 
        unsafe_allow_html=True
    )
        col1, col2 = st.columns(2)
        # Bar plot: Average MPG by Number of Cylinders
        with col1:
            st.write("""
            **Engine Cylinder Configuration and Market Trends in Fuel Efficiency**
                    """)
            mpg_by_cyl = df.groupby('cylinders')['mpg'].mean().reset_index()
            # Ensure consistent order
            unique_cyls = sorted(df['cylinders'].unique())
            color_palette = ["#353535", "#3c6e71", "#1985A1", "#d9d9d9", "#284b63", "#8e9aaf"]
            color_map = dict(zip(unique_cyls, color_palette))
            # Plot
            fig, ax = plt.subplots()
            bars = sns.barplot(
                x='cylinders', y='mpg', data=mpg_by_cyl,
                order=unique_cyls, ax=ax
            )
            for bar, cyl in zip(ax.patches, unique_cyls):
                bar.set_facecolor(color_map[cyl])
            ax.set_xlabel('Cylinders')
            ax.set_ylabel('Miles per galloon')
            #ax.set_title('Average MPG by number of cylinders in car')
            st.pyplot(fig)
    
        with col2:
            cyl_counts = df['cylinders'].value_counts().sort_index()
            st.write('''
                    **Market share of cars as per engine cylinder configuration**
                    ''')
            # Use the same color order as bar plot
            pie_colors = [color_map[cyl] for cyl in cyl_counts.index]
            fig1, ax1 = plt.subplots()
            ax1.pie(
                cyl_counts, autopct='%1.1f%%',colors=pie_colors
            )
            ax1.axis('equal')
            ax.set_title("Percent of cars in market with different cylinder configuration")
            st.pyplot(fig1)
        st.write("""
    The analysis of engine configurations reveals that 4-cylinder vehicles dominate the market, accounting for 51.3% of total market share.
    Their widespread popularity is largely due to their superior fuel efficiency, offering an average of 30 miles per gallon (MPG). 
    These vehicles cater to a broad range of consumers seeking cost-effective and fuel-conscious options, making them the preferred choice 
    for everyday commuting and general use.

    On the other hand, 5-cylinder engines, while also fuel-efficient, hold a minimal presence in the market, with representation below 1%.
    Vehicles equipped with 6-cylinder and 8-cylinder engines focus primarily on performance, providing higher acceleration, power, and 
    speed. However, this enhanced capability comes at the cost of fuel efficiency. Specifically, 8-cylinder vehicles rank lowest in fuel 
    economy, averaging only 15 MPG, making them the least fuel-efficient category in the market. Meanwhile, 6-cylinder cars strike a 
    balance, offering decent mileage while retaining several performance advantages of 8-cylinder models. Notably, they command 47% of 
    the market share, indicating strong consumer preference for a blend of efficiency and performance.

    Lastly, 3-cylinder vehicles exhibit fuel efficiency comparable to 6-cylinder models, yet they remain rare in the market. Their 
    limited adoption suggests niche demand rather than widespread consumer preference.  
    """)

# -------------------------------------
        cylinder_df = df.groupby('cylinders')[['horsepower','acceleration','weight','displacement']].agg('mean')
        st.markdown("##### Impact of Engine Cylinder Variation on Key Performance Metrics")
        st.dataframe(cylinder_df,
                     column_config={
                        "horsepower": st.column_config.NumberColumn("Horsepower", format="%.2f"),
                        "acceleration": st.column_config.NumberColumn("Acceleration", format="%.2f m/s²"),
                        "weight": st.column_config.NumberColumn("Weight", format="%.2f kg"),
                        "displacement": st.column_config.NumberColumn("Displacement", format="%.2f cc")
                    },
                    hide_index=True,
                    use_container_width=True
                                    )
        
        st.write("""
    Above table shows how vehicle performance parameters highlights the significant influence of engine cylinder 
    count on horsepower, acceleration, and weight.
                """)
        
        st.markdown('''
    - Horsepower Trends: Cars with 3-cylinder engines generate an average of 99.25 Bhp, while 4-cylinder vehicles show a decrease in 
    horsepower, producing 78.65 Bhp. However, with increasing cylinder count, horsepower consistently rises, indicating a 
    direct correlation between engine size and power output.
    
    - Acceleration Variations: The relationship between acceleration and cylinder count is more complex. Acceleration improves up 
    to 5-cylinder engines, reaching peak performance. However, for 6- and 8-cylinder vehicles, acceleration declines noticeably, 
    possibly due to increased vehicle weight and performance optimization toward power rather than speed responsiveness.
    
    - Impact on Vehicle Weight: As cylinder count increases, so does the weight of the vehicle due to the addition of materials 
    and components. Cars with 3-cylinder engines weigh approximately 2,398.5 kg, whereas 8-cylinder vehicles reach 4,114.71 kg, 
    representing a staggering 172% increase in weight. This weight gain plays a crucial role in fuel efficiency and overall 
    driving dynamics.
    ''')
        
        st.info("**Key Takeaway:** Cars with higher cylinder counts deliver more horsepower but also add significant weight, while " \
        "acceleration peaks at 5 cylinders before declining—showing a trade-off between power, speed, and efficiency.")
# --------------------------------------

        st.markdown('#### Advancements in Car Technology and Fuel Efficiency Trends')
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        data = df.groupby(['origin'])['mpg'].agg('mean').sort_values(ascending=True).reset_index()

        #Build the chart using Plotly Express
        fig = px.bar(
            data, 
            x='origin', 
            y='mpg',
            title='<b>Fuel Efficiency by Vehicle Origin</b>',
            labels={'origin': 'Country of Origin', 'mpg': 'Average MPG'},
            template='plotly_white' # Gives a clean, stark white background canvas
        )
        # Fine-tune the styling to match a professional publication
        fig.update_traces(
            marker_color='#E66145',      # Premium soft coral color
            marker_line_width=0,         # Removes harsh borders
            width=0.5                    # Makes the bar widths elegant and slim
        )
        fig.update_layout(
            title_font_size=18,
            title_font_color='#111111',
            xaxis=dict(tickangle=0, title_font=dict(size=13, color='#262730')),
            yaxis=dict(title_font=dict(size=13, color='#262730'), gridcolor='#EFEFEF'),
            margin=dict(l=40, r=40, t=60, b=40), # Adds clean breathing room around the graph
            height=400
        )
        # Display natively in Streamlit (takes up full container width elegantly)
        st.plotly_chart(fig, use_container_width=True)
        st.write('''
    The continuous evolution of automobile technology has led to a remarkable increase in fuel efficiency across newer vehicle variants. 
    With each successive model release, manufacturers integrate improvements in engine design, aerodynamics, and fuel optimization, 
    contributing to enhanced mileage per gallon. This trend reflects the growing focus on delivering vehicles that not only meet 
    consumer demands for cost-effective fuel consumption but also align with sustainability goals.

    These advancements bring dual benefits—customers experience lower fuel expenses, and the environment sees reduced emissions,
    helping curb pollution. The automotive industry's commitment to innovation plays a crucial role in shaping a future where vehicles 
    are more energy-efficient, supporting efforts to minimize carbon footprints globally. As automakers continue refining their designs, 
    newer model variants are expected to further optimize fuel utilization, reinforcing the shift toward eco-friendly transportation 
    solutions.
    ''')

# ----------------------------------
        # Explore car names
        st.markdown("#### Which cars are most frequently bought?")
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        car_counts = df['car_name'].str.title().value_counts()
        car_counts = car_counts.sort_values(ascending=True)
        # Remove 'Other' if present
        car_counts = car_counts[car_counts.index != 'Other']
        # Convert Series to DataFrame for Plotly Express
        df_cars = car_counts.reset_index()
        df_cars.columns = ['car_name', 'count']
        # Initialize Chart
        fig3 = px.bar(
            df_cars,
            x='count',
            y='car_name',
            orientation='h',
            labels={'count': 'Purchase Count', 'car_name': 'Car Model'}
        )
        # Chart-Specific Customization (Using our secondary palette color)
        fig3.update_traces(
            marker_color="#2B5C8F", 
            marker_line_width=0, 
            width=0.6
        )
        # Apply your Master Theme Directly
        fig3 = apply_blog_theme(fig3, title_text="Most Commonly Bought Cars")
        # Adjusting left margin strictly for horizontal labels so long car names don't clip
        fig3.update_layout(margin=dict(l=120, r=30, t=70, b=50)) 
        # Render
        st.plotly_chart(fig3, use_container_width=True)
        st.write('''
    The analysis of consumer purchasing trends highlights Ford Pinto as the most sought-after car, leading the market in overall sales. 
    It is followed closely by Toyota Corolla, AMC Matador, and Ford Maverick, which collectively secure the top four positions in the 
    list of the ten most purchased vehicles. These models continue to be preferred by consumers due to their reliability, affordability, 
    and performance.

    Further down the rankings, Chevrolet Chevette and Impala maintain strong market presence, alongside AMC Gremlin and Hornet, 
    Toyota Corona, and Peugeot 504. While individual AMC models do not claim the top spot, their collective presence in the market 
    is significant. With three of its cars ranking within the top ten, AMC emerges as the most purchased car brand, showcasing its 
    widespread appeal among consumers.
    ''')

# ------------------------------------
        # Explore car brand names
        st.markdown("#### Market Share Analysis of Car Brands")
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        brand_name = df['car brand'].str.title().value_counts()
        # car count with greater or equal to 5
        brand_name = brand_name[brand_name >= 5].sort_values(ascending=True)
        # Convert Series to DataFrame for Plotly Express
        df_brands = brand_name.reset_index()
        df_brands.columns = ['car_brand', 'cars_sold']
        # Initialize Chart
        fig5 = px.bar(
            df_brands,
            x='cars_sold',
            y='car_brand',
            orientation='h',
            color='cars_sold',  # Maps the "cool" gradient color scale to the volume of sales
            color_continuous_scale=px.colors.sequential.ice, 
            labels={'cars_sold': 'Number of Cars Sold', 'car_brand': 'Car Brands'}
        )
        # Chart-Specific Customization
        fig5.update_traces(marker_line_width=0, width=0.6)
        fig5.update_layout(coloraxis_showscale=False) # Hides the color bar legend for a cleaner blog layout
        # Apply your Master Theme Directly
        fig5 = apply_blog_theme(fig5, title_text="Popular Car Brands")
        # Extra left margin safety for brand name labels
        fig5.update_layout(margin=dict(l=120, r=30, t=70, b=50))
        # Render
        st.plotly_chart(fig5, use_container_width=True)
        st.write('''
    Ford and Chevrolet have firmly established themselves as the dominant players in the automotive market, consistently leading in 
    vehicle sales over the observed period. Their strong brand presence and widespread consumer appeal have positioned them at the 
    forefront of the industry, capturing a significant portion of market share.

    While Plymouth, AMC, Dodge, Toyota, Datsun, and Volkswagen trail behind the leaders, they maintain respectable sales figures, 
    demonstrating competitive performance in the market. Additionally, Buick, Pontiac, Honda, Mazda, and Mercury continue to perform 
    well, reinforcing their relevance among consumers seeking reliable and well-engineered vehicles.

    On the other end of the spectrum, Renault, Chrysler, Volvo, Audi, and Fiat have struggled to gain substantial traction, with 
    significantly lower sales volumes. These brands face challenges in market penetration, resulting in comparatively lower adoption 
    rates among consumers. The overall market dynamics underscore the stronghold of established manufacturers while highlighting areas 
    of opportunity for emerging competitors.
    ''')

# -------------------------------------
        # Cars performance wrt to model year
        st.markdown("#### Variations in car features with growing years")
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        selected_car = st.selectbox("Select the car brand", 
                [
            'renault', 'chrysler', 'volvo', 'audi', 'fiat', 'peugeot', 'oldsmobile',
        'mercury', 'mazda', 'honda', 'pontiac', 'buick', 'volkswagen', 'datsun',
        'toyota', 'dodge', 'amc', 'plymouth', 'chevrolet', 'ford'
        ])
        # SECTION 1: THE GLOBAL UNIFIED LEGEND (OUTSIDE ST.COLUMNS) ---
        st.markdown("<br>", unsafe_allow_html=True) # Subtle vertical spacer
        
        # Create 4 small horizontal columns centered below the charts to act as our legend keys
        _, leg1, leg2, leg3, leg4 = st.columns([1.2, 1.2, 1.2, 1.2, 1.2])

        with leg1:
            st.markdown('<span style="color:#E66145; font-size:16px;">▬●</span> **Car Weight**', unsafe_allow_html=True)
        with leg2:
            st.markdown('<span style="color:#2B5C8F; font-size:16px;">▬●</span> **Displacement**', unsafe_allow_html=True)
        with leg3:
            st.markdown('<span style="color:#F4A261; font-size:16px;">▬●</span> **Acceleration**', unsafe_allow_html=True)
        with leg4:
            st.markdown('<span style="color:#2A9D8F; font-size:16px;">▬●</span> **MPG**', unsafe_allow_html=True)
        
        # SECTION 2: GRAPHS
        col1, col2 = st.columns(2)
        # Graph 1: Weight Trend
        with col1:
            performance_car = df[df['car brand'] == selected_car]
            weight_data = performance_car.groupby('model year')['weight'].mean().reset_index()
            
            fig1 = px.line(weight_data, x='model year', y='weight', labels={'model year': 'Model Manufactured Year', 'weight': 'Average Weight (lbs)'})
            fig1.update_traces(line=dict(color='#E66145', width=3.5), mode='lines+markers', marker=dict(size=6))
            
            fig1 = apply_blog_theme(fig1, title_text=f"{selected_car.title()} Weight Trend Over Time")
            fig1.update_layout(showlegend=False, margin=dict(l=60, r=40, t=70, b=30)) # Turned off legend & balanced padding
            st.plotly_chart(fig1, use_container_width=True)
            st.write('''
        One thing that is popping out from the above graph is that with coming years car manufactures are now shifting towards 
        manufacturing lighter cars except for some car brands which are pushing for more high performance cars like ford. This not 
        only decreases their fuel consumption but reduces the burden the fuel expenses on customers.     
        ''')

        # Graph 2: Performance Metrics
        with col2:
            metrics_data = performance_car.groupby('model year')[['acceleration', 'displacement', 'mpg']].mean().reset_index()
            metrics_melted = metrics_data.melt(id_vars=['model year'], value_vars=['acceleration', 'displacement', 'mpg'], var_name='Metric', value_name='Value')
            
            fig2 = px.line(
                metrics_melted, 
                x='model year', 
                y='Value', 
                color='Metric',
                color_discrete_map={'displacement': '#2B5C8F', 'acceleration': '#F4A261', 'mpg': '#2A9D8F'},
                labels={'model year': 'Model Manufactured Year', 'Value': 'Metric Value'}
            )
            fig2.update_traces(line=dict(width=3), mode='lines+markers', marker=dict(size=5))
            
            fig2 = apply_blog_theme(fig2, title_text=f"{selected_car.title()} Performance Characteristics")
            fig2.update_layout(showlegend=False, margin=dict(l=60, r=40, t=70, b=30)) # Turned off legend & balanced padding
            st.plotly_chart(fig2, use_container_width=True)
            st.write('''
        Acceleration is held steady with some slight decrease in mid 70's, whereas mileage of cars (mpg) is steadily growing year by year.
        Displacement is directly proportional to number of cylinders, as number of cylinders in engine are coming down so do displacement.        
        ''')
            
        # SECTION 2: THE GLOBAL UNIFIED LEGEND (OUTSIDE ST.COLUMNS) ---
        st.markdown("<br>", unsafe_allow_html=True) # Subtle vertical spacer
        
        # Create 4 small horizontal columns centered below the charts to act as our legend keys
        # _, leg1, leg2, leg3, leg4 = st.columns([1.2, 1.2, 1.2, 1.2, 1.2])

        # with leg1:
        #     st.markdown('<span style="color:#E66145; font-size:16px;">▬●</span> **Car Weight**', unsafe_allow_html=True)
        # with leg2:
        #     st.markdown('<span style="color:#2B5C8F; font-size:16px;">▬●</span> **Displacement**', unsafe_allow_html=True)
        # with leg3:
        #     st.markdown('<span style="color:#F4A261; font-size:16px;">▬●</span> **Acceleration**', unsafe_allow_html=True)
        # with leg4:
        #     st.markdown('<span style="color:#2A9D8F; font-size:16px;">▬●</span> **MPG**', unsafe_allow_html=True)
        

# ------------------------------------
        # origin vs mpg vs model year
        st.markdown("#### Impact of Model Year and Car Origin on Fuel Efficiency")
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        # Data Preparation (Aggregate the mean MPG grouped by year and origin)
        trend_data = df.groupby(['model year', 'origin'])['mpg'].mean().reset_index()
        # Initialize Multi-line Chart
        fig8 = px.line(
            trend_data,
            x='model year',
            y='mpg',
            color='origin',
            # Map premium blog-consistent hex values to your categorical origins
            color_discrete_map={
                'usa': '#E66145',     # Premium Coral
                'europe': '#2B5C8F',  # Slate Blue
                'japan': '#2A9D8F'    # Deep Teal
            },
            labels={'model year': 'Model Year', 'mpg': 'Average Miles Per Gallon', 'origin': 'Origin'}
        )
        # Chart-Specific Customization (Thick lines and clear marker points)
        fig8.update_traces(line=dict(width=3.5), mode='lines+markers', marker=dict(size=6))

        # Apply your Master Theme Directly
        fig8 = apply_blog_theme(fig8, title_text="Car Mileage Trends by Region and Model Year")

        # Optional: Since this chart has its own internal legend for 'origin', we position it cleanly
        fig8.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",                      # Vertical stack looks cleaner inside the grid
                yanchor="top",
                y=0.95,                               # Just under the top grid line
                xanchor="left",
                x=0.02,                               # Nudged slightly right of the Y-axis line
                bgcolor="rgba(255, 255, 255, 0.7)",   # Translucent background so gridlines don't clip text
                title_text="Car's Generation"
            )
        )
        # Render
        st.plotly_chart(fig8, use_container_width=True)
        st.write('''
    The analysis reveals a strong correlation between model year and fuel efficiency, demonstrating significant advancements in 
    automotive engineering over time. As newer car models were introduced, manufacturers optimized fuel consumption, leading to 
    more efficient vehicles. The data shows that in the early 1970s to mid-1970s, cars achieved an average of 25 to 30 miles per 
    gallon (MPG). However, from the late 1970s onward, mileage improved steadily, reaching 40 MPG by the early 1980s—a remarkable 
    increase compared to the previous decade.       
    
    Additionally, car origin played a critical role in fuel efficiency trends. Vehicles from origin 1 consistently showed lower fuel 
    efficiency than those from origin 2 and 3, suggesting differences in manufacturing strategies and technological advancements across 
    regions. This trend highlights how design and engineering standards across different markets influenced mileage performance.
             
    From a cost perspective, this efficiency improvement is substantial. If one gallon of gasoline cost $10 in the 1970s, then by the 
    1980s, the same amount of fuel allowed cars to travel an additional 10 miles, effectively reducing fuel expenses for consumers 
    while contributing to sustainability efforts. These insights underscore the evolution of fuel-efficient automobiles, driven by 
    continuous research, innovation, and consumer demand for cost-effective transportation.
    ''')

# --------------------------------
        # car weight vs model year
        st.markdown("#### The weight of the car has been significantly descreased in coming years with automotive innovation")
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        # 1. Data Preparation (Aggregate mean weight by model year)
        weight_trend = df.groupby('model year')['weight'].mean().reset_index()
        # Calculate linear regression trendline coordinates manually using NumPy
        x_vals = weight_trend['model year']
        y_vals = weight_trend['weight']
        slope, intercept = np.polyfit(x_vals, y_vals, 1)
        weight_trend['regression_trend'] = slope * x_vals + intercept
        # Initialize Base Chart (Main Weight Line)
        fig9 = px.line(
            weight_trend,
            x='model year',
            y='weight',
            labels={'model year': 'Model Year', 'weight': 'Average Weight (lbs)'}
        )
        # Style main line with premium brand coral
        fig9.update_traces(
            line=dict(color='#E66145', width=3.5), 
            mode='lines+markers', 
            marker=dict(size=6),
            name='Average Weight'
        )
        # Add the Dashed Regression Trendline Layer
        fig9.add_scatter(
            x=weight_trend['model year'],
            y=weight_trend['regression_trend'],
            mode='lines',
            line=dict(color='#555555', width=1.5, dash='dash'),
            name='Linear Trend',
            hoverinfo='skip' # Keeps data hover clean by only focusing on real data points
        )
        # Apply your Master Theme Directly
        fig9 = apply_blog_theme(fig9, title_text="Decrease in Car Weight Over Model Years")

        # Clean layout tuning with zero overlapping text risk
        fig9.update_layout(
            showlegend=False, 
            margin=dict(l=60, r=40, t=70, b=50)
        )
        # Render
        st.plotly_chart(fig9, use_container_width=True)
        st.write('''
    Advancements in automotive research and development have led to significant reductions in vehicle weight, contributing to improved 
    fuel efficiency. As manufacturers focus on making cars more affordable, lightweight materials and optimized engineering designs 
    have played a crucial role in enhancing mileage.

    Over the past decade, the average weight of cars has decreased from 3,400 kg to 2,400 kg, representing a 30% reduction. This 
    decline in weight directly impacts fuel consumption, as lighter vehicles require less energy to operate, leading to increased 
    miles per gallon. These innovations not only provide cost savings for consumers but also support sustainability efforts by reducing 
    fuel dependency and lowering emissions.

    With ongoing advancements in material science and vehicle aerodynamics, the trend toward lighter, more efficient cars is expected 
    to continue, shaping the future of the automotive industry.
    ''')

# -----------------------------------
        # Car performance with coming years
        st.markdown("#### Growing years shows a decrease in muscle cars production.")
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        make_year = df.groupby('model year',as_index=False)[['horsepower','acceleration','displacement','cylinders']].agg('mean')
        # SECTION 1: GRAPHS
        col1, col2 = st.columns(2)
        with col1:
            # Melt metrics for the first plot
            df_melted1 = pd.melt(make_year,id_vars=['model year'], value_vars=['horsepower', 'displacement'], var_name='Metric', value_name='Value') 
            fig1 = px.line(
                df_melted1, 
                x='model year', 
                y='Value', 
                color='Metric',
                color_discrete_map={
                    'horsepower': '#E66145',    
                    'displacement': '#2B5C8F'  
                },
                labels={'model year': 'Model Year', 'Value': 'Metric Value'}
            )        
            # Trace styling
            fig1.update_traces(line=dict(width=3), mode='lines+markers', marker=dict(size=5))
            # Apply theme and interior legend
            fig1 = apply_blog_theme(fig1, title_text="Engine Output Trends Over Time")
            fig1.update_layout(
                margin=dict(l=60, r=40, t=70, b=30),
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Melt metrics for the second plot
            df_melted2 = make_year.melt(id_vars=['model year'], value_vars=['acceleration', 'cylinders'], var_name='Metric', value_name='Value')
            fig2 = px.line(
                df_melted2, 
                x='model year', 
                y='Value', 
                color='Metric',
                color_discrete_map={
                    'acceleration': '#F4A261',  
                    'cylinders': '#2A9D8F'     
                },
                labels={'model year': 'Model Year', 'Value': 'Metric Value'}
            )
            # Trace styling
            fig2.update_traces(line=dict(width=3), mode='lines+markers', marker=dict(size=5))
            # Apply theme and interior legend to match Column 1 symmetry
            fig2 = apply_blog_theme(fig2, title_text="Mechanical Dynamics Over Time")
            fig2.update_layout(
                margin=dict(l=60, r=40, t=70, b=30),
                showlegend=False  # Hide legend here to avoid duplication with Column 1
            )
            st.plotly_chart(fig2, use_container_width=True)
        #SECTION 2: THE GLOBAL UNIFIED LEGEND (OUTSIDE ST.COLUMNS) ---
        st.markdown("<br>", unsafe_allow_html=True) # Subtle vertical spacer
        # Create 4 small horizontal columns centered below the charts to act as our legend keys
        _, leg1, leg2, leg3, leg4 = st.columns([0.5, 1.2, 1.2, 1.2, 1.2])

        with leg1:
            st.markdown('<span style="color:#F4A261; font-size:16px;">▬●▬</span> **Acceleration**', unsafe_allow_html=True)
        with leg2:
            st.markdown('<span style="color:#2B5C8F; font-size:16px;">▬●▬</span> **Displacement**', unsafe_allow_html=True)
        with leg3:
            st.markdown('<span style="color:#2A9D8F; font-size:16px;">▬●▬</span> **Cylinders**', unsafe_allow_html=True)
        with leg4:
            st.markdown('<span style="color:#E66145; font-size:16px;">▬●▬</span> **Horsepower**', unsafe_allow_html=True)
        
# ---------------------------------
        # with weight of car as in groups
        st.markdown("#### How does the weight of car affects the customer's buying preference?")
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        weight_counts = df['weight groups'].value_counts().sort_values(ascending=True)
        # Convert Series to DataFrame for Plotly Express
        df_weights = weight_counts.reset_index()
        df_weights.columns = ['weight_group', 'car_count']
        # Initialize Chart
        fig11 = px.bar(
            df_weights,
            x='car_count',
            y='weight_group',
            orientation='h',
            color='car_count', # Maps the cool color scale gradient to the volume of cars
            color_continuous_scale=px.colors.sequential.ice,
            labels={'car_count': 'Number of Cars', 'weight_group': 'Weight Category'}
        )
        # Chart-Specific Customization
        fig11.update_traces(marker_line_width=0, width=0.6)
        fig11.update_layout(coloraxis_showscale=False) # Removes color bar legend clutter
        # Apply your Master Theme Directly
        fig11 = apply_blog_theme(fig11, title_text="Distribution of Cars Across Weight Categories")
        # Add generous left margin padding so category text strings don't clip on the axis
        fig11.update_layout(margin=dict(l=140, r=40, t=70, b=50))
        # Render
        st.plotly_chart(fig11, use_container_width=True)
        st.write("""
    The distributions shows concentration in the mid-weight range. The largest group falls in the category of 
    2000 - 2500 kg, followed by 2500 - 3000 with just less than 100 cars falling in this category. There is a noticable
    tapering off at both extremes: fewer vehicles exist in the lightest and heaviest segments. This pattern suggests
    that most cars are designed within 2500 - 3000 kg range, likely balancing performance.
    
    Weight affects buyer's preference as heavier cars are generally perceived as safer in collisions, whereas light-weight
    cars are environment friendly and most appealing for buyers and it's clearly visible too.
    Weight also plays a crucial role in influencing car's fuel efficiency. As lighter cars tends to consume less
    fuel and they are also the most preferred choice of constumers. Heavier cars are great to gain driving experience
    but heavy on pocket as they drinks lot of fuel in their run.
    
    Performance of car is also not too far from getting affected by its weight. As weight rises, the time taken to
    accelerate and decelerate the car also rises. So, to gain speed it will take more time than lighter cars and during
    braking too. Emissions are also higher for heavier cars as they consume more fuel to drive same length when 
    compared to a light weight car.        
    """)

# -----------------------------------
        # Explore target variable
        st.subheader("Explore the target variable",divider='rainbow')
        st.markdown('''##### Distribution of Miles Per Gallon (MPG) in the Market''')
        # 1. Initialize Interactive Histogram with Marginal Profiles
        fig2 = px.histogram(
            df,
            x='mpg',
            color='origin',
            nbins=20,
            marginal='violin', # Adds a sleek, modern distribution profile curve right above the bars
            barmode='overlay', # Overlays categories cleanly with transparency instead of stacking them
            # Map premium consistent hex values to your categorical origins
            color_discrete_map={
                1: '#002966',     # Premium Coral
                2: "#BF00FF",  # Slate Blue
                3: "#3385FF"    # Deep Teal
            },
            labels={'mpg': 'Miles Per Gallon', 'count': 'Frequency', 'origin': 'Origin'}
        )
        # Chart-Specific Customization (Control opacity for professional blending)
        fig2.update_traces(opacity=0.75, marker_line_width=0.5, marker_line_color='#FFFFFF')
        # Apply your Master Theme Directly
        fig2 = apply_blog_theme(fig2, title_text="Distribution of MPG by Vehicle Origin")
        # Clean Horizontal Legend Tuning (Avoiding layout overlapping issues)
        fig2.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.25,
                xanchor="center",
                x=0.5,
                title_text=""
            ),
            margin=dict(l=70, r=40, t=80, b=100), # Increased bottom padding for the legend placement
            # Inject an absolute-positioned text annotation directly in the middle!
            annotations=[
                dict(
                    text="<b>Car Generation</b>", # Your styled legend title
                    xref="paper",                # Scale relative to the entire chart width
                    yref="paper",                # Scale relative to the entire chart height
                    x=0.5,                       # 0.5 is the exact horizontal center
                    y=-0.27,                     # Positioned perfectly right above the legend items
                    showarrow=False,             # Turn off pointing arrows
                    font=dict(size=12, color="#555555"), # Match your blog text theme colors
                    align="center"
                )
            ]
        )
        # Render
        st.plotly_chart(fig2, use_container_width=True)
        st.write('''
    The histogram analysis of miles per gallon (MPG) reveals a right-skewed distribution, indicating that the majority of vehicles
    have mileage below 30 MPG. The highest concentration of cars is observed around 15 MPG, making them the most common in the market. 
    This suggests that fuel efficiency remains a challenge for a significant portion of vehicles, particularly those with larger 
    engines or older designs.

    Conversely, cars with MPG greater than 35 are relatively rare, and as efficiency surpasses 40 MPG, the number of available models 
    declines drastically. These ultra-efficient vehicles are limited in the market, reflecting the technological constraints or consumer 
    preferences that may favor performance over fuel economy.

    Understanding this distribution can help manufacturers and policymakers evaluate trends in fuel efficiency, identifying opportunities
    to promote higher-mileage models and encourage sustainable transportation solutions.        
    ''')

# ------------------------------------------
        # Target variable vs rest numeric variable
        st.markdown('#### Correlation between numeric features and target variables')
        st.markdown(
    """
    <hr style="
        border: none;
        height: 3px;
        background-color: #2B5C8F;
        margin-top: -10px;
        margin-bottom: 25px;
        border-radius: 2px;
    ">
    """, 
    unsafe_allow_html=True
)
        col1, col2 = st.columns(2)
        with col1:
            feature = st.selectbox("Select a car feature", ['weight', 'displacement'])
            cor = df[feature].corr(df['mpg'])
            st.info(f'Coorelation between {feature} and mpg: {round(cor,3)}')
            fig1, ax1 = plt.subplots()
            sns.scatterplot(data=df, x=feature, y='mpg', color='indianred', ax=ax1)
            ax1.set_xlabel(f'{feature}')
            ax1.set_ylabel('Miles per Galloon')
            st.pyplot(fig1)
            if feature == 'weight':
                st.write('''
            The correlation between car weight and miles per galloon is -0.832, indicating a strong negative relationship
            . Heavier cars tend to have lower fuel efficiency. This means as vehicle weight increases, mileage 
            generally decreases significantly. Understanding this trend is crucial for making informed purchasing
            decisions.
            ''')
            else:
                st.write('''
                The correlation between car engine displacement and miles per galloon is -0.804, showing a strong negative
                relationship. Larger engines typically result in lower fuel efficiency. This suggests that as engine size
                increases, car tends to consume more fuel per mile. Such insight is important for balancing performance
                needs with fuel economy in both engineering and consumer choices.
                ''')

        with col2:
            feature = st.selectbox("Select a car feature", ['acceleration', 'horsepower'])
            cor = df[feature].corr(df['mpg'])
            st.info(f'Coorelation between {feature} and mpg: {round(cor,3)}')
            fig2, ax2 = plt.subplots()
            sns.scatterplot(data=df, x=feature, y='mpg', color='indianred', ax=ax2)
            ax2.set_xlabel(f'{feature}')
            ax2.set_ylabel('Miles per Galloon')
            st.pyplot(fig2)
            if feature == 'acceleration':
                st.write('''
            The correlation between acceleration and miles per galloon is 0.402, indicating a moderate positive relationship
            Cars with better acceleration tend to have slightly higher fuel efficiency. While the coonection isn't as strong
            as with other features, it suggests that well performing vehicles can still be economical. This highlights
            that performance and efficiency are not always mutually exclusive
            ''')
            else:
                st.write('''
            The correlation between horsepower and miles per galloon is -0.773, showing a strong negative
            relationship. Cars with more horsepower generally have lower fuel efficiency. This means higher engine
            power often comes at the cost of consuming more fuel. It's a key trade-off to consider when balancing
            performance with operating costs.
            ''')

# show_page = show_explore_page()