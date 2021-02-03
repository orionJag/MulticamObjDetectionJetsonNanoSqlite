
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
    plt.bar(ItemDesc, ItemCount, color='red')
    plt.title('Objects Detected Count')
    plt.xlabel('Item Desc')
    plt.ylabel('Item Count')
    plt.savefig('Plots/Items_Detected1.jpeg')
    #plt.show() 

    # Plot the distribution curve
    plt.pie(ItemCount, labels=ItemDesc, shadow=True, autopct='%1.1f%%')
    plt.axis('equal')
    #plt.legend(title="Object Detections")
    plt.grid(True)
    plt.savefig('Plots/Items_Detected2.jpeg')

# Plot details 
def plot_ObjDetectCount_Time():
    sqlStmt =  'SELECT count(distinct Item_Desc) as RecCnt, CrtTS FROM OpnCVStats Group by CrtTS'
    sqlCursor = conn.cursor()
    sqlCursor.execute(sqlStmt)
    item_data = sqlCursor.fetchall()

    ItemCount =[]
    ItemCrtTS =[]
    for row in item_data:
            ItemCount.append(row[0])
            ItemCrtTS.append(row[1])

    sqlCursor.close()
    plt.figure()
    plt.plot(ItemCrtTS, ItemCount)  
    plt.xlabel("TimeStamp")
    plt.ylabel("ItemCount")
    plt.title("Object Detected over Multiple Cycles")
    #plt.legend()
    plt.grid(True)
    plt.savefig('Plots/Items_Detected3.jpeg')    


    # Jetson Statistics (Temp)
    sqlStmt =  'select CrtTS, jtempao, jtempcpu, jtempgpu, jtemppll, jtempthermal, jpowercur from OpnCVStats order by CrtTS' 
    sqlCursor = conn.cursor()
    sqlCursor.execute(sqlStmt)
    item_data = sqlCursor.fetchall()

    ItemCrtTS =[]
    ItemTempao=[]
    ItemCpu=[]
    ItemGpu=[]
    ItemPll=[]
    ItemThermal=[]
    ItemPowercur=[]
    for row in item_data:
            ItemCrtTS.append(row[0])
            ItemTempao.append(row[1])
            ItemCpu.append(row[2])
            ItemGpu.append(row[3])
            ItemPll.append(row[4])
            ItemThermal.append(row[5])
            ItemPowercur.append(row[6])

    sqlCursor.close()
    plt.figure()
    plt.plot(ItemCrtTS, ItemTempao, label = "Temp AO")  
    plt.plot(ItemCrtTS, ItemCpu, label = "Temp CPU")  
    plt.plot(ItemCrtTS, ItemGpu, label = "Temp GPU")  
    plt.plot(ItemCrtTS, ItemPll, label = "Temp PLL")  
    plt.plot(ItemCrtTS, ItemThermal, label = "Temp Thermal")  
    plt.plot(ItemCrtTS, ItemPowercur, label = "Temp PowerCur")  
    plt.xlabel("TimeStamp")
    plt.ylabel("Jetson Temperature")
    plt.title("Jetson Temp over  Multiple Cycles")
    plt.legend()
    plt.grid(True)
    plt.savefig('Plots/JetsonTemp.jpeg')
    #plt.show()

    # Jetson Statistics (CPU, GPU)
    sqlStmt =  'select CrtTS, jcpu1, jcpu2, jcpu3, jcpu4, jgpu from OpnCVStats order by CrtTS' 
    sqlCursor = conn.cursor()
    sqlCursor.execute(sqlStmt)
    item_data = sqlCursor.fetchall()

    ItemCrtTS =[]
    ItemCpu1=[]
    ItemCpu2=[]
    ItemCpu3=[]
    ItemCpu4=[]
    ItemGpu1=[]
    for row in item_data:
            ItemCrtTS.append(row[0])
            ItemCpu1.append(row[1])
            ItemCpu2.append(row[2])
            ItemCpu3.append(row[3])
            ItemCpu4.append(row[4])
            ItemGpu1.append(row[5])


    sqlCursor.close()
    plt.figure()
    plt.plot(ItemCrtTS, ItemCpu1, label = "CPU1")  
    plt.plot(ItemCrtTS, ItemCpu2, label = "CPU2")  
    plt.plot(ItemCrtTS, ItemCpu3, label = "CPU3")  
    plt.plot(ItemCrtTS, ItemCpu4, label = "CPU4")  
    plt.plot(ItemCrtTS, ItemGpu1, label = "GPU1")  
    plt.xlabel("TimeStamp")
    plt.ylabel("Jetson Procs")
    plt.title("Jetson Procs Stats over Multiple Cycles")
    plt.axis()
    plt.legend()
    plt.grid(True)
    plt.savefig('Plots/JetsonProcs.jpeg') 


# # plot the graphs 
#plot_ObjDetectCount()
#plot_ObjDetectCount_Time()
