# Automotive Fuel Economy Prediction

## Project Overview
Understanding and predicting fuel efficiency is crucial, given rising fuel costs and growing environmental concerns. This report delves into the factors influencing automotive fuel consumption, focusing on a dataset of various car models. The analysis aims to estimate how far a car can travel on a single gallon of fuel, using key vehicle attributes such as weight, acceleration, cylinder count, etc. By leveraging machine learning techniques, the goal is to uncover patterns that influence fuel efficiency, ultimately providing insights that can assist manufacturers, consumers, and policymakers in making informed decisions.

The dataset used for this analysis includes various features that directly impact a vehicle’s mileage. Weight is a critical factor, as heavier cars typically require more fuel. Similarly, the number of cylinders influences fuel consumption, with higher-cylinder engines generally using more fuel per mile. Acceleration and horsepower also play crucial role, affecting energy efficiency in different driving conditions. Through analysis, i have examined distributions, correlations, and patterns within the data to ensure meaningful insights and reliable predictions.

This report presents detailed findings from the exploratory analysis, highlighting relationships among vehicle attributes and fuel efficiency.

## Background and Overview: Analyzing Fuel Efficiency Trends in Automobiles
In an era of rising fuel costs and increasing environmental concerns, understanding fuel efficiency has become more crucial than ever. This project explores how various vehicle attributes—such as weight, acceleration, horsepower, and engine cylinder configuration—affect the miles a car can travel per gallon of fuel. By leveraging data-driven insights, this study sheds light on key automotive trends, enabling manufacturers, policymakers, and consumers to make more informed decisions about fuel efficiency, cost optimization, and sustainability.

## Summary
In an era of rising fuel costs and increasing environmental concerns, understanding fuel efficiency has become more crucial than ever. This project explores how various vehicle attributes—such as weight, acceleration, horsepower, and engine cylinder configuration—affect the miles a car can travel per gallon of fuel. By leveraging data-driven insights, this study sheds light on key automotive trends, enabling manufacturers, policymakers, and consumers to make more informed decisions about fuel efficiency, cost optimization, and sustainability.

The analysis of the dataset reveals several key insights into the factors influencing automotive fuel efficiency. The following points summarize the main findings:

[<img src="visuals/cylinders.png" alt="Engine Cylinder Configuration" height="1000px">](https://github.com/pravin-nawghare/Automotive-Fuel-Economy-Predictior/blob/main/visuals/cylinders.png)

- 4-cylinder vehicles dominate the market, accounting for 51.3% of total market share. Their widespread popularity is largely due to their superior fuel efficiency, offering an average of 30 miles per gallon (MPG).
- Vehicles equipped with 6-cylinder and 8-cylinder engines focus primarily on performance, providing higher acceleration, power, and speed.
- Lastly, 3-cylinder vehicles exhibit fuel efficiency comparable to 6-cylinder models, yet they remain rare in the market.

[<img src="visuals/Model year and mileage.png" alt="Model Year and Mileage" height="1000px">](https://github.com/pravin-nawghare/Automotive-Fuel-Economy-Predictior/blob/main/visuals/Model%20year%20and%20mileage.png)

- The data shows that in the early 1970s to mid-1970s, cars achieved an average of 25 to 30 miles per gallon (MPG). However, from the late 1970s onward, mileage improved steadily, reaching 40 MPG by the early 1980s—a remarkable increase compared to the previous decade.
- Vehicles from origin 1 consistently showed lower fuel efficiency than those from origin 2 and 3, suggesting differences in manufacturing strategies and technological advancements across regions. 

## Insights deep dive
### Engine Cylinders and Market Preferences
[<img src="visuals/market size by cylinders.png" alt="Engine Cylinder Configuration" height="500px">](https://github.com/pravin-nawghare/Automotive-Fuel-Economy-Predictior/blob/main/visuals/market%20size%20by%20cylinders.png)

The data highlights the influence of engine cylinder configurations on both performance and market demand. Four-cylinder vehicles dominate, holding 51.3% of market share, largely due to their optimal balance between power and fuel efficiency, covering approximately 30 miles per gallon. Meanwhile, six-cylinder models strike a middle ground between performance and mileage, securing 47% of the market share. At the other end of the spectrum, eight-cylinder vehicles—despite their high power and acceleration—rank as the least fuel-efficient, averaging only 15 MPG, making them more appealing for performance-driven consumers rather than those focused on economy.

### Weight Reduction and Its Impact on Mileage
[<img src="visuals/weight vs mileage.png" alt="Weight effects on car's mileage" height="1000px">](https://github.com/pravin-nawghare/Automotive-Fuel-Economy-Predictior/blob/main/visuals/weight%20vs%20mileage.png)

Another remarkable trend observed in this study is the 30% reduction in average vehicle weight over the last decade—from 3,400 kg to 2,400 kg—contributing significantly to improved fuel efficiency. As cars become lighter and more aerodynamically refined, fuel consumption decreases, allowing vehicles to cover greater distances with minimal energy expenditure. This shift in design strategy highlights the industry's commitment to enhancing affordability and sustainability.

### The Role of Car Origin and Brand Performance
[<img src="visuals/most sold car brands.png" alt="Number of cars sold" height="500px">](https://github.com/pravin-nawghare/Automotive-Fuel-Economy-Predictior/blob/main/visuals/most%20sold%20car%20brands.png)

Automotive origin plays a key role in fuel efficiency trends. Cars from certain origins consistently exhibit better mileage compared to others, reinforcing differences in engineering philosophies and fuel economy optimizations across global manufacturers. Leading brands such as Ford and Chevrolet dominate the market, selling the highest number of vehicles, while Plymouth, AMC, Dodge, Toyota, and Volkswagen follow closely behind. Interestingly, while AMC vehicles individually do not claim the top sales position, their combined presence across three models makes AMC the most purchased brand in the market.

## Conclusion

This study offers valuable insights into the factors driving fuel efficiency trends, ranging from model year advancements and engine configurations to market preferences and weight optimizations. As automotive technology continues to evolve, car manufacturers can utilize these findings to shape future fuel-efficient vehicle designs, optimize cost-effectiveness, and promote sustainable transportation solutions. Further analysis could explore predictive modeling to forecast upcoming efficiency trends, helping businesses anticipate consumer demands and engineering advancements in the next generation of automobiles.

## Mileage Prediction


