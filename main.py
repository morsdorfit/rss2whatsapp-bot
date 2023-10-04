import feedparser, dateparser, os, os.path, json, requests

from datetime import datetime, timezone


rss_url="*RSSURL*"

author_contains=""

greenapi_instance_id ="greenapiid"
greenapi_api_token ="token"
whatsapp_group_id="whatsappgroupname"

#-------------------------------------------------------------------------------
#       READ / WRITE TIMESTAMP
#-------------------------------------------------------------------------------

def get_last_post_timestamp() -> int:

    current_timestamp = int(datetime.now().timestamp())
    last_post_update = current_timestamp

    current_dir = os.path.dirname(os.path.realpath(__file__)) + "/data.json"

    # read timestamp from file
    try:
        with open(current_dir, "r") as f:
            last_post_update = int(json.loads(f.read())["last_post"])
    except Exception as e:
        pass

    # write timestamp to json file
    with open(current_dir, "w") as f:
        f.write(json.dumps({"last_post": current_timestamp}))

    return last_post_update

#-------------------------------------------------------------------------------
#       loop every article
#-------------------------------------------------------------------------------

# fetch all articles by rss feed
all_articles = feedparser.parse(rss_url)
last_post_timestamp = get_last_post_timestamp()

for article in all_articles["entries"]:

    # fetch article data
    article_name = article["title"]
    article_link = article["link"]
    article_author = article["author"]
    article_timestamp = int(dateparser.parse(article["published"]).timestamp())
    article_post = "New News: " + article_name + " , " + article_link

    # if article is older than last post -> exit process
    if last_post_timestamp > article_timestamp:
        print("I will Stop now")
        break

    # send WhatsApp Message via API
    url = "https://api.green-api.com/waInstance*greenapiinstance*/sendMessage/*TOKEN*"
    payload = {'chatId': whatsapp_group_id, 'message': article_post}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.text.encode('utf8'))
    
