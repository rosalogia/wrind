from bs4 import BeautifulSoup
import requests
import csv

URL = "https://1000mostcommonwords.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all(
    "span"
)  # 1000commonwords stores its links containing language names in spans

# Stores all the languages on this website
language_names = []

# This loop parses out the various languages on 1000commonwords
for result in results:
    """Iterates through spans, which contain language names, and parses out name"""
    if result.find("a") is None:
        continue

    try:
        language_name = str(result.find("a").contents[0])
    except IndexError:
        continue

    try:
        language_name = str(result.find("a").contents[0])
        language_name = language_name.split(">", 1)[1].strip()
        language_names.append(language_name.split("<", 1)[0].strip())
    except IndexError:
        try:
            language_name = str(result.find("a").contents[0])
            language_name = language_name.split("(", 1)[0].strip()
            language_names.append(language_name)
        except IndexError:
            language_names.append(language_name.strip())


# This loop iterates through every sub-page of 1000commonwords, parsing out the the foreign/translation words and inputting them into a CSV
for language_name in language_names:
    try:
        file_name = "language_decks/" + language_name.lower() + ".csv"
        langURL = (
            "https://1000mostcommonwords.com/1000-most-common-"
            + language_name.lower()
            + "-words/"
        )
        lang_page = requests.get(langURL)
        soup = BeautifulSoup(lang_page.content, "html.parser")
        table_of_words = soup.find("table")
        with open(file_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in table_of_words.find_all("tr")[1:]:
                col = row.find_all("td")
                try:
                    foreign_word = col[1].contents[0]
                    english_translation = col[2].contents[0]
                    writer.writerow([foreign_word, english_translation])
                except IndexError:
                    continue
    except AttributeError:
        continue
