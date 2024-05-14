import os
import random

import contentful
from dotenv import load_dotenv

load_dotenv()
SPACE_ID = os.getenv("CONTENTFUL_API_SPACE")
ACCESS_TOKEN = os.getenv("CONTENTFUL_API_TOKEN")

client = contentful.Client(SPACE_ID, ACCESS_TOKEN)


def get_random_marketing_post(category):
    category_posts = client.entries(
        {
            "content_type": "marketing_archives",
            "limit": 1000,
            "select": "fields",
            "fields.category[in]": category,
        }
    )

    posts = []
    for post in category_posts:
        if post.fields().get("img") != None:
            posts.append(post)

    return random.choice(posts)


def get_next_upcoming_event():
    upcoming_events = client.entries(
        {"content_type": "upcomingEvents", "limit": 1, "order": "fields.index"}
    )
    return upcoming_events[0]


def get_upcoming_events():
    return client.entries({"content_type": "upcomingEvents", "order": "fields.index"})


def get_most_recent_event():
    past_events = client.entries(
        {"content_type": "pastEvents", "limit": 1, "order": "-fields.index"}
    )
    return past_events[0]


def get_media_resources():
    resources = {
        "publication": client.entries(
            {"content_type": "publications", "order": "fields.index"}
        ),
        "blog": client.entries(
            {"content_type": "blogRecommendations", "order": "fields.blogNo"}
        ),
        "podcast": client.entries(
            {"content_type": "podcastEpisode", "order": "fields.link"}
        ),
    }
    return resources
