import requests
from pydantic import BaseModel, HttpUrl, ValidationError
from modules.crawel import HEADERS

class URLInput(BaseModel):
    url: HttpUrl


def validate_url(url: str) -> bool:
    """
    Validate URL format and basic reachability.
    """
    try:
        validated = URLInput(url=url)

        response = requests.get(
            str(validated.url),
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )

        
        if response.text and len(response.text) > 500:
            return True

        return False

    except (ValidationError, requests.RequestException):
        return False