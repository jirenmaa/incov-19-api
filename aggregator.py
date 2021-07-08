import json
import re
from datetime import date

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent()

def month_str_to_num(month):
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return months.index(month) + 1


def aggregate_medicalnewstoday(website):
    response = requests.get(
        website.get("url") + website.get("param"),
        headers={"User-Agent": user_agent.random},
    )
    soup = BeautifulSoup(response.content, "html.parser")
    response.close()

    payloads = []
    # search articles in div, it is like article wrapper
    # each wrapper have many article in it
    for section in soup.find("div", class_="css-stl7tm"):
        try:
            # find all article from article wrapper (div)
            # return as list each recursion, so it's a 2d array
            wrapper = section.findChildren("li", recursive=True)

            # loop each article from wrapper
            # and take the content from article to be processed
            for article in wrapper:
                for content in article:
                    # get the detail link for article
                    # it necessary because, because the upload date
                    # only showed in article detail
                    figure = content.find("figure")
                    images = figure.find("lazy-image")

                    params = figure.find("a").get("href")
                    detail = requests.get(
                        website.get("url") + params,
                        headers={"User-Agent": user_agent.random},
                    )
                    soup = BeautifulSoup(detail.content, "html.parser")
                    detail.close()

                    # match the date string from the article detail
                    # " on (month), (year)"
                    update_text = soup.find("section", class_="css-b1jl63").find_all(
                        "span"
                    )
                    for date_str in update_text:
                        pattern = r"\son\s([a-zA-Z]+)\s(\d+),\s(\d+)"
                        ismatch = re.match(pattern, date_str.text)

                        if ismatch:
                            break

                    # the format date of this string is "m d y"
                    formatted = (
                        date_str.text.lstrip()
                        .replace("Updated ", "")
                        .replace("on ", "")
                        .replace(",", "")
                    )
                    pubdate = list(map(str, formatted.split(" ")))
                    # date method need parameter thats look like
                    # "y m d" and the string format is "m d y"
                    pubdate = date(
                        int(pubdate[2]), month_str_to_num(pubdate[0]), int(pubdate[1])
                    ).strftime("%B %d %Y")

                    payloads.append(
                        {
                            "website": website.get("name"),
                            "url": website.get("url") + params,
                            "title": content.find(
                                attrs={"data-testid": "title-link"}
                            ).text,
                            "subtitle": content.find(
                                attrs={"data-testid": "text-link"}
                            ).text,
                            "upload_at": pubdate,
                            "image": images["src"],
                        },
                    )
        except:
            pass

    return payloads


def aggregate_msn(website):
    response = requests.get(
        website.get("url") + website.get("param"),
        headers={"User-Agent": user_agent.random},
    )
    soup = BeautifulSoup(response.content, "html.parser")
    response.close()

    # remove first article (pop first list)
    # because it is not related to the news
    soup = soup.find("div", class_="rc-container-js").find_all(
        "div", {"class": ["rc-item-js", "rc-item show"]}
    )
    soup.pop(0)

    payloads = []
    for section in soup:
        try:
            # div authorinfo-flexar -> time attr:datetime
            params = section.find("a")["href"]
            images = section.find("img").get("data-src")
            titles = section.find("h3")
            pubdate = None
            new_urls = params
            subtitle = section.find("p")

            if not params.startswith("https://"):
                new_urls = website.get("url") + params
                # request attempt to get the published date
                response = requests.get(
                    website.get("url") + params,
                    headers={"User-Agent": user_agent.random},
                )
                soup = BeautifulSoup(response.content, "html.parser")
                response.close()

                # get datetime string and compile it to our date string format
                get_date = soup.find("div", class_="authorinfo-flexar").find("time")
                pubdate = re.search(r"^[\d-]*", get_date.get("datetime")).group()
                pubdate = list(map(int, pubdate.split("-")))
                pubdate = date(pubdate[0], pubdate[1], pubdate[2]).strftime("%B %d %Y")

            if images:
                images = json.loads(images)["default"]
            else:
                images = section.find("img").get("src")

            if titles:
                titles = titles.text
            else:
                titles = section.find("span", class_="kicker").text

            subtitle = subtitle.text if subtitle else subtitle

            payloads.append(
                {
                    "website": website.get("name"),
                    "url": new_urls,
                    "title": titles,
                    "subtitle": subtitle,
                    "upload_at": pubdate,
                    "image": images,
                },
            )
        except:
            pass

    return payloads


def aggregate_9news(website):
    response = requests.get(
        website.get("url") + website.get("param"),
        headers={"User-Agent": user_agent.random},
    )
    soup = BeautifulSoup(response.content, "html.parser")
    response.close()

    payloads = []
    for section in soup.find("div", class_="feed--latest").find_all("article"):
        try:
            pubdate = section.get("data-display-datetime")
            details = section.find("a", class_="story__media__link")
            title = section.find("span", class_="story__headline__text")
            subtitle = section.find("div", class_="story__abstract")
            image = section.find("img")

            subtitle = subtitle.text if subtitle else subtitle

            payloads.append(
                {
                    "website": website.get("name"),
                    "url": details.get("href"),
                    "title": title.text,
                    "subtitle": subtitle,
                    "upload_at": pubdate,
                    "image": image.get("src"),
                }
            )
        except:
            pass

    return payloads


websites = {
    "medicalnewstoday": {
        "name": "medicalnewstoday",
        "url": "https://www.medicalnewstoday.com",
        "param": "/coronavirus",
    },
    "msn": {
        "name": "msn",
        "url": "https://www.msn.com",
        "param": "/en-us/news/coronavirus/wisconsin",
    },
    "9news": {
        "name": "9news",
        "url": "https://www.9news.com.au",
        "param": "/coronavirus",
    },
}
