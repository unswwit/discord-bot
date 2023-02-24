import os
import random

import contentful
from dotenv import load_dotenv

load_dotenv()
SPACE_ID = os.getenv('CONTENTFUL_API_SPACE')
ACCESS_TOKEN = os.getenv('CONTENTFUL_API_TOKEN')

client = contentful.Client(SPACE_ID, ACCESS_TOKEN)


def getRandomMarketingPost(category):
    categoryPosts = client.entries(
        {'content_type': 'marketing_archives', 'limit': 1000, 'select': 'fields', 'fields.category[in]': category})

    posts = []
    for post in categoryPosts:
        if post.fields().get('img') != None:
            posts.append(post)

    return random.choice(posts)
