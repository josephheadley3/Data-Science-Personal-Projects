"""
The following script is run using the command "python3 movie_parser.py" in the command terminal.
The script does not take any command line input, however the one prerequsite is that this script
should be located in the same directory as the file "movies.csv".
"""

import pandas as pd
import numpy as np

def enhance_df(csv):
    """
    Function that reads in data from csv file, stores that data in a pandas dataframe variable named df,
    adds the genre counts to a new column in df titled 'genres_count' and returns the dataframe with the
    new column now attached.
    """
    df = pd.read_csv(csv)
    df['genres_count'] = df['genres'].apply(lambda x: len(x.split("|")))
    return df

def average_genre_count(df):
    """
    Function that returns the average integer number of genres per movie.
    """
    return round(sum([count for count in df['genres_count']])/len([count for count in df['genres_count']]),0)

def most_common_genre(df):
    """
    Function that initally makes a list comprehension that contains list elements of the 'genres'
    column in the dataframe, uses another list comprehension to add a comma after each list element,
    rejoins this list as one string value and splits the string a list of all the genres from every movie 
    present in the dataframe. 
    
    This result is then converted to a numpy array that is passed through the
    numpy unique() function and passed to the genres and freq to store numpy arrays of every unique genre
    in the dataframe and those genres' frequencies respectively.

    Lastly, the elements in the arrays freq and genres are passed as key-value pairs to a dict variable
    named genre_dict and both the genre with the highest frequency and the highest frequency value are
    returned. 
    """
    genre_list_1 = [genres for genres in df['genres'].apply(lambda x: ",".join(x.split("|")))]
    genre_list_2 = np.array("".join([item + ',' for item in genre_list_1]).split(",")[0:22084])
    genres, freq = np.unique(genre_list_2, return_counts = True)
    genre_dict = dict(zip(freq,genres))
    return genre_dict[max(genre_dict.keys())], max(genre_dict.keys())

def main():
    """
    Main function that runs the enhanced_df() function and writes the enhanced dataframe to a csv file.
    This function also runs the average_genre_count() and the most_common_genre() functions to return
    the answers to the extra credit questions.
    """
    enhance_df("movies.csv").to_csv('movies_enhanced.csv', index = False)

    # Extra Credit Portion
    count = int(average_genre_count(enhance_df("movies.csv")))
    common_genre = most_common_genre(enhance_df("movies.csv"))[0]
    common_genre_count = most_common_genre(enhance_df("movies.csv"))[1]

    print(f"\nThe average (integer) number of genres per movie is {count} genres.")
    print(f"The most common genre in the dataset is {common_genre} with a count of {common_genre_count}.")

if __name__ == '__main__':
    main()