
# Plots the results of object detection using Pretrained models
# Uses Sqlite for ploting 



# Import statements 
import sqlite3 as lite
import matplotlib.pyplot as plt
from dateutil import parser
import pandas as pd


#Sqlite connection 
conn = lite.connect('MultiCamDB.db')



# Plot summary 
def plot_ObjDetectCount():
    sqlStmt = 'SELECT Item_Desc, count(*) as ItemCnt FROM OpnCVStats group by Item_Desc '
    sqlCursor = conn.cursor()
    sqlCursor.execute(sqlStmt)
    item_data = sqlCursor.fetchall()

    ItemDesc = []
    ItemCount =[]
    for row in item_data:
            ItemDesc.append(row[0])
            ItemCount.append(row[1])

    sqlCursor.close()
    plt.figure(figsize=(10,6)) 
    plt.bar(ItemDesc, ItemCount, color='red')
    plt.title('Objects Detected Count')
    plt.xlabel('Item Desc',  fontsize=10)
    plt.ylabel('Item Count', fontsize=10)
    plt.savefig('Plots/Items_Detected1.jpeg')
    plt.close()
    #plt.show() 

    # Plot the distribution curve
    plt.figure(figsize=(10,6)) 
    plt.pie(ItemCount, labels=ItemDesc, shadow=True, autopct='%1.1f%%')
    plt.legend(title="Object Detections")
    plt.grid(True)
    plt.savefig('Plots/Items_Detected2.jpeg')
    plt.close()
    ItemDesc.clear()
    ItemCount.clear()


# Plot details 
def plot_ObjDetectCount_Time():
    sqlStmt =  'SELECT count(distinct Item_Desc) as RecCnt, CrtTS, substr(CrtTS, 15,5) as mmSec FROM OpnCVStats Group by CrtTS'
    sqlCursor = conn.cursor()
    sqlCursor.execute(sqlStmt)
    item_data = sqlCursor.fetchall()

    ItemCount =[]
    ItemCrtTS =[]
    ItemMMSEC =[]
    for row in item_data:
            ItemCount.append(row[0])
            ItemCrtTS.append(row[1])
            ItemMMSEC.append(row[2])

    sqlCursor.close()
    plt.figure(figsize=(10,6))   
    plt.plot(ItemMMSEC, ItemCount)
    plt.xlabel("TimeStamp", fontsize=8)
    plt.ylabel("ItemCount", fontsize=8)
    plt.title("Object Detected over Multiple Cycles")
    plt.grid(True)
    plt.savefig('Plots/Items_Detected3.jpeg')
    plt.close()    
    ItemCount.clear()
    ItemCrtTS.clear()
    ItemMMSEC.clear()


    # Jetson Statistics (Temp)
    sqlStmt =  'select CrtTS, substr(CrtTS, 15,5) as mmSec, jtempao, jtempcpu, jtempgpu, jtemppll, jtempthermal, jpowercur from OpnCVStats order by CrtTS' 
    sqlCursor = conn.cursor()
    sqlCursor.execute(sqlStmt)
    item_data = sqlCursor.fetchall()

    ItemCrtTS =[]
    ItemMMSEC=[]
    ItemTempao=[]
    ItemCpu=[]
    ItemGpu=[]
    ItemPll=[]
    ItemThermal=[]
    ItemPowercur=[]
    for row in item_data:
            ItemCrtTS.append(row[0])
            ItemMMSEC.append(row[1])
            ItemTempao.append(row[2])
            ItemCpu.append(row[3])
            ItemGpu.append(row[4])
            ItemPll.append(row[5])
            ItemThermal.append(row[6])
            ItemPowercur.append(row[7])

    sqlCursor.close()
    plt.figure(figsize=(10,6)) 
    plt.plot(ItemMMSEC, ItemTempao, label = "Temp AO")  
    plt.plot(ItemMMSEC, ItemCpu, label = "Temp CPU")  
    plt.plot(ItemMMSEC, ItemGpu, label = "Temp GPU")  
    plt.plot(ItemMMSEC, ItemPll, label = "Temp PLL")  
    plt.plot(ItemMMSEC, ItemThermal, label = "Temp Thermal")  
    plt.plot(ItemMMSEC, ItemPowercur, label = "Temp PowerCur")  
    plt.xlabel("TimeStamp", fontsize=8)
    plt.ylabel("Jetson Temperature", fontsize=8)
    plt.title("Jetson Temp over  Multiple Cycles")
    plt.legend()
    plt.grid(True)
    plt.savefig('Plots/JetsonTemp.jpeg')
    plt.close()
    #plt.show()
    ItemCrtTS.clear()
    ItemMMSEC.clear()


    # Jetson Statistics (CPU, GPU)
    sqlStmt =  'select CrtTS, substr(CrtTS, 15,5) as mmSec, jcpu1, jcpu2, jcpu3, jcpu4, jgpu from OpnCVStats order by CrtTS' 
    sqlCursor = conn.cursor()
    sqlCursor.execute(sqlStmt)
    item_data = sqlCursor.fetchall()

    ItemCrtTS =[]
    ItemMMSEC=[]
    ItemCpu1=[]
    ItemCpu2=[]
    ItemCpu3=[]
    ItemCpu4=[]
    ItemGpu1=[]
    for row in item_data:
            ItemCrtTS.append(row[0])
            ItemMMSEC.append(row[1])
            ItemCpu1.append(row[2])
            ItemCpu2.append(row[3])
            ItemCpu3.append(row[4])
            ItemCpu4.append(row[5])
            ItemGpu1.append(row[6])

    sqlCursor.close()
    plt.figure(figsize=(10,6)) 
    plt.plot(ItemMMSEC, ItemCpu1, label = "CPU1")  
    plt.plot(ItemMMSEC, ItemCpu2, label = "CPU2")  
    plt.plot(ItemMMSEC, ItemCpu3, label = "CPU3")  
    plt.plot(ItemMMSEC, ItemCpu4, label = "CPU4")  
    plt.plot(ItemMMSEC, ItemGpu1, label = "GPU1")  
    plt.xlabel("TimeStamp", fontsize=8)
    plt.ylabel("Jetson Procs", fontsize=8)
    plt.title("Jetson Procs Stats over Multiple Cycles")
    plt.grid(True)
    plt.savefig('Plots/JetsonProcs.jpeg') 
    plt.close()
    ItemCrtTS.clear()
    ItemMMSEC.clear()


# # plot the graphs 
#plot_ObjDetectCount()
#plot_ObjDetectCount_Time()
