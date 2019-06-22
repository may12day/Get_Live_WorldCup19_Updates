"""
@author: Mayank Devnani
Description:This script will download the homepage of https://demo.entitysport.com/ and scrap the live updates whenever 
there is a Four, Six and fall of Wicket. 
"""

# Importing necessary libraries
from bs4 import BeautifulSoup
from plyer import notification
import requests
import time


prev_ball_status = 0


def sys_notification(title, commentary, current_score):
    """ To display the notification on system """
    notification.notify(
        title=title, message=commentary + " " + current_score, timeout=30
    )


def get_html(request_URL="https://demo.entitysport.com/"):
    """ Get the HTML structure of a webpage with headers and parse using html5lib library """

    # Attaching headers as we are a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    html = requests.get(request_URL, headers=headers)
    soup = BeautifulSoup(html.content, "html5lib")
    return soup


def get_match_URL(soup):
    """ Get the URL of match which is going on. """

    match_URL = soup.find("a", attrs={"class": "match-status-3"})["href"]
    return match_URL


def get_live_updates(live_match_URL):
    """ Scrapping the live updates from webpage """

    print("Fetching the live updates...")
    global prev_ball_status
    
    while True:

        # Make it sleep for 5 seconds
        # Zzzzz.....
        time.sleep(5)

        # Getting the URL of live match
        soup = get_html(live_match_URL)
        
        # Getting the right team name which is currently batting
        c = soup.find("div", attrs={"class": "teambScore"}).text.strip()
        if c == '':
            team_name = "teamaScore"
        else:
            team_name = "teambScore"

        # Getting the match title
        title = soup.find("h1", attrs={"id": "heading"}).text.split(",")[0]

        # Getting the update from last ball
        last_ball = soup.find("div", attrs={"class": "live-info4"}).span.text.strip()

        # Getting the current score
        current_score = soup.find("div", attrs={"class": team_name}).text.strip()

        # Current ball of the over
        current_ball_status = soup.find("div", attrs={"class": "ovb"}).text.strip()

        if current_ball_status != prev_ball_status:

            # Fall of Wicket
            if last_ball == "W":
                last_wicket_commentary = soup.find(
                    "div", attrs={"class": "comment-wicket"})
                last_wicket_commentary = last_wicket_commentary.find(
                    "div", attrs={"class": "text"}
                ).text.strip()
                print(
                    "Last Wicket Commentary: "+ last_wicket_commentary + " " + current_score
                )
                sys_notification(title, last_wicket_commentary, current_score)
                time.sleep(60)

            # If it is a Four or Six
            elif (last_ball == "4") or (last_ball == "6"):
                last_hit_commentary = soup.find("div", attrs={"class": "comment-ball"})
                last_hit_commentary = last_hit_commentary.find(
                    "div", attrs={"class": "text"}
                ).text.strip()
                print(
                    "Last Hit Commentary: " + last_hit_commentary + " " + current_score
                )
                sys_notification(title, last_hit_commentary, current_score)
            prev_ball_status = current_ball_status


if __name__ == "__main__":
    """ main function """
    soup = get_html()
    live_match_URL = get_match_URL(soup)
    get_live_updates(live_match_URL)
