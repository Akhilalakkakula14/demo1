import nltk
nltk.download('punkt')

import requests
from newspaper import Article
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
from nltk.tokenize import sent_tokenize


def extract_news_info(url):
    article = Article(url)
    article.download()
    article.parse()

    # Basic title and body extraction
    title = article.title
    text = article.text
    link = url
    image_link = article.top_image

    # Custom summary using first 3 sentences
    sentences = sent_tokenize(text)
    summary = ' '.join(sentences[:3])  # First 3 sentences as summary

    # Try to get publish date
    publish_date = article.publish_date
    if not publish_date:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_date = soup.find('meta', {'property': 'article:published_time'})
            if meta_date and meta_date.get('content'):
                publish_date = datetime.fromisoformat(meta_date['content'][:19])
            else:
                publish_date = datetime.today()
        except:
            publish_date = datetime.today()

    expiry_date = publish_date + timedelta(days=60)
    expiry_date_str = expiry_date.strftime('%Y-%m-%d')
    channel = url.split("//")[1].split("/")[0].replace("www.", "").split(".")[0].title()

    result = {
        "Title": title,
        "Summary": summary,
        "Channel": channel,
        "Link": link,
        "Expiry Date": expiry_date_str,
        "Image Link": image_link
    }

    return json.dumps(result, indent=2)

































# import nltk
# nltk.download('punkt')
# import requests
# from newspaper import Article
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# import json

# def extract_news_info(url):
#     # Step 1: Download and parse the article
#     article = Article(url)
#     article.download()
#     article.parse()
#     article.nlp()  # Enables .summary

#     # Step 2: Extract info
#     title = article.title
#     summary = article.summary
#     link = url

#     # Try to extract the first image
#     image_link = article.top_image

#     # Step 3: Try to fetch article publish date
#     publish_date = article.publish_date
#     if not publish_date:
#         # fallback: scrape manually
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Look for meta tags or common patterns
#         meta_date = soup.find('meta', {'property': 'article:published_time'})
#         if meta_date and meta_date.get('content'):
#             publish_date = meta_date.get('content')
#             publish_date = datetime.fromisoformat(publish_date[:19])
#         else:
#             # If publish date not found, assume today's date
#             publish_date = datetime.today()

#     # Step 4: Calculate Expiry Date (60 days from publish)
#     expiry_date = publish_date + timedelta(days=60)
#     expiry_date_str = expiry_date.strftime('%Y-%m-%d')

#     # Step 5: Extract channel from domain name
#     channel = url.split("//")[1].split("/")[0].replace("www.", "").split(".")[0].title()

#     # Step 6: Format JSON output
#     result = {
#         "Title": title,
#         "Summary": summary,
#         "Channel": channel,
#         "Link": link,
#         "Expiry Date": expiry_date_str,
#         "Image Link": image_link
#     }

#     return json.dumps(result, indent=2)


# # Example usage
# if __name__ == "__main__":
#     news_url = "https://timestech.in/enhancing-embedded-systems-with-automation-using-ci-cd-and-circuit-isolation-techniques/"
#     json_output = extract_news_info(news_url)
#     print(json_output)
