from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
import requests
import json
import urllib.request
import urllib.parse

#LINEでメッセージを送るためのキー
LINE_ACSESS_KEY = "LINE_ACSESS_KEY"
#送信先のLINEのID
LINE_USER_KEY = "LINE_USER_KEY"

def push_info(json_input, context):
    line_bot_api = LineBotApi(LINE_ACSESS_KEY)
    text_message = get_text_message()
    try:
        line_bot_api.push_message(LINE_USER_KEY, TextSendMessage(text=text_message))
    except LineBotApiError as e:
        print(e)

def get_text_message():
    review_url = "https://itunes.apple.com/jp/rss/customerreviews/id=アプリID/json"
    headers = {
        "Content-Type":"application/json",
    }
    response_obj = urllib.request.Request(review_url, headers=headers)
    # tryでエラーハンドリング
    try:
       with urllib.request.urlopen(response_obj) as response:
        response_body = response.read().decode("utf-8")
        result_objs = json.loads(response_body)
        result_obj = result_objs["feed"]
        review_count = len(result_obj["entry"])
        messages = "レビュー数は" + str(review_count) + "件です"
        return messages
    except urllib.error.HTTPError as e:
        if e.code >= 400:
            messages = e.reason
            return messages
        else:
            return e
