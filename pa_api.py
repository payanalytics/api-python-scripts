import requests
import json


def pa_get(url: str, token: str) -> dict | list:
    response = requests.get(
        url,
        headers={
            "Authorization": "Token %s" % (token,),
            "Accept": "application/json",
        },
    )
    response.raise_for_status()

    return response.json()


def pa_delete(url: str, token: str) -> None:
    response = requests.delete(
        url,
        headers={
            "Authorization": "Token %s" % (token,),
            "Accept": "application/json",
        },
    )
    response.raise_for_status()


def pa_post(url: str, token: str, data: list | dict) -> list | dict:
    raw_json = json.dumps(data)
    response = requests.post(
        url,
        data=raw_json,
        headers={
            "Authorization": "Token %s" % (token,),
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    if response.status_code > 399:
        print(response.content)

    response.raise_for_status()

    return response.json()
