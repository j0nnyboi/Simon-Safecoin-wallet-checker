
import requests
from time import gmtime, strftime,sleep
import datetime
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from safecoin.rpc.types import MemcmpOpts
from safecoin.publickey import PublicKey

api_endpoint="https://api.mainnet-beta.safecoin.org"
client = Client(api_endpoint)

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

import pygsheets
import pandas as pd
from pymongo import MongoClient


######################################Section that needs your data#####################################

gc = pygsheets.authorize(service_file='Google-Sheet.json')#.json to access google sheet
sh = gc.open('Balance-Monitor')#Name at top of Google Sheet

dbclient = MongoClient("mongodb+srv://URL")#Url from your account

#####################################################################################################

wks = sh.sheet1
db = dbclient.WalletBalance


def getBal(addr,client):
        try:
                addrBalance = int(client.get_balance(addr)['result']['value'])/1000000000
                print(addr," : ",addrBalance)
                return addrBalance
        except:
                return 0
        
def SafePrice(cg,Safecoinbalance):
        SafePrice = cg.get_price(ids='safe-coin-2', vs_currencies='usd')
        Price = Safecoinbalance * SafePrice['safe-coin-2']['usd']
        print("price : ",Price)
        return Price

Daypre = 99

while True:
        sleep(10)
        #day = strftime("%d", gmtime())#day check
        day = strftime("%H", gmtime())#hour check
        if(day != Daypre):#once an day we check if we need to update
            if(client.is_connected()):
                Daypre = day
                col_list = wks.get_col(1, returnas='cell')
                for addr in col_list:
                        ADDR = addr.value
                        if(ADDR != ''):
                                if(ADDR != "Wallet address"):
                                        addrBalance = getBal(ADDR,client)
                                        cellToChange = wks.cell((addr.row,4))
                                        cellToChange.set_value(str(addrBalance))
                                        Price = SafePrice(cg,addrBalance)
                                        cellPrice = wks.cell((addr.row,5))
                                        cellPrice.set_value(str(Price))
                                        collection = db[ADDR]  
                                        mydict = { "time": datetime.datetime.now(), "Balance": addrBalance, "price": Price }
                                        collection.insert_one(mydict)
                        else:
                                break

                
                        
            else:
                 client = Client(api_endpoint)

