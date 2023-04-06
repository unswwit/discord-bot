import os
import random

import contentful
from dotenv import load_dotenv

load_dotenv()
SPACE_ID = os.getenv("CONTENTFUL_API_SPACE")
ACCESS_TOKEN = os.getenv("CONTENTFUL_API_TOKEN")

client = contentful.Client(SPACE_ID, ACCESS_TOKEN)


def getRandomMarketingPost(category):
    categoryPosts = client.entries(
        {
            "content_type": "marketing_archives",
            "limit": 1000,
            "select": "fields",
            "fields.category[in]": category,
        }
    )

    posts = []
    for post in categoryPosts:
        if post.fields().get("img") != None:
            posts.append(post)

    return random.choice(posts)


def getNextUpcomingEvent():
    upcomingEvents = client.entries(
        {"content_type": "upcomingEvents", "limit": 1, "order": "fields.index"}
    )
    return upcomingEvents[0]


def getUpcomingEvents():
    return client.entries({"content_type": "upcomingEvents", "order": "fields.index"})


def getMostRecentEvent():
    pastEvents = client.entries(
        {"content_type": "pastEvents", "limit": 1, "order": "-fields.index"}
    )
    return pastEvents[0]
