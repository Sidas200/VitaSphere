import pymongo


url = "mongodb+srv://arturo2005sidas:Sidas-200@vitasphere.nvtg2.mongodb.net/?retryWrites=true&w=majority&appName=Vitasphere"
client = pymongo.MongoClient(url)
db = client["VitaSphere"] 
