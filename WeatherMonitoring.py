import selenium
#load selenium module into python program
from selenium import webdriver
#absolute import of the "webdriver" sub-package from the selenium package 
from selenium.webdriver.common.by import By
#relative import of the "By" sub-package from the selenium.webdriver.common.by package
from selenium.webdriver.firefox.options import Options as FirefoxOptions
#changing the variable name of "Options" to "FirefoxOptions" where "Options" sub-package is 
#obtained from relative import of "selenium.webdriver.firefox.options"
import time
#import time module into python program, available from python libraries
#used to represent time in code, eg to make system sleep
import os
#import os module (miscllaneous operating system interfaces), available from python libraries
#allow portable way of using operating system dependent functionality, eg clear screen in terminal
import winsound
#import winsound module, avalable from python libraries
#allow the code to play basic sounds

# import serial
#imports the PySerial package
#facilitates the communciation between the python program and the arduino
# ser = serial.Serial('COM3', 9600)
#initialising the serial communication port, and setting the communication baud rate

def init_webdriver(headless=True):
#defining the function init_webdriver()
#purpose is to initialise webdriver by calling webdriver.Firefox()
#to also enable ,browser to open and run in background
    if headless == True:    
        options = FirefoxOptions()
        options.add_argument("--headless") 
        #argument parsing to edit selenium's webdriver options, enabling headless browser
        return webdriver.Firefox(options=options)
        #initialise webdriver with headless browser
    else:
        return webdriver.Firefox()
        #initialise webdriver normally, without headless browser

def getData(changeWeb):
    if (changeWeb == 0): #obtain weather conditions
        #company location
        rawRainDataBSH = driver.execute_script("return nowcasts[2]")
        #execute_script() method synchronously executes JavaScriptin the webpage/window
        #nowcast[] is an array in the webpage's JavaScript that contains the following
        #1. area name (name of the location)
        #2. icon (weather status are represented with an icon on the webpage)
        #3. latitude
        #4. longitude
        #5. weather (weather condition eg cloudy, showers, light rain etc)
        #return nowcasts[x] will retrieve x's array of data back to the program and store in a variable
        stringData = str(rawRainDataBSH)
        #change retrieved data's datatype to string so that the data's character positions can be determined
        #after changing to datatype to string, data can be modified to be more presentable 
        secondLastCharacterPos = len(stringData) - 1
        #getting position of second last character of the string data
        #this will be the position of the second last character, which is the apostrophe '  
        processedBSHData = " " + stringData[1:secondLastCharacterPos].replace("'", '')
        #adding a space infront of the whole string to make the data seem more organised in terminal
        #using list slicing to exclude out the first and last character, which are curly brackets "{" and "}"
        #.replace("'", '') removes all the apostrophe characters in the string 

        #the locations below are north from company location
        #North: Ang Mo Kio
        rawRainDataAMK = driver.execute_script("return nowcasts[0]")
        RainDataAMK = dataProcessing(rawRainDataAMK)

        #the locations below are east from company location
        #East: Serangoon
        rawRainDataSRG = driver.execute_script("return nowcasts[35]") 
        RainDataSRG = dataProcessing(rawRainDataSRG)

        #the locations below are south of company location
        #South: Toa Payoh, Novena
        rawRainDataTPY = driver.execute_script("return nowcasts[41]")  
        RainDataTPY = dataProcessing(rawRainDataTPY)

        rawRainDataNVA = driver.execute_script("return nowcasts[23]")
        RainDataNVA = dataProcessing(rawRainDataNVA)

        #the locations below are west of company location
        #West: Central Water Catchment, Bukit Timah, Bukit Panjang
        rawRainDataCWC = driver.execute_script("return nowcasts[8]")
        RainDataCWC = dataProcessing(rawRainDataCWC) 

        rawRainDataBKT = driver.execute_script("return nowcasts[6]")
        RainDataBKT = dataProcessing(rawRainDataBKT)

        rawRainDataBKP = driver.execute_script("return nowcasts[7]")
        RainDataBKP = dataProcessing(rawRainDataBKP)

        return processedBSHData, RainDataAMK, RainDataSRG, RainDataTPY, RainDataNVA, RainDataCWC, RainDataBKT, RainDataBKP

    if (changeWeb == 1): #obtain wind directions
        #initialise the 4 variables to equal to 0
        #this means that by default, wind direction is not towards the main location
        NWind = 0
        #Nwind variable means wind from north side
        #NWind = 0 means that wind from the north location is not directed towards the main location
        EWind = 0
        #Ewind variable means wind from east side
        SWind = 0
        #Swind variable means wind from south side
        WWind = 0
        #Wwind variable means wind from west side
        
        try: 
            #try block will test if element can be found
            WindDirectionAMK = driver.find_element(By.XPATH, 
            value = "/html/body/div/div/div[3]/div[2]/div/div[1]/div/span[5]/img").get_attribute("alt")
            #find_element() method finds the element on the webpage based on By strategy and locator
            #using xpath to locate element
            #ang mo kio will give north side wind data
            #data for wind direction at ang mo kio can be found in the fifth span tag
            #in the span tag, there is an img tag that contains a url for the image of the wind direction
            #and a alt, which contains a short text to display in case image is unavailable
            #by retrieving the text in alt, direction of wind can be determined
        except: 
            #except block will hand the error if element cannot be found
            print("Wind data from Northside not available")
            #notify the user that the wind data from north side is unavailable
        else: 
            #else block will execute code when element can be found
            if(WindDirectionAMK == "S" or WindDirectionAMK == "SW" or WindDirectionAMK == "SE"): 
                #north location blowing southwards will direct the wind to the main location
                NWind = 1
                #Wind from the north side is directed towards the main location

        try:
            WindDirectionTS = driver.find_element(By.XPATH, 
            value = "/html/body/div/div/div[3]/div[2]/div/div[1]/div/span[12]/img").get_attribute("alt")
            #data for wind direction at tai seng can be found in the twelve span tag
        except:
            print("Wind data from Eastside not available")
            #notify the user that the wind data from east side is unavailable
        else: 
            if(WindDirectionTS == "W" or WindDirectionTS == "NW" or WindDirectionTS == "SW"):
                EWind = 1
                #Wind from the east side is directed towards the main location

        try:
            WindDirectionNWT = driver.find_element(By.XPATH, 
            value = "/html/body/div/div/div[3]/div[2]/div/div[1]/div/span[6]/img").get_attribute("alt")
            #data for wind direction at newton can be found in the sixth span tag
            
        except:
            print("Wind data from Southside not available")
            #notify the user that the wind data from south side is unavailable
        else: 
            if(WindDirectionNWT == "N" or WindDirectionNWT == "NW" or WindDirectionNWT == "NE"):
                SWind = 1
                #Wind from the south side is directed towards the main location

        try:
            WindDirectionCLM = driver.find_element(By.XPATH, 
            value = "/html/body/div/div/div[3]/div[2]/div/div[1]/div/span[14]/img").get_attribute("alt")
            #data for wind direction at clementi can be found in the fourteenth span tag
        except:
            print("Wind data from Westside not available")
            #notify the user that the wind data from west side is unavailable
        else: 
            if(WindDirectionCLM == "E" or WindDirectionCLM == "NE" or WindDirectionCLM == "SE"):
                # print(WindDirectionCLM)
                WWind = 1
                #Wind from the west side is directed towards the main location

    return NWind, EWind, SWind, WWind
        
def dataProcessing(rawData):
    stringData = str(rawData)
    secondLastCharacterPos = len(stringData) - 1
    processedStringData = " " + stringData[1:secondLastCharacterPos].replace("'", '')
    #same data processing steps as the one for bishan in getData()
    weatherCondition = processedStringData.split(": ")[5]
    #split processedStringData into a substrings to form a list of items
    #split items in string by separator string ": "
    #[5] is the sixth item in the list, as the item number starts from 0,1,2,3,4,5...
    return weatherCondition

def incomingRain(rAMK, rSRG, rTPY, rNVA, rCWC, 
rBKT, rBKP, NW, EW, SW, WW):
    #initialise the 4 variables to equal to 0
    NRain = 0
    ERain = 0
    SRain = 0
    WRain = 0

    if (rAMK == 1):
    #if ang mo kio is raining
        NRain = 1
        #location north of main location is raining
    else:
        NRain = 0
        #location north of main location is not raining

    if (rSRG == 1):
    #if serangoon is raining
        ERain = 1
        #location east of main location is raining
    else:
        ERain = 0
        #location east of main location is not raining

    if (rTPY == 1 or rNVA == 1):
    #if toa payoh or novena is raining
        SRain = 1
        #locations south of main location is raining
    else:
        SRain = 0
        #locations south of main location is not raining

    if (rCWC == 1 or rBKT == 1 or rBKP == 1):
    #if central water catchement or bukit timah or bukit panjang is raining
        WRain = 1
        #locations west of main location is raining
    else:
        WRain = 0
        #locations west of main locaiton is not raining

    if((NRain == 1 and NW == 1) or (ERain == 1 and EW == 1) 
    or (SRain == 1 and SW == 1) or (WRain == 1 and WW == 1)):
        #if surrounding location is raining and its wind is directed 
        # towards company location, chance of incoming rain is determined
        print("Possible incoming rain")
    else:
        print("Surrounding rain not likely blown towards main location")
        

def accessWebpage(changeWeb):
    #take in value of changeWeb = 0 or changeWeb = 1, where the value of changeWeb will determine which webpage to access
    URL = ["http://www.weather.gov.sg/weather-forecast-2hrnowcast-2/", "http://www.weather.gov.sg/weather-currentobservations-wind/"] 
    #array containing weather nowcast URL and wind nowcast URL, both in string datatype
    driver.get(URL[changeWeb])
    #syntax: driver.get("URL_of_the_webpage")
    #webdriver takes in the URL to access the webpage
    if (changeWeb == 0):
        print("Accessing rain nowcast...")
        #clarify to the user that the rain nowcast webpage is being accessed
    if (changeWeb == 1):
        print("Accessing wind nowcast...")
        #clarify to the user that the wind nowcast webpage is being accessed
    

def determineRain(wData):
    rainStatus = 0
    if (wData == "Light rain"   or wData == "Moderate Rain" 
    or wData == "Heavy rain"    or wData == "Passing showers" 
    or wData == "Light showers" or wData == "Showers" 
    or wData == "Heavy showers" or wData == "Thundery showers"
    or wData == "Heavy thundery showers" or wData == "Heavy thundery showers with gusty winds"):
    #if weatherdata of location matches any of the rain related texts, determine location is raining
        rainStatus = 1
    else:
    #else location is not raining
        rainStatus = 0
    return rainStatus

driver = init_webdriver()
#initialise webdriver, returns and calls the webdriver.Firefox() method

#web scraping loop
while (True):
    accessWebpage(changeWeb = 0)
    #access rain nowcast webpage
    print("-------------------------------")
    wDataBSH,wDataAMK,wDataSRG,wDataTPY,wDataNVA,wDataCWC,wDataBKT,wDataBKP = getData(changeWeb = 0)
    #return Bishan's processed string data and the surrounding locations weather data
    splitData = wDataBSH.split(",")
    #split Bishan's processed string data by the separator string ","
    for x in splitData:
    #x starts at 0 and increment by 1. maximum is based on the number of items in split data
        print(x)    
        #print out each item in the list in splitData
    weatherConditionBSH = splitData[4].split(": ")[1]
    #obtain only the weather data for Bishan
    rainBSH = determineRain(weatherConditionBSH)
    if (rainBSH == 1):
        print(" Rain Status: Raining")
        buzzFrequency = 2500  
        # Set Frequency buzz sound to 2500 hz
        buzzDuration = 200
        # Set Duration of buzz to 0.2 seconds
        print(" Shelter System Activated")
        # ser.write(b'H')
        # Tells arduino to activate shelter system
    else:
        print(" Rain Status: Not Raining")
        print(" Shelter System Deactivated")
        # ser.write(b'L')
        # Tells arduino to deactivate the shelter system
        
    print("-------------------------------")

    #determine is locations are raining
    rainAMK = determineRain(wDataAMK)
    rainSRG = determineRain(wDataSRG)
    rainTPY = determineRain(wDataTPY)
    rainNVA = determineRain(wDataNVA)
    rainCWC = determineRain(wDataCWC)
    rainBKT = determineRain(wDataBKT)
    rainBKP = determineRain(wDataBKP)

    accessWebpage(changeWeb = 1)
    #access wind nowcast webpage
    NWind, EWind, SWind, WWind = getData(changeWeb = 1)
    #retrieve wind direction data of surrounding locations,
    #determine if the directions are pointed towards the main location

    incomingRain(rainAMK,rainSRG,wDataTPY,wDataNVA,wDataCWC,wDataBKT,wDataBKP,NWind,EWind,SWind,WWind)
    #determine if rain is directed towards main location

    time.sleep(2)
    #two second delay
    os.system('cls')
    #refresh terminal