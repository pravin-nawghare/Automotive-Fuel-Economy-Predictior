import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("EDA on Automotive Fuel Economy Predictor")

def clean_data(df,column):
    df[column] = df[column].replace('?',np.nan)
    df[column] = df[column].astype(float)
    median_value = df[column].median()
    df[column] = df[column].fillna(median_value)
    return df

def car_name_reduce(categories,cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "other"
    return categorical_map

rename_maps = {'vw':'volkswagen', 'chevy':'chevrolet', 'vokswagen':'volkswagen', 'maxda':'mazda','toyouta':'toyota', 'chevroelt':'chevrolet'}
def extract_car_brand(df, old_column, new_column, rename_map):
    df[new_column] =  df[old_column].astype(str).str.split().str[0]

    # rename car names
    if rename_map:
        df[new_column] = df[new_column].map(lambda x: rename_map.get(x,x))
    return df

def grouping_car_by_weights(df, column):
    labels = ['1500 - 2000','2000 - 2500','2500 - 3000','3000 - 3500','3500 - 4000','4000 - 4500','up-to 5000']
    bins = [1500,2000,2500,3000,3500,4000,4500, 5000]
    df['weight groups'] = pd.cut(df[column], bins=bins, labels=labels)
    return df

def load_data():
    df = pd.read_csv('auto-mpg.csv')

    #clean data
    df = clean_data(df,'horsepower')
    
    # extract car brands
    df = extract_car_brand(df, 'car name', 'car brand', rename_maps)

    # reduce car name
    car_map = car_name_reduce(df['car name'].value_counts(),4)
    df['car_name'] = df['car name'].map(car_map)

    # group by their weights
    df = grouping_car_by_weights(df, 'weight')
    
    return df

df = load_data()

def show_explore_page():
    # st.header("Explore various car brands in the market", divider='grey')
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

    # st.subheader("Weight of cars vs MPG",divider='rainbow')
    # fig6, ax6 = plt.subplots()
    # #data = df.groupby(['weight groups'])['mpg'].agg('mean')
    # fig6 = sns.barplot(data=df,x=df.groupby(['weight groups'])['mpg'].agg('mean'),y='mpg' ,ax=ax6)
    # ax6.set_xlabel('Weight group of cars')
    # ax6.set_ylabel('Fuel consumed in Miles per galloon')
    # ax6.set_title('Weight vs MPG')
    # st.pyplot(fig6)

    st.subheader("Which engine is dominating the roads? Are less number of cylinders more preferrable.", divider='rainbow')
    col1, col2 = st.columns(2)
    # Bar plot: Average MPG by Number of Cylinders
    with col1:
        st.write("""
        **Engine Cylinder Configuration and Market Trends in Fuel Efficiency**
                 """)
        mpg_by_cyl = df.groupby('cylinders')['mpg'].mean().reset_index()
        # Ensure consistent order
        unique_cyls = sorted(df['cylinders'].unique())
        color_palette = sns.color_palette("pastel", len(unique_cyls))
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


    cylinder_df = df.groupby('cylinders')[['horsepower','acceleration','weight','displacement']].agg('mean')
    st.text("Impact of Engine Cylinder Variation on Key Performance Metrics")
    st.dataframe(cylinder_df)
    st.markdown('''
    Above table shows how vehicle performance parameters highlights the significant influence of engine cylinder 
    count on horsepower, acceleration, and weight.
    
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

    st.subheader('Advancements in Car Technology and Fuel Efficiency Trends',divider='rainbow')
    data = df.groupby(['origin'])['mpg'].agg('mean').sort_values(ascending=True)
    fig10,ax10 = plt.subplots()
    data.plot(kind='bar', ax=ax10, color='orange')
    ax10.set_xlabel('Origin')
    ax10.set_ylabel('Miles Per Galloon')
    #ax10.set_title('Most commonly bought cars')
    st.pyplot(fig10)
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


    # Explore car names
    st.subheader("Which cars are most frequently bought?", divider='rainbow')
    car_counts = df['car_name'].str.title().value_counts()
    car_counts = car_counts.sort_values(ascending=True)
    # Remove 'Other' if present
    car_counts = car_counts[car_counts.index != 'Other']
    fig3, ax3 = plt.subplots()
    car_counts.plot(kind='barh', ax=ax3, color='skyblue')
    ax3.set_xlabel('Count')
    ax3.set_ylabel('Car Name')
    ax3.set_title('Most commonly bought cars')
    st.pyplot(fig3)
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

    # Explore car brand names
    st.subheader("Market Share Analysis of Car Brands",divider='rainbow')
    fig5, ax5 = plt.subplots()
    c= sns.color_palette(palette="cool", n_colors=31)
    brand_name = df['car brand'].str.title().value_counts()
    # car count with greater or equal to 5
    brand_name = brand_name[brand_name >= 5].sort_values(ascending=True)
    #sns.countplot(data=brand_name,  palette = c, ax=ax5)
    brand_name.plot(kind='barh',ax=ax5, color=c)
    ax5.set_xlabel('Number of cars sold')
    ax5.set_ylabel('Car Brands')
    ax5.set_title('Popular Car Brands')
    st.pyplot(fig5)
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

    # Cars performance wrt to model year
    st.subheader("Variations in car features with growing years",divider='rainbow')  
    selected_car = st.selectbox("Select the car brand", 
            [
        'renault', 'chrysler', 'volvo', 'audi', 'fiat', 'peugeot', 'oldsmobile',
       'mercury', 'mazda', 'honda', 'pontiac', 'buick', 'volkswagen', 'datsun',
       'toyota', 'dodge', 'amc', 'plymouth', 'chevrolet', 'ford'
    ])
    col1, col2 = st.columns(2)
    with col1:
        fig1,ax1 = plt.subplots()
        performance_car = df[df['car brand'] == selected_car]
        performance_car.groupby('model year')[['weight']].agg('mean')
        sns.lineplot(data=performance_car, x='model year', y='weight',color ='red',errorbar=None,ax=ax1)
        ax1.set_xlabel('Model manufactured year')
        ax1.set_ylabel('Weight of car')
        ax1.set_title('Car weight vs model year')
        st.pyplot(fig1)
        st.write('''
        One thing that is popping out from the above graph is that with coming years car manufactures are now shifting towards 
        manufacturing lighter cars except for some car brands which are pushing for more high performance cars like ford. This not 
        only decreases their fuel consumption but reduces the burden the fuel expenses on customers.     
        ''')

    with col2:
        fig1,ax1 = plt.subplots()
        performance_car = df[df['car brand'] == selected_car]
        performance_car.groupby('model year')[['acceleration','displacement','mpg']].agg('mean')
        sns.lineplot(data=performance_car, x='model year', y='displacement',color = 'green',label='displacememnt',errorbar=None,ax=ax1)
        sns.lineplot(data=performance_car, x='model year', y='acceleration',color = 'blue',label='acceleration',errorbar=None,ax=ax1)
        sns.lineplot(data=performance_car, x='model year', y='mpg',color = 'violet',label='MPG',errorbar=None,ax=ax1)
        ax1.set_xlabel('Model manufactured year')
        ax1.set_ylabel('Car performance characteristics')
        ax1.set_title('Car performance metrics')
        st.pyplot(fig1)
        st.write('''
        Acceleration is held steady with some slight decrease in mid 70's, whereas mileage of cars (mpg) is steadily growing year by year.
        Displacement is directly proportional to number of cylinders, as number of cylinders in engine are coming down so do displacement.        
        ''')

    #alernate
    # st.subheader("Cars manufactured in early 70s were more compared to late 70s and early 80s",divider='rainbow')
    # year_counts = df['model year'].value_counts().sort_index()
    # year_df = pd.DataFrame({'Model Year':year_counts.index, 'Count': year_counts.values})
    # year_df.set_index('Model Year', inplace=True)
    # #plot
    # fig7,ax7 = plt.subplots()
    # sns.lineplot(data=year_df, x=year_df.index, y='Count', marker='o')
    # ax7.set_xlabel("Model Year")
    # ax7.set_ylabel("Number of cars manufactured")
    # ax7.set_title("Numbers of car manufactured in different year")
    # ax7.set_ylim(20,45)
    # st.pyplot(fig7)
    # st.text('''    
    # ''')

    # origin vs mpg vs model year
    st.subheader("Impact of Model Year and Car Origin on Fuel Efficiency",divider='rainbow')
    fig8,ax8 = plt.subplots()
    sns.lineplot(data=df, x='model year', y='mpg', marker='o', hue='origin',palette='cool', errorbar=None)
    ax8.set_xlabel("Model Year")
    ax8.set_ylabel("Miles per galloon")
    ax8.set_title("Car mileage has incerased with growing years and origin")
    st.pyplot(fig8)
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

    # car weight vs model year
    st.subheader("The weight of the car has been significantly descreased in coming years with automotive innovation",divider='rainbow')
    fig9,ax9 = plt.subplots()
    sns.lineplot(data=df, x='model year', y='weight',marker='o',color='violet')
    sns.regplot(data=df, x='model year', y='weight', scatter=False, label ='Trend', color='red',line_kws={'linestyle':'--','linewidth':0.5},ci=None)
    ax9.set_xlabel("Model Year")
    ax9.set_ylabel("Weight of car")
    #ax9.set_title("Decrease in car weight with growing years")
    st.pyplot(fig9)
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

    # Car performance with coming years
    st.subheader("Growing years has seen decrease in high performance cars",divider='rainbow')
    make_year = df.groupby('model year')[['horsepower','acceleration','displacement','cylinders']].agg('mean')
    col1, col2 = st.columns(2)
    with col1:
        fig1,ax1 = plt.subplots()
        sns.lineplot(data=make_year, x='model year', y='horsepower',marker='o', color='blue', errorbar=None,label='horsepower')
        sns.lineplot(data=make_year, x='model year', y='displacement',marker='*', color='red', errorbar=None,label='displacement')
        ax1.set_xlabel("Model Year")
        #ax1.set_ylabel("Displacement/Horsepower")
        ax1.set_title("Horsepower and Displacement vs Model Year")
        st.pyplot(fig1)
    with col2:
        fig2,ax2 = plt.subplots()
        sns.lineplot(data=make_year, x='model year', y='acceleration', marker='o' ,color='orange', errorbar=None,label='acceleration')
        sns.lineplot(data=make_year, x='model year', y='cylinders',marker='*', color='red', errorbar=None,label='cylinders')
        ax2.set_xlabel("Model Year")
        ax2.set_title("Acceleration and Engine Cylinders vs Model Year")
        st.pyplot(fig2)

    # with weight of car as in groups
    st.subheader("Cars in different weights category",divider='rainbow')
    fig11,ax11 = plt.subplots()
    c = sns.color_palette(palette='cool',n_colors=10)
    data = df['weight groups'].value_counts().sort_values(ascending=True)
    # sns.barplot(data=data, x=df['car weights'], color=c )
    data.plot(kind='barh', color=c, ax=ax11)
    ax11.set_xlabel("Number of cars")
    ax11.set_ylabel("Weight of car")
    ax11.set_title("How does the weight of car affects the customer's buying preference?")
    st.pyplot(fig11)
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

    # Explore target variable
    st.subheader("Explore the target variable",divider='rainbow')
    st.markdown('''
            ##### Distribution of Miles Per Gallon (MPG) in the Market
                ''')
    fig2, ax2 = plt.subplots()
    sns.histplot(data=df, x='mpg', hue='origin', bins=20, kde=True, palette='autumn', ax=ax2)
    ax2.set_xlabel('Miles Per Galloon')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of MPG')
    st.pyplot(fig2)
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

    # Target variable vs rest numeric variable
    st.subheader('Correlation between numeric features and target variables',divider='rainbow')
    col1, col2 = st.columns(2)
    with col1:
        feature = st.selectbox("Select a car feature", ['weight', 'displacement'])
        cor = df[feature].corr(df['mpg'])
        st.text(f'Coorelation between {feature} and mpg: {round(cor,3)}')
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
        st.text(f'Coorelation between {feature} and mpg: {round(cor,3)}')
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