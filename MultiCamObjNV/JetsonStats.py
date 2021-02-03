
# Provides various Jetson hardware attribute during the object dectection using Pretrained models



# import statements
from jtop import jtop, JtopException


# Collect the Jetson Statistics after every detection set
def startJsonStats():
        
        with jtop() as jetson:
                while jetson.ok():
                    stats = jetson.stats
                    js_time = stats['time']
                    recTime = str(js_time.date())  + str(js_time.time())
                    #js_uptime= stats['uptime'] 
                    js_jetson_clocks= stats['jetson_clocks']
                    js_nvp_model= stats['nvp model']
                    js_CPU1= stats['CPU1']
                    js_CPU2= stats['CPU2']
                    js_CPU3= stats['CPU3']
                    js_CPU4= stats['CPU4']
                    js_GPU= stats['GPU']
                    js_RAM= stats['RAM']
                    js_EMC= stats['EMC']
                    js_IRAM= stats['IRAM']
                    js_SWAP= stats['SWAP']
                    js_APE= stats['APE']
                    js_NVENC= stats['NVENC']
                    js_NVDEC= stats['NVDEC']
                    js_NVJPG= stats['NVJPG']
                    js_fan= stats['fan']
                    js_Temp_AO= stats['Temp AO']
                    js_Temp_CPU= stats['Temp CPU']
                    js_Temp_GPU= stats['Temp GPU']
                    js_Temp_PLL= stats['Temp PLL']
                    js_Temp_iwlwifi= stats['Temp iwlwifi']
                    js_Temp_thermal= stats['Temp thermal']
                    js_power_cur= stats['power cur']
                    js_power_avg= stats['power avg']
                    jStatvalue =  str(recTime) +  "', '"   + (js_jetson_clocks) +  "', '"  +  str(js_nvp_model) +  "', '"  +  str(js_CPU1)  +  "', '" +  str(js_CPU2)  +  "',  '" + str(js_CPU3)  +  "', '"  + str(js_CPU4) +  "', '"  + str(js_GPU) +  "', '"  +  str(js_Temp_AO) +  "', '"  + str(js_Temp_CPU) +  "',  '"  + str(js_Temp_GPU)  +  "',  '"  +  str(js_Temp_PLL) +  "', '"  +  str(js_Temp_iwlwifi) +  "', '"  + str(js_Temp_thermal)  +  "',  '"  + str(js_power_cur) 
                    return jStatvalue    
