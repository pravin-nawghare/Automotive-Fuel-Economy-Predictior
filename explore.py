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
    st.header("Explore Car Brands", divider='grey')
    st.text("")

    # st.subheader("Weight of cars vs MPG",divider='rainbow')
    # fig6, ax6 = plt.subplots()
    # #data = df.groupby(['weight groups'])['mpg'].agg('mean')
    # fig6 = sns.barplot(data=df,x=df.groupby(['weight groups'])['mpg'].agg('mean'),y='mpg' ,ax=ax6)
    # ax6.set_xlabel('Weight group of cars')
    # ax6.set_ylabel('Fuel consumed in Miles per galloon')
    # ax6.set_title('Weight vs MPG')
    # st.pyplot(fig6)

    st.write("About the data....")
    st.subheader("Which engine is dominating the roads? Are less number of cylinders more preferrable.", divider='rainbow')
    col1, col2 = st.columns(2)
    # Bar plot: Average MPG by Number of Cylinders
    with col1:
        st.write("""
        **Fuel consumed by cars with different number of cylinders they have**
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
    Cars with 4 cylinders engine are most preferred choice as it captures 51.3% of market share,and also a great option for wider range of 
    customers who are looking for fuel efficient cars as these cars are most fuel efficient compared to other engine cylinder configuration
    by covering distance around 30 miles in one galloon of gasoline. Cars with 5 cylinder engine also a fuel efficient variant but they 
    even >1% in the market. Cylinders with higher number like 6 and 8 are great performance cars with high acceleration, power and speed.
    But to give all these great things they have consume to more fuel, infact 8 cylinder engine is least fuel efficent car in the car 
    market with only 15 miles per galloon mileage but 6 cylinder engine car comes with good overall package as they have decent mileage
    and rest of the feaures from 8 cyliner engine car. But the most important thing is these cars covers whooping 47% market share.
    3 cylinder engine is also same as 6 cylinder engine in terms of mileage but they are also very rare in the market.  
    """)
    cylinder_df = df.groupby('cylinders')[['horsepower','acceleration','weight','displacement']].agg('mean')
    st.text("Relation between increase in number of cylinders with respective to cars performance")
    st.dataframe(cylinder_df)
    st.write('''Above table shows how other parameters of varies with variation in number of engine cylinders.
    Cars with 3 cylinder engine were producing 99.25Bhp of horespower with 13.25 acceleration, with 4 cylinder engine
    horsepower has decreased to 78.65Bhp but acceleration has risen to 16.60. With increase in cylinders upto 5 acceleration of car was rising
    but but 6 and 8 it has decresed significantly. Similarily, horsepower has been rising only.
    When it comes to weight of the cars as cylinders increases material inside car increases eventually, 
    weight also increases. From 2398.5 kg with 3 cylinder engine it has increase to 4114.71 kg
    for 8 cylinder engine, which is an increase of 172% in weight of cars. 
    ''')

    st.subheader('Origin ',divider='rainbow')
    data = df.groupby(['origin'])['mpg'].agg('mean').sort_values(ascending=True)
    fig10,ax10 = plt.subplots()
    data.plot(kind='bar', ax=ax10, color='orange')
    ax10.set_xlabel('Origin')
    ax10.set_ylabel('Miles Per Galloon')
    #ax10.set_title('Most commonly bought cars')
    st.pyplot(fig10)
    st.write('''
    The amount of distance covered by cars is increasing as the origin of cars has been increased. It is a great thing to see with 
    with more and more research and advancement in car technology it is clearly visible how automakers are now manufacturing fuel 
    efficient cars which is not only beneficial for customer but for environment also by curbing the pollution.   
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
    Ford Pinto is most desirable car for the consumers as it most commonly bought car, followed by Toyota Corolla, AMC Matador and
    Ford Maverick. All these sits on top 4 positions in the top 10 most bought car list. Below them comes Chevrolet Chevette and 
    Impalla, AMC Gremlin and Hornet, Toyota Corona and Puegot 504. From this list it has been observed that though individual cars 
    of AMC do not occupy first position but coming together they are most bought car brand in the market with 3 cars in top 10. 
    ''')

    # Explore car brand names
    st.subheader("Which car brand is dominating the car market?",divider='rainbow')
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
    Ford and Chervolet has undoubtely has captured most of the market, by selling most number of cars in the given years. Plymouth,
    AMC, Dodge, Toyota, Datsun and Volkswagen are not that far in the list but by far in terms of count of cars sold. Buick, Pontiac, 
    Honda, Mazda and Mercury are also doing well. Rest of the brands like Renault, Chrysler, Volvo, Audi and Fiat are barely making 
    their cars into hands of customers. They are the least sold car brands in the market.
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
        One thing that is popping out from the above graph is that with coming years car
        manufactures are now shifting towards manufacturing lighter cars. This not only decreases their fuel consumption 
        but reduces the burden the fuel expenses on customers.     
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
    st.subheader("How does the origin of car and make year affects fuel consumption of cars?",divider='rainbow')
    fig8,ax8 = plt.subplots()
    sns.lineplot(data=df, x='model year', y='mpg', marker='o', hue='origin',palette='cool', errorbar=None)
    ax8.set_xlabel("Model Year")
    ax8.set_ylabel("Miles per galloon")
    ax8.set_title("Car mileage has incerased with growing years and origin")
    st.pyplot(fig8)
    st.write('''
    Model year has seen high correlation with mileage of cars, similarly origin too. As the model year kept on 
    rising the car are becoming more and more fuel efficient. Cars with origin 1 were always way less fuel 
    efficient compared to cars with origin 2 and 3. In early 70 to mid 70's the distance covered by cars in 
    one galloon of gasoline was 25 to 30 miles. But from late 70's it has started rising and in the early 80's 
    it reached the mark the of 40 miles in one galloon of gasoline, which a decade ago varing between 25 - 30.
    In other terms it can be interpretated as, if one galloon of gasoline costs $10 in 70's then with same 
    amount of fuel now 10 miles are extra covered by the cars in 80's         
    ''')

    # car weight vs model year
    st.subheader("The weight of the car has been significantly descreased in coming years with advancement in technology",divider='rainbow')
    fig9,ax9 = plt.subplots()
    sns.lineplot(data=df, x='model year', y='weight',marker='o',color='violet')
    sns.regplot(data=df, x='model year', y='weight', scatter=False, label ='Trend', color='red',line_kws={'linestyle':'--','linewidth':0.5},ci=None)
    ax9.set_xlabel("Model Year")
    ax9.set_ylabel("Weight of car")
    #ax9.set_title("Decrease in car weight with growing years")
    st.pyplot(fig9)
    st.write('''
    As research and development teams of all car brands are working to make more affordable, the cars are 
    also becoming light in weight thus increasing the mileage of the cars. In a decade on research the car
    weight has been decreased from 3400kg to 2400kg which is decrease of about 30% in car weight.
    ''')

    # Car performance with coming years
    st.subheader("Growing years has seen decrease in performance of cars",divider='rainbow')
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
    st.subheader("Car weights",divider='rainbow')
    fig11,ax11 = plt.subplots()
    c = sns.color_palette(palette='cool',n_colors=10)
    data = df['weight groups'].value_counts().sort_values(ascending=True)
    # sns.barplot(data=data, x=df['car weights'], color=c )
    data.plot(kind='barh', color=c, ax=ax11)
    ax11.set_xlabel("Number of cars")
    ax11.set_ylabel("Weight of car")
    ax11.set_title("How heavy cars are their in the market")
    st.pyplot(fig11)
    st.write("")

    # Explore target variable
    st.subheader("Explore target variable",divider='rainbow')
    fig2, ax2 = plt.subplots()
    sns.histplot(data=df, x='mpg', hue='origin', bins=20, kde=True, palette='autumn', ax=ax2)
    ax2.set_xlabel('Miles Per Galloon')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of MPG')
    st.pyplot(fig2)
    st.write('''
    The histogram plot of miles per galloon (mpg) is right skewed. Most of the cars have mileage less 30 miles.
    With mpg around 15 their are most number of cars in the market. Very few of them are greater than 35 but as 
    mpg goes above 40 the number of cars with range of distance covered in one galloon of fuel are hardly 
    countable on finger tips.        
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