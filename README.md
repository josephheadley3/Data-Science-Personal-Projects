# Data Science Personal Projects Portfolio
This webpage serves to summarize the work that I have completed in some of my data science projects such as the processes of data collection and cleaning, data analysis, and data visualizations.


[# Project 1: Anime Ranking Analysis Project Overview](https://github.com/josephheadley3/Data-Science-Personal-Projects/tree/master/Anime_Ranking_Project)
1. Collection: Webscraped myanimelist.net using python with requests, beautifulsoup, and regex modules to gather data on the anime ranked top 100, "middle 100", and bottom 100 into 6 separate .csv files

2. Cleaning: Combined data from .csv files into one dataframe, changed null values and unnecessary cell elements to "Unavailable" where necessary, and imputed for known values that were excluded in collection phase.

3. Feature Engineering: Standardized the categories of the "Age Rating" column and added the columns "Total Minutes" and "Synopsis Length".

4. Data Visualizations: Created the following visualizations to display the distribution of genres, media, and source materials among the anime in the dataset.

<img src="https://github.com/josephheadley3/Data-Science-Personal-Projects/blob/master/Anime_Ranking_Project/Data_Visualizations/anime_genres.png" width="1400" height="800">

<img src="https://github.com/josephheadley3/Data-Science-Personal-Projects/blob/master/Anime_Ranking_Project/Data_Visualizations/anime_media.png" width="800" height="600" class="center">

<img src="https://github.com/josephheadley3/Data-Science-Personal-Projects/blob/master/Anime_Ranking_Project/Data_Visualizations/anime_sources.png" width="800" height="600" class="center">

5. Data Analysis Part 1: Utilized natural language processing and machine learning to predict anime genres, specifically between anime that have "Action" as a primary genre (Genre 1) and anime that have "Dementia" as a primary genre, based on words present in synopses.

6. Data Analysis Part 2: Utilized multivariate linear regression to analyze the relationship between quantitative independent variables of "Number of Episodes", "Number of Members", "Total Minutes", and "Synopsis Length" and the score given to an anime and checked values for different forms of error.
