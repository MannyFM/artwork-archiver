import json


def normalize_album(data: json) -> tuple:
    res = (
        data['artists'][0]['name'],
        data['name'],
        data['images'][0]['url']
        # (image['url'] for image in data['images']),
    )
    return res
