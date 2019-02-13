#!/usr/bin/env python3

import sys, requests, json, operator, pandas
from bs4 import BeautifulSoup
from beautifultable import BeautifulTable

#Get team nums
if(len(sys.argv) > 1):
    url = sys.argv[1]
else:
    print("Please enter the robotevents URL >> ", end="")
    url = input()

soup = BeautifulSoup(requests.get(url).text, features="lxml")

print
#Get team num table from robotevents
teamListTable = pandas.read_html(str(soup), attrs={"id":"data-table"})[0]
teamNums = teamListTable["Team"].values

#Print event info
eventInfoTable = BeautifulTable()
eventInfoTable.width_exceed_policy = BeautifulTable.WEP_ELLIPSIS
eventInfoTable.column_headers = ["\033[1;32mEvent Name\033[0;0m", "\033[1;32m# Teams\033[0;0m"]
eventInfoTable.append_row([(soup.title.string.strip().replace("Robot Events: ", "")), len(teamNums)])
print(eventInfoTable)

#Team object Class
class Team:
    teamNum = "0000A"
    topDriver = 0
    topProgramming = 0

    def __init__(self, teamNum):
        self.teamNum = teamNum

#Instantiate empty list of team objects
teamObjList = list()
print()
searchParameters = {"season":"Turning Point", "season_rank":"true"}
for index, currentTeam in enumerate(teamNums):
    sys.stdout.write("\rGetting skills information for Team \033[1;31m%d\033[0;0m of %d..." % (index + 1, len(teamNums)))
    searchParameters["team"] = currentTeam
    rawresponse = requests.get("https://api.vexdb.io/v1/get_skills", params = searchParameters)
    skillsevents = json.loads(rawresponse.text)
    newTeam = Team(currentTeam)
    for run in skillsevents["result"]:
        scoreType = run["type"]
        if(scoreType == 0):
            newTeam.topDriver = run["score"]
        elif(scoreType == 1):
            newTeam.topProgramming = run["score"]
    teamObjList.append(newTeam)
sys.stdout.write("\r                                                                            \n")
sys.stdout.flush()

#Sort team objects by total of driver and programming skills scores
sortedTeamObjList = sorted(teamObjList, key=lambda teamObj: (teamObj.topDriver + teamObj.topProgramming), reverse=True)

skillsInfoTable = BeautifulTable()
skillsInfoTable.width_exceed_policy = BeautifulTable.WEP_ELLIPSIS
skillsInfoTable.column_headers = ["\033[1;31mTeam #\033[0;0m", "\033[1;33mTotal (Inter-event)\033[0;0m", "\033[;1mTop Driver\033[;1m", "\033[0;1mTop Programming\033[0;0m"]
for teamObj in sortedTeamObjList:
    skillsInfoTable.append_row([("\033[1;31m%s\033[0;0m" % teamObj.teamNum), ("\033[1;33m%d\033[0;0m" % (teamObj.topDriver + teamObj.topProgramming)), teamObj.topDriver, teamObj.topProgramming])
print(skillsInfoTable)
