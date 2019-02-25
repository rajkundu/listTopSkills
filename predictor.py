import requests
import json
import sys
def main():
    i = 0
    teamString = input("Enter the teams: \n")
    if(".txt" in teamString):
        with open(teamString) as f:
            teamListRaw = f.readlines()
            for line in teamListRaw:
                teamString = line
                teamString.rstrip()
                teamList = teamString.split()
                calculate(teamList)
                i+=1
    else:
        teamList = teamString.split()
        calculate(teamList)

def calculate(teamList):
    rawR1 = requests.get("https://api.vexdb.io/v1/get_rankings?team="+teamList[0] + "&season=Turning%20Point")
    rawR2 = requests.get("https://api.vexdb.io/v1/get_rankings?team="+teamList[1] + "&season=Turning%20Point")
    rawB1 = requests.get("https://api.vexdb.io/v1/get_rankings?team="+teamList[2] + "&season=Turning%20Point")
    rawB2 = requests.get("https://api.vexdb.io/v1/get_rankings?team="+teamList[3] + "&season=Turning%20Point")

    cleanR1 = json.loads(rawR1.text)
    cleanR2 = json.loads(rawR2.text)
    cleanB1 = json.loads(rawB1.text)
    cleanB2 = json.loads(rawB2.text)
    if(cleanR1['size'] > 0 and cleanR2['size'] > 0 and cleanB1['size'] > 0 and cleanB2['size'] > 0):
            redOPR = cleanR1['result'][0]['opr'] + cleanR2['result'][0]['opr']
            blueOPR = cleanB1['result'][0]['opr'] + cleanB2['result'][0]['opr']
            redDPR = cleanR1['result'][0]['dpr'] + cleanR2['result'][0]['dpr']
            blueDPR = cleanB1['result'][0]['dpr'] + cleanB2['result'][0]['dpr']

            redScore = redOPR+blueDPR
            blueScore = blueOPR+redDPR
            redScore = int(round(redScore))
            blueScore = int(round(blueScore))

            print("Red (" + teamList[0] + " and " + teamList[1] +"): " + str(redScore))
            print("Blue (" + teamList[2] + " and " + teamList[3] +"): " + str(blueScore))

    else:
        print("Error: Check team numbers. Entered teams either do not exist or haven't competed in Turning Point yet.")
if __name__ == "__main__":
    main()
