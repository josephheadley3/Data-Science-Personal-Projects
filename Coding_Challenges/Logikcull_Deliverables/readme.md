# Internship Code Challenge

## The Challenge
For this code challenge, you will be adding a field to a CSV file.  The source CSV file is simply a short list of movies from the movielens dataset.  Each row contains 3 fields: movieId, title, and genres.  The `genres` field contains a list of different genres for the movie separated by the | symbol.  What you need to do is the following:

1. Read in the file (movies.csv)
2. Count how many genres each movie has
3. Write a new file with the exact same fields plus 1 additional field called `genre_count`

**Bonus**
1. Print out the average number of genres per movie
2. Print out the most common genre in this dataset
3. Put up the code in your own git repo

Please do this yourself as part of the follow-up interview will be discussing it with Logikcull engineers. We value your time so spend no more than 2 hours on this challenge.  However, if you have extra time within that 2-hour window feel free to go above and beyond.

**Requirements**
* Python script. No jupyter notebooks please
* Use python 3.  Python 2 is dead and it's time to move on
* Include how to run the script in the comments of the script
* The main file should be called `movie_parser.py`
* The resulting csv file should be called `movies_enhanced.csv`

### Sample Input

    movieId,title,genres
    1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
    2,Jumanji (1995),Adventure|Children|Fantasy
    3,Grumpier Old Men (1995),Comedy|Romance

### Sample Output
    movieId,title,genres,genre_count
    1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy,5
    2,Jumanji (1995),Adventure|Children|Fantasy,3
    3,Grumpier Old Men (1995),Comedy|Romance,2

## Hint
Feel free to use any resources you need. One important library you will need in python will be the `csv` module for 
which you can find documentation on [here](https://docs.python.org/3/library/csv.html) 
