
import requests
from time import gmtime, strftime,sleep
import datetime
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from safecoin.rpc.types import MemcmpOpts
from safecoin.publickey import PublicKey

api_endpoint="https://api.mainnet-beta.safecoin.org"
client = Client(api_endpoint)

from openpyxl import Workbook,load_workbook
from openpyxl.utils import get_column_letter


def getBal(addr,client):
        addrBalance = int(client.get_balance(addr)['result']['value'])/1000000000
        print(addr," : ",addrBalance)
        return addrBalance
        


Daypre = 99

while True:
        sleep(10)
        day = strftime("%d", gmtime())
        if(day != Daypre):#once an day we check if we need to update
            Daypre = day
            if(client.is_connected()): 
                wb = load_workbook('Wallet_balances.xlsx')
                ws = wb.active
                
            
                for row1 in ws["1"]:
                    ROW1 = row1
                colDate = "%s1" % (get_column_letter(ROW1.column + 1))
                #print(colDate)
                ws[colDate] = datetime.datetime.now()
                #ws[colDate].number_format
                           
                colA = ws['A']      
                for addr in colA:
                    #print(addr.value)
                    if(addr.value != "Wallet address"):
                        addrBalance = getBal(addr.value,client)
                        colval = "%s%s" % (get_column_letter(ROW1.column + 1),addr.row)
                        ws[colval] = addrBalance

                wb.save('Wallet_balances.xlsx')
                        
            else:
                 client = Client(api_endpoint)

                
                    
                    

                
                    
                                        
                        
                        
                        

