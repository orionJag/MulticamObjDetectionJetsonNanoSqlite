# MulticamObjDetectionJetsonNanoSqlite
Provides computer vision analytics using multiple FOSCAM on Jetson Nano and SQLite.


# Overview
 The project uses several Computer Vison pretrained models to detect specific objects, stores object attributes in SQLite database and takes a picture when predetermined objects are detected.  The FOSCAM cameras also periodical scans the area using Pan-Tilt-Zoom movement. The SQLite database provides detailed analytics of the environment being reported on including the objects being detected, model used and ROI of the objects. In addition, Jetson Nano's stats are also collected to understand the performance behavior of GPU, CPU with various pretrained models.	

# Prerequisites
 # Hardware
    •	NVIDIA Jetson 4GB running JetPack 4.5
    •	SD card 128 GB, EVO 
    •	Cooling fan installed on Jetson Nano device
    •	Power cable with 5V/4A barrel adapter
    •	Camera: FOSCAM FI9821P+V3 of at least 2 units
 
 # Software
    •	Visual studio code with Python extension
    •	SQLite
    •	SQLitebrowser
    •	FOSCAM VMS for calibration of the scan setup 
    •	Jetson Stats for comparison with info collected 

 # Environment Setup
    •	Install Process:  https://developer.nvidia.com/embedded/jetpack
    •	JetPack 4.5 software: https://developer.nvidia.com/jetson-nano-sd-card-image
    •	Setup FOSCAM camera using FOSCAM VMS & provide static IP addresses.
    •	Apply patches to FOSCAM (if any)
            https://www.foscam.com/downloads/firmware_details.html?id=117
    •	Install SQLite 
    	  sudo apt-get install sqlite3
    •	Install SQLitebrowser (optional)
    	  sudo apt-get install sqlitebrowser
    •	Install Jetson Stats
              sudo pip3 install jetson-stats
              sudo reboot now
    •	Install OpenCV Library
    	  sudo apt-get install python3-opencv
              sudo apt-get remove python3-opencv
    The above is required to get cv2 to version '4.1.1'
   
    •	Install Camera Libraries 
    	  sudo pip3 install libpyfoscam
   	          sudo pip3 install nanocamera

•	Install Jetson Inference lib 
      Refer Paul McWhorter’s video tutorial
                https://www.youtube.com/watch?v=5rbOsKCZ-VU&list=PLGs0VKk2DiYxP-ElZ7-QXIERFFPkOuP4_&index=49
          

•	Create a swap file of 12GB
    Disable the config file 
      sudo systemctl disable nvzramconfig
    
    Allocate 12GB in the swap  
      sudo fallocate -l 12G /mnt/12GB.swap    
    Provide access 
      sudo chmod 600 /mnt/12GB.swap
    Make the swap 
      sudo mkswap /mnt/12GB.swap
    Change the fstab file 
      sudo nano /etc/fstab
    Add the following to the bottom of the swap file 
        /mnt/12GB.swap swap swap defaults 0 0 
    Reboot 
      sudo reboot now 
    Display the changes with the cmd after reboot and it should show the 12GB swap
      free -m

•	FOSCAM Setup
	  Using FOSCAM VMS, calibrate each Cameras for PTZ sweep of 180 degree, focusing on the environment for each DNN will be trained on. Also, this overrides the factory defaults of the scan position.
 
# Installed version
    •	Jetpack 4.5 (L4T 32.5.0)
    •	SOC Family tegra210
    •	CUDA: 10.2.89 
    •	OpenCV: 4.1.1 
    •	TensorRT: 7.1.3.0 
    •	cuDNN: 8.0.0.180

# How to run
    •	Once Jetson Nano environment is setup 
    •	Download the repository into Jetson Nano 
    •	Provide appropriate permissions to the folder for storing images and database 
    •	Uncomment CameraStream & myCamX and update with camera credentials and IP address in Main.py
    •	Remove files from the folder named "Plots" inside the project folder 
    •	Create a folder named "Images" inside the project folder to house all Images that are captured    
    •	Run the Main.py
    •	If you need to run different pretrained model, uncomment appropriate models under 
             "pretrained models" and "execute for each pretrained"  


# Conclusion 
    This script can be used to collect object detection of the environment being analyzed for. By placing the multiple 
    cameras in appropriate positions, blind spots can be minimized. The information collected can used for various 
    vision analytics including inputs for Transfer Learning setups. The collected Jetson performance 
    characteristics could be used for proper selection of Jetson Hardware family depending upon the models, Camera 
    and scanning frequencies. 

