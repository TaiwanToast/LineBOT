from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI

api_key = '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'

db = SQLDatabase.from_uri('mysql+pymysql://root:548787@127.0.0.1/line2')
llm = OpenAI(api_key=api_key, temperature=0, max_tokens=900)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, return_direct=True)

# a = db_chain.run('資料庫中尋找"產品類別=商用噴墨印表機，售價>25000"，輸出依照"產品品牌、產品名稱、產品售價、店家名稱、店家地址、店家電話"')
# print(a.replace('[(', ''))

# 組電腦
db_chain.run('用資料庫中的資料組一台電競電腦')