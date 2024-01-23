# Line Bot=======================================================================================================
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import MessageAction

# AI=======================================================================================================
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI

# =======================================================================================================
class product(object):
    def __init__(self, brand, name, price, store) -> None:
        self.brand = brand
        self.name = name
        self.price = price
        self.store = store

def split_products_info(result_of_AI):
    for i in ['[', ']']:
        result_of_AI = result_of_AI.replace(i, '')
    result_of_AI = result_of_AI.split('), (')
    result_of_AI[0] = result_of_AI[0].replace('(', '')
    result_of_AI[-1] = result_of_AI[-1].replace(')', '')
    for i in range(len(result_of_AI)):
        result_of_AI[i] = result_of_AI[i].replace('\'', '')
    
    list_result_of_AI = []
    for i in result_of_AI:
        list_result_of_AI.append(i.split(', '))
    
    products = []
    store_set = set()
    for i in list_result_of_AI:
        products.append(product(brand=i[0], name=i[1], price=i[2], store=i[3::]))
        store_set.add(' '.join(i[3::]))
    
    return products, store_set

def merge_products_info(products):
    products_info = ''
    len_products = len(products)
    for i in range(len_products):
        products_info += '品牌: ' + products[i].brand + '\n' + '名稱: ' + products[i].name + '\n' + '售價: ' + products[i].price + '\n' + '店家名稱: ' + products[i].store[0] + '\n' + '店家電話: ' + products[i].store[2] + '\n' + '店家地址: ' + products[i].store[1]
        if i < len_products - 1:
            products_info += '\n\n'
    return products_info
# =======================================================================================================

# 設定AI=======================================================================================================
api_key = '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'

db = SQLDatabase.from_uri('mysql+pymysql://root:548787@127.0.0.1/line2')
llm = OpenAI(api_key=api_key, temperature=0)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, return_direct=True)

# 設定Line Bot=======================================================================================================
app = Flask(__name__)

channel_access_token = 'PFI2FNsELtpjWKU1OA6syYBecn1abKK4cbCkKX4Pr817gnYTlGe691WLkraZI90/DTi9j7Ak+BC2lTlRxzWCDGsCEy4ZOnXObKokcoMiTHuzqhqa8gBuNNR/fqu0wn1qErrTpcSXJZRuINQpYjCNTwdB04t89/1O/w1cDnyilFU='
channel_secret = 'd2f11970855408ed5836395c3904b44e'

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# =======================================================================================================
def computer_purpose(event):
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=MessageAction(label='文書用', text='文書用')),
        QuickReplyButton(action=MessageAction(label='電競用', text='電競用'))
    ])
    message = TextSendMessage(text='請問是文書用還是電競用？', quick_reply=quick_reply)
    line_bot_api.reply_message(event.reply_token, messages=message)

def computer_budget(event):
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=MessageAction(label='一萬元以下', text='一萬元以下')),
        QuickReplyButton(action=MessageAction(label='一萬元到一萬五千元', text='一萬元到一萬五千元')),
        QuickReplyButton(action=MessageAction(label='一萬五千元到兩萬元', text='一萬五千元到兩萬元'))
    ])
    reply_message = TextSendMessage(text='請問您的預算範圍是？', quick_reply=quick_reply)
    line_bot_api.reply_message(event.reply_token, reply_message)

printer_purpose_items = ['商用噴墨印表機', '噴墨印表機', 'HP 繪圖機', 'EPSON 專業繪圖機', '雷射印表機', '點陣印表機']
def printer_purpose(event):
    global printer_purpose_items
    quick_reply = QuickReply(items=[QuickReplyButton(action=MessageAction(label=i, text=i)) for i in printer_purpose_items])
    reply_message = TextSendMessage(text='請問您要什麼類型的印表機？', quick_reply=quick_reply)
    line_bot_api.reply_message(event.reply_token, reply_message)

printer_budget_item = ['10000到15000', '15000到20000', '20000到25000']
def printer_budget(event):
    quick_reply_items = [QuickReplyButton(action=MessageAction(label=i, text=i)) for i in printer_budget_item]
    quick_reply = QuickReply(items=quick_reply_items)
    reply_message = TextSendMessage(text='請問您的預算範圍是？', quick_reply=quick_reply)
    line_bot_api.reply_message(event.reply_token, reply_message)

# =======================================================================================================
user_data = {}
initial_flag = True
computer_flag = False
printer_flag = False

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text
    global initial_flag, computer_flag, printer_flag, db_chain

    if initial_flag == True:
        if '我想組電腦' in user_message:
            computer_flag = True
            initial_flag = False
            user_data[user_id] = {'status': 'initial'}
            computer_purpose(event)

        if '我想買印表機' in user_message:
            printer_flag = True
            initial_flag = False
            user_data[user_id] = {'status': 'initial'}
            printer_purpose(event)

    else:
        if computer_flag == True:
            if user_data[user_id]['status'] == 'initial':
                if user_message == '文書用' or user_message == '電競用':
                    user_data[user_id]['purpose'] = user_message
                    computer_budget(event)
                    user_data[user_id]['status'] = 'budget'

            elif user_data[user_id]['status'] == 'budget':
                user_data[user_id]['budget'] = user_message
                reply_message = '我想要組一台' + user_data[user_id]['purpose'] + '，預算在' + user_data[user_id]['budget'] + '的電腦'   # 之後要給AI吃的問題
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                del user_data[user_id]
                computer_flag = False
                initial_flag = True

        elif printer_flag == True:
            global printer_purpose_items
            if user_data[user_id]['status'] == 'initial':
                if user_message in printer_purpose_items:
                    user_data[user_id]['purpose'] = user_message
                    printer_budget(event)
                    user_data[user_id]['status'] = 'budget'
            
            elif user_data[user_id]['status'] == 'budget':
                user_data[user_id]['budget'] = user_message
                send_messge_to_AI = '資料庫中尋找"產品類別=' + user_data[user_id]['purpose'] + '"，"售價' + user_data[user_id]['budget'] + '"，輸出依照"產品品牌、產品名稱、產品售價、店家名稱、店家地址、店家電話"'
                result_of_AI = db_chain.run(send_messge_to_AI)
                products, store_set = split_products_info(result_of_AI)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=merge_products_info(products)))
                del user_data[user_id]
                computer_flag = False
                initial_flag = True

# =======================================================================================================
if __name__ == "__main__":
    app.run(debug=True)
