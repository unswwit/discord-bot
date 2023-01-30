import os
import random

import contentful
from dotenv import load_dotenv

load_dotenv()
SPACE_ID = os.getenv('CONTENTFUL_API_SPACE')
ACCESS_TOKEN = os.getenv('CONTENTFUL_API_TOKEN')

client = contentful.Client(SPACE_ID, ACCESS_TOKEN)


def getRandomMarketingPost(category):
    marketingArchives = client.entries(
        {'content_type': 'marketing_archives', 'limit': 1000})

    posts = []
    for post in marketingArchives:
        if category in post.fields().get('category') and post.fields().get('img') != None:
            posts.append(post)

    post = random.choice(posts)
    postLabel = post.fields().get('label').replace(' ', '-') + '.png'
    postLink = 'https:' + post.fields().get('img').url()

    return {
        'label': postLabel,
        'link': postLink,
    }
