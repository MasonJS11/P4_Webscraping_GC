#Nina Freeman, Lydia McPhee, Rebeca Mousser, Mason Stewart
#P4 General Conference Webscraping

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt

#feel free to change this however you see fit, but I think this'll be 
#the best/easiest way for the program to flow using custom functions
def scrape_data():
    print("Scraping data...")
    # data scraping person will code and parse with this (Rebeca?)

def show_summaries():
    print("Showing summaries...")
    # last person who is handling the flow/menu will code this and incorporate everyone else's 

def get_talk_links():
    base_url = "https://www.churchofjesuschrist.org"
    url = base_url + "/study/general-conference/2025/10?lang=eng"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for a_tag in soup.select("a[href]"):
        href = a_tag["href"]

        # Must be a conference talk link
        if "/study/general-conference/2025/10/" not in href:
            continue

        # Skip session pages
        if "session" in href.lower():
            continue

        full_url = href if href.startswith("http") else base_url + href

        if full_url not in links:
            links.append(full_url)

    return links


def scrape_basic_info():
    talk_links = get_talk_links()

    talks_data = []

    for url in talk_links:
        print(f"Scraping: {url}")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # ---- TITLE ----
        title_tag = soup.find("p", class_="title")
        title = title_tag.text.strip() if title_tag else ""

        # Skip sustaining talk
        if "sustaining" in title.lower():
            continue

        # ---- SPEAKER ----
        speaker_tag = soup.find(string=lambda text: text and text.strip().startswith("By "))
        speaker = speaker_tag.strip()[3:] if speaker_tag else ""

        # ---- KICKER ----
        kicker_tag = soup.find("p", class_="kicker")
        kicker = kicker_tag.text.strip() if kicker_tag else ""

        talks_data.append({
            "Speaker_Name": speaker,
            "Talk_Name": title,
            "Kicker": kicker
        })

    return talks_data

def main():
    user_input = input(
        "If you want to scrape data, enter 1. "
        "If you want to see summaries of stored data, enter 2. "
        "Enter any other value to exit the program: "
    )

    if user_input == "1":
        scrape_data()
    elif user_input == "2":
        show_summaries()
    else:
        print("Closing the program.")


if __name__ == "__main__":
    main()