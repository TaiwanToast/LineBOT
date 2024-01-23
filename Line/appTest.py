from linebot import LineBotApi, WebhookHandler
# 載入對應的函式庫
from linebot.models import FlexSendMessage, BubbleContainer, ImageComponent
import json
line_bot_api = LineBotApi('4l6IXH5agbRF9G222NzLJKsHVEHBxyCk9utqAFUYxtr0+ESnEYso1uD2zI0wF38GzVPAwpnozjvWuY314U9FskP9gd4khbSPPfhJxxxi4opXkV1CxjuEVlXuOVq8/6kzyx7Yrk93eFYiBPY+jUiRSAdB04t89/1O/w1cDnyilFU=')
# 剛剛 Flex Message 的 JSON 檔案就貼在下方

a = FlexSendMessage(
        alt_text='hello',
        contents={
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Hello, this is a card with location information!",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "text",
                "text": "You can customize this card as per your requirements."
            }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "View Location",
                    "uri": "https://www.google.com/maps/place/900%E5%B1%8F%E6%9D%B1%E7%B8%A3%E5%B1%8F%E6%9D%B1%E5%B8%82%E6%A6%AE%E7%B8%BD%E6%9D%B1%E8%B7%AF1%E8%99%9F"
                }
            }
        ]
    }
})

line_bot_api.push_message('Ueb5880469fb1b618c5a24640525c0b4f', a)