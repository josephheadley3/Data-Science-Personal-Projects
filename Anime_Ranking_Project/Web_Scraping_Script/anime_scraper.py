"""
This python program is designed to create of dataset with information on anime rated on the website
myanimelist.net.

The dataset is comprised of the top 100, middle 100, and bottom 100 rated anime,
with information such as each series episode length, aire dates, a series synopsis, etc.

The purpose of creating such a dataset is to analyze it with various data science techniques
such as machine learning, natural language processing, and deep learning to name a few.

These analyses serve as a means of gaining insight into understanding what makes certain anime
popular or not as well as providing an opportunity to improve one's abilities in the techniques
mentioned above.
"""

# Imports

import csv
import re
from bs4 import BeautifulSoup as bs
import requests

# Instance variables

names = []
ranks = []
scores = []
media = []
ep_nums = []
ep_lens = []
start_dates = []
end_dates = []
seasons = []
materials = []
age_ratings = []
mem_nums = []
urls = []
synopses = []
gnrs = []
genre_1 = []
genre_2 = []
genre_3 = []
genre_4 = []
genre_5 = []
genre_6 = []
genre_7 = []
genre_8 = []

""" def reset():
    names.clear()
    ranks.clear()
    scores.clear()
    media.clear()
    ep_nums.clear()
    ep_lens.clear()
    start_dates.clear()
    end_dates.clear()
    seasons.clear()
    materials.clear()
    age_ratings.clear()
    mem_nums.clear()
    urls.clear()
    synopses.clear()
    gnrs.clear()
    genre_1.clear()
    genre_2.clear()
    genre_3.clear()
    genre_4.clear()
    genre_5.clear()
    genre_6.clear()
    genre_7.clear()
    genre_8.clear() """

# All Purpose Functions

def strip_fat(listobj):
    """
    This function is used to remove some of the unwanted elements in the web-scraped summaries
    of each anime such as random extra spaces and the ending remark in most summaries that
    credits some sort of source for the summary.
    """
    temp = listobj[:]
    for val in temp:
        if str(val) == '':
            listobj.remove(val)
    if "(Source:" in listobj:
        listobj.pop()
        listobj.pop()
    elif "[Written" in listobj:
        listobj.pop()
        listobj.pop()
        listobj.pop()
        listobj.pop()
    return listobj

def add_genres(gnrs):
    """
    This function populates 8 separate lists (columns) with one of two values, a string for the
    type of genre an anime falls under or a null value. As not every anime fits every genre,
    it becomes necessary to account for each instance in which an anime fits a specify set of
    genres.
    """
    if len(gnrs) == 1:
        genre_1.append(gnrs[0])
        genre_2.append(None)
        genre_3.append(None)
        genre_4.append(None)
        genre_5.append(None)
        genre_6.append(None)
        genre_7.append(None)
        genre_8.append(None)

    if len(gnrs) == 2:
        genre_1.append(gnrs[0])
        genre_2.append(gnrs[1])
        genre_3.append(None)
        genre_4.append(None)
        genre_5.append(None)
        genre_6.append(None)
        genre_7.append(None)
        genre_8.append(None)

    if len(gnrs) == 3:
        genre_1.append(gnrs[0])
        genre_2.append(gnrs[1])
        genre_3.append(gnrs[2])
        genre_4.append(None)
        genre_5.append(None)
        genre_6.append(None)
        genre_7.append(None)
        genre_8.append(None)

    if len(gnrs) == 4:
        genre_1.append(gnrs[0])
        genre_2.append(gnrs[1])
        genre_3.append(gnrs[2])
        genre_4.append(gnrs[3])
        genre_5.append(None)
        genre_6.append(None)
        genre_7.append(None)
        genre_8.append(None)

    if len(gnrs) == 5:
        genre_1.append(gnrs[0])
        genre_2.append(gnrs[1])
        genre_3.append(gnrs[2])
        genre_4.append(gnrs[3])
        genre_5.append(gnrs[4])
        genre_6.append(None)
        genre_7.append(None)
        genre_8.append(None)

    if len(gnrs) == 6:
        genre_1.append(gnrs[0])
        genre_2.append(gnrs[1])
        genre_3.append(gnrs[2])
        genre_4.append(gnrs[3])
        genre_5.append(gnrs[4])
        genre_6.append(gnrs[5])
        genre_7.append(None)
        genre_8.append(None)

    if len(gnrs) == 7:
        genre_1.append(gnrs[0])
        genre_2.append(gnrs[1])
        genre_3.append(gnrs[2])
        genre_4.append(gnrs[3])
        genre_5.append(gnrs[4])
        genre_6.append(gnrs[5])
        genre_7.append(gnrs[6])
        genre_8.append(None)

    if len(gnrs) >= 8:
        genre_1.append(gnrs[0])
        genre_2.append(gnrs[1])
        genre_3.append(gnrs[2])
        genre_4.append(gnrs[3])
        genre_5.append(gnrs[4])
        genre_6.append(gnrs[5])
        genre_7.append(gnrs[6])
        genre_8.append(gnrs[7])

# Core function

def animescrape(source):
    """
    This function is the core function of this python web scraping file
    as it scrapes myanimelist.net for the anime in its rankings page, looping through
    all the desired information, storing them in lists and constructing a csv file
    based on that information.
    """
    # Core functionality
    # Relies heavily on BeautifulSoup web scraping and searching through regular expressions

    # reset()

    csv_file = open("ranked_anime.csv", "a")
    csv_writer = csv.writer(csv_file)

    soup = bs(source, 'lxml')

    ## Loop that scrapes anime name and anime url link
    for match in soup.find_all('div', class_='di-ib clearfix'):
        names.append(match.a.text)
        urls.append(match.a['href'])

    ## Loop that scrapes anime score on myanimelist
    for match in soup.find_all('div', class_='js-top-ranking-score-col di-ib al'):
        scores.append(match.span.text)

    ## Loop that scrapes anime's media, number of episodes, starting aire date, ending aire date,
    ## and its number of members on myanimelist
    for match in soup.find_all('div', class_='information di-ib mt4'):
        info = str(match.text).split('\n')
        info = [i.strip() for i in info]

        medium = re.search(r'\w+', info[1]).group(0)
        start_date = info[2].split(" - ")[0]
        mem_num = re.search(r'\d+', "".join(info[3].split(','))).group(0)

        try:
            ep_num = re.search(r'\d+', info[1]).group(0)
        except Exception:
            ep_num = 0

        try:
            end_date = info[2].split(" - ")[1]
        except Exception:
            end_date = "N/A"

        media.append(medium)
        ep_nums.append(ep_num)
        start_dates.append(start_date)
        end_dates.append(end_date)
        mem_nums.append(mem_num)

    ## Loop that scrapes anime's synopsis, genres, ranks,
    ## premier season, episode length, age rating, and source material
    for url in urls:
        newsoup = bs(requests.get(url).text, 'lxml')

        summary = str(newsoup.find('div', class_='js-scrollfix-bottom-rel').table.p.text)
        synopsis = " ".join(strip_fat(re.split(r'\s', summary)))
        synopses.append(synopsis)

        for genre in newsoup.find_all('span', itemprop="genre"):
            gnrs.append(genre.text)

        add_genres(gnrs)
        gnrs.clear()

        for rank in newsoup.find_all('span', class_="numbers ranked"):
            ranks.append(rank.text.split("#")[1])

        foundseason = False
        foundeplen = False
        foundagerat = False
        foundmaterial = False
        for item in newsoup.find_all('td', class_='borderClass'):
            season = re.search(r"(Spring|Summer|Fall|Winter).\d{4}", item.text)
            ep_len = re.search(r"(\d{1,2})\s(min|hr|sec)\.\s?([a-z0-9]+)?\s?(\w+)?\.?", item.text)
            age_rating = re.search(r"\s{3}(R|PG|G)(\s|\+|-)+([0-9+]{2,3})?", item.text)
            material = re.search(r"\s{3}(Manga|Visual novel|Game|Original|Novel|Light novel|Web manga|Other|Picture book|Music|Card game|4-koma manga|Book)\s{3}", item.text)

            if season is not None:
                seasons.append(season.group(1))
                foundseason = True

            if ep_len is not None:
                ep_lens.append(ep_len.group(0))
                foundeplen = True

            if age_rating is not None:
                age_ratings.append(age_rating.group(0))
                foundagerat = True

            if material is not None:
                materials.append(material.group(1))
                foundmaterial = True

        if not foundseason:
            seasons.append("N/A")
        if not foundeplen:
            ep_lens.append("N/A")
        if not foundagerat:
            age_ratings.append("N/A")
        if not foundmaterial:
            materials.append("N/A")

    for i in range(0, len(names)):
        csv_writer.writerow([names[i], ranks[i], scores[i], media[i], ep_nums[i], ep_lens[i],
                             start_dates[i], end_dates[i], seasons[i], materials[i],
                             age_ratings[i], mem_nums[i], urls[i], synopses[i], genre_1[i],
                             genre_2[i], genre_3[i], genre_4[i], genre_5[i], genre_6[i],
                             genre_7[i], genre_8[i]])
    csv_file.close()

def top50():
    """
    This function defines the source variable argument for the animescrape function
    as the webpage that lists the anime ranked in the top 50 of myanimelist and passes
    that argument to the animescrape function to construct the corresponding csv file.
    """
    animescrape(requests.get("http://myanimelist.net/topanime.php").text)

def top100():
    """
    This function defines the source variable argument for the animescrape function
    as the webpage that lists the anime ranked in the top 100 of myanimelist and passes
    that argument to the animescrape function to construct the corresponding csv file.
    """
    animescrape(requests.get("https://myanimelist.net/topanime.php?limit=50").text)

def mid50():
    """
    This function defines the source variable argument for the animescrape function
    as the webpage that lists the anime ranked in the "middle 50" of myanimelist and passes
    that argument to the animescrape function to construct the corresponding csv file.
    """
    animescrape(requests.get("https://myanimelist.net/topanime.php?limit=5300").text)

def mid100():
    """
    This function defines the source variable argument for the animescrape function
    as the webpage that lists the anime ranked in the "middle 100" of myanimelist and passes
    that argument to the animescrape function to construct the corresponding csv file.
    """
    animescrape(requests.get("https://myanimelist.net/topanime.php?limit=5350").text)

def bottom100():
    """
    This function defines the source variable argument for the animescrape function
    as the webpage that lists the anime ranked in the "bottom 100" of myanimelist and passes
    that argument to the animescrape function to construct the corresponding csv file.
    """
    animescrape(requests.get("https://myanimelist.net/topanime.php?limit=10700").text)

def bottom50():
    """
    This function defines the source variable argument for the animescrape function
    as the webpage that lists the anime ranked in the "bottom 50" of myanimelist and passes
    that argument to the animescrape function to construct the corresponding csv file.
    """
    animescrape(requests.get("https://myanimelist.net/topanime.php?limit=10750").text)

def main():
    """
    This function runs the previously defined functions to scrape myanimelist.net for
    information on a broad range of ranked anime to compile into a single csv file.
    """

    # Csv Initialization & Closure
    csv_file = open("ranked_anime.csv", "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Title", "Rank", "Score", "Medium", "Number of Episodes",
                         "Episode Length", "Start Date", "End Date", "Premier Season",
                         "Source Material", "Age Rating", "Number of Members", "URLS", "Synopses",
                         "Genre 1", "Genre 2", "Genre 3", "Genre 4", "Genre 5", "Genre 6",
                         "Genre 7", "Genre 8"])
    csv_file.close()

    # top50()
    # top100()
    # mid50()
    # mid100()
    # bottom100()
    bottom50()


if __name__ == '__main__':
    main()
