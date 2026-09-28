import datetime
import secrets
import string
from tabulate import tabulate 
from operator import itemgetter
import sys

#Accomodating Unsuported values 
global error
error="Please enter supported value"
def inputint(prompt):
     while True:
          try:
               var=int(input(prompt))
               break
          except ValueError:
               print(error)
     return var         
def inputfloat(prompt):
     while True:
        try:
            var=float(input(prompt))
            break
        except ValueError:
            print(error)    
     return var                

class Users:

    def __init__(self, name):
        self.name=name
        self.userid= ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        self.cash = 10000
        self.holdings = 0

    def __str__(self):
         return f"""
============ACCOUNT============
USER: {self.name}
USER ID: {self.userid}
CASH: {self.cash}
HOLDINGS: {self.holdings}
"""    

    def Buy(self,price,quantity):
        self.cash = self.cash - (price*quantity)
        self.holdings = self.holdings + quantity

    def Sell(self,price,quantity):
        self.cash = self.cash + (price*quantity)
        self.holdings = self.holdings - quantity 

u1=Users("saketh")


#MAIN MENU
def mainmenu():
    print("")
    print("""MAIN MENU
    1) Buy
    2) Sell
    3) View Order Book
    4) Trade
    5) Trade History
    6) Exit Exchange""")
    a=int(input("Welcome! What would you like to do? "))
    return a
                       

#BUY
buyorders=[[11.2, 12, '20:07:27'], [11.2, 10, '20:07:29'], [23.3, 2, '20:07:29'], [12.6, 30, '20:07:29'], [12.6, 35, '20:07:29']]
def buy():
    global nob
    nob =int(input("how many orders do you want to place? "))

    for i in range (nob) :
        ord=[]
        #taking inputs
        price = inputfloat(f"Enter order {i+1} price: ")
        quantity = inputint(f"Enter order {i+1} quantity: ")
        time = datetime.datetime.now().strftime("%X")
        name=u1.name

        ord.append(price)
        ord.append(quantity)
        ord.append(time)
        ord.append(name)
        buyorders.append(ord)

        u1.Buy(price,quantity)
    print("Your order has been placed!")
    print("")

def buysort():
    buyorders.sort(key=itemgetter(0),reverse= True)
  

# SELL
sellorders=[[11.2, 200, '20:07:29'], [13.1, 150, '20:07:29']]
def sell():
    global nos
    nos = int(input("how many orders do you want to sell? "))

    for i in range (nos) :
        ord=[]
        price = inputfloat(f"Enter order {i+1} price: ")
        quantity = inputint(f"Enter order {i+1} quantity: ")
        time = datetime.datetime.now().strftime("%X")
        name=u1.name
        
        ord.append(price)
        ord.append(quantity)
        ord.append(time)
        ord.append(name)
        sellorders.append(ord)

        u1.Sell(price,quantity)
    print("Your order has been placed!")
    print("")

def sellsort():
    sellorders.sort(key=itemgetter(0))
   


# SHOW ORDER BOOK
def orderbook():
    buysort()
    sellsort()
    global tablerows
    tablerows=[]    
    if len(sellorders)==0:
       for i in range (len(buyorders)):
           tablerows.append(buyorders[i]+["","",""])
    elif len(buyorders)==0:
       for i in range(len(sellorders)):
           tablerows.append(["","",""]+sellorders[i])
    if len(sellorders)!=0 and len(buyorders)!=0:
        if len(sellorders)!=len(buyorders):
            no= min(len(sellorders),len(buyorders)) 
        else: 
            no=len(buyorders) 

        for i in range (no):
            tablerows.append(buyorders[i] + sellorders[i])
        if len(buyorders)>len(sellorders):
            for i in range (len(buyorders)-len(sellorders)):
                tablerows.append(buyorders[no+i])  
        else:
            for i in range(len(sellorders)-len(buyorders)):
                tablerows.append(["","","",]+sellorders[no+i])  
    buyheaders = ["Price", "Quantity"," Time "]  
    sellheaders= ["Price", "Quantity"," Time "]    
    header = buyheaders + sellheaders
    print("""
+=================================+=================================+
|            BUY(BIDS)            |            SELL(ASKS)           |""")
    print(tabulate(tablerows, headers = header, tablefmt= "grid", colalign=("center","center","center","center","center","center")))   

#MATCHING ENGINE
global tradehistory
tradehistory = []
def matching_engine():
    global sellorders
    global buyorders
    sellsort()
    buysort()
    if len(tradehistory)==0:         #traced id
        i=1
    else:
        i=tradehistory[-1][0]+1    

    if len(sellorders)==0 or len(buyorders)==0:  #if any of the orders are zero
        print("TRADE NOT POSSIBLE")
        return
    j=0
    
    while buyorders and sellorders:

        if buyorders[0][0]<sellorders[0][0]:    #not possible at all case
            if j==0:
                print("TRADE NOT POSSIBLE")
                break 
            else:
                break   
        
        if buyorders[0][0]>=sellorders[0][0]:         #trading
            print("")

            if buyorders[0][2]>sellorders[0][2]:    #determining executive price based on time
                expr = sellorders[0][0]
            else:
                expr = buyorders[0][0]    

            print("TRADE SUCCESSFUL")                                #ui
            print(f"BUY: {buyorders[0][1]} @ {buyorders[0][0]}")
            print(f"SELL: {sellorders[0][1]} @ {sellorders[0][0]}")

            temp=buyorders[0][1]-sellorders[0][1]             #determining the quantity of orders remaining
            if temp<0:
                print(f"TRADE: {buyorders[0][1]} @ {expr}")
                exqt=buyorders[0][1]
                del buyorders[0]
                sellorders[0][1] = abs(temp)
                
                
                
            elif temp==0:
                print(f"TRADE: {buyorders[0][1]} @ {expr}")
                exqt=buyorders[0][1]
                del buyorders[0]
                del sellorders[0]
                

            else:
                print(f"TRADE: {sellorders[0][1]} @ {expr} ")
                exqt=sellorders[0][1]
                del sellorders[0]
                buyorders[0][1] = abs(temp) 
            print("")      

            tradehis=[]                            #tradehistory
            tradehis.append(i)
            tradehis.append(expr)
            tradehis.append(exqt)
            tradehis.append(datetime.datetime.now().strftime("%X"))
            tradehistory.append(tradehis)

            i=i+1
            j=j+1

#TRADE HISTORY
def trade_history():
    tablerows=[]
    if len(tradehistory)==0:
        print("NO TRADE HISTORY")
    else:
        print("""
        1) View Trade History
        2) Search Trade History by ORDER ID
        3) Search Trade History by Price
        4) Search Trade History by Quantity
        5) Search Trade History by Time""")
        a = int(input("What do you want to do?"))

        match a:
            case 1:
                tablerows=tradehistory
                tableheaders=["ORDER ID","PRICE","QUANTITY","TIME"]
                print(tabulate(tablerows,headers= tableheaders, tablefmt= "pipe", colalign=("center","center","center","center")))

            case 2:
                id=int(input("ORDER ID: "))
                for i in range (len(tradehistory)):
                    if tradehistory[i][0] == id:
                        tablerows.append(tradehistory[i])
                if len(tablerows)==0:
                        print("NO ORDERS FOUND") 
                else:            
                        tableheaders=["ORDER ID","PRICE","QUANTITY","TIME"]
                        print(tabulate(tablerows,headers= tableheaders, tablefmt= "pipe", colalign=("center","center","center","center")))         

            case 3:
                id=float(input("PRICE: "))
                for i in range (len(tradehistory)):
                    if tradehistory[i][1] == id:
                        tablerows.append(tradehistory[i])
                if len(tablerows)==0:
                        print("NO ORDERS FOUND") 
                else:            
                        tableheaders=["ORDER ID","PRICE","QUANTITY","TIME"]
                        print(tabulate(tablerows,headers= tableheaders, tablefmt= "pipe", colalign=("center","center","center","center")))

            case 4:
                id=int(input("QUANTITY: "))
                for i in range (len(tradehistory)):
                    if tradehistory[i][2] == id:
                        tablerows.append(tradehistory[i])
                if len(tablerows)==0:
                        print("NO ORDERS FOUND") 
                else:            
                        tableheaders=["ORDER ID","PRICE","QUANTITY","TIME"]
                        print(tabulate(tablerows,headers= tableheaders, tablefmt= "pipe", colalign=("center","center","center","center")))

            case 5:
                id=input("TIME: ")
                for i in range (len(tradehistory)):
                    if tradehistory[i][3] == id:
                        tablerows.append(tradehistory[i])
                if len(tablerows)==0:
                        print("NO ORDERS FOUND") 
                else:            
                        tableheaders=["ORDER ID","PRICE","QUANTITY","TIME"]
                        print(tabulate(tablerows,headers= tableheaders, tablefmt= "pipe", colalign=("center","center","center","center")))  

            case _:                    
                  print("Unsupported Value. Please Enter Correct Value")                                                                      

   









