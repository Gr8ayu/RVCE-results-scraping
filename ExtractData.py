import re, os
from bs4 import BeautifulSoup as bs
from time import strftime

def extractGrades(page):
    soup = bs(page,'html.parser')

    if soup.find("title").get_text()!='RVCE RESULTS':
        return 0

    x = soup.find("td", attrs={'data-title':'USN'})
    if x == None:
        return 0

    USN = x.find('b')
    if USN:
        USN = USN.get_text()
    else:
        USN = ""
        return 0

    x = soup.find("td", attrs={'data-title':'NAME'})
    NAME = x.find('b')
    if NAME:
        NAME = NAME.get_text()
    else:
        NAME = ""

    x = soup.find("td", attrs={'data-title':'SGPA'})
    SGPA = x.find('b')
    if SGPA:
        SGPA = SGPA.get_text()
    else:
        SGPA = ""

    y = soup.findAll("tbody")[1]
    y = y.findAll('tr')

    grades= []
    y.pop(-1)
    for table_row in y:

        Cname = table_row.find("td",attrs={'data-title':'COURSE NAME'})
        if Cname and Cname != None:
            Cname = Cname.get_text()
        Cgrade = table_row.find("td",attrs={'data-title':'GRADE'})
        if Cgrade and Cgrade != None:
            Cgrade = Cgrade.get_text()

        grades.append([Cname,Cgrade])

    return {"usn":USN,"name":NAME,"sgpa":SGPA,"grades":grades}

def writeData(data,filename):

    resultpath = r'./results/'+str(strftime("%Y-%m-%d %H:%M:%S"))+'/'
    if not os.path.exists(resultpath):
        print("creating directory :",resultpath)
        os.makedirs(resultpath)

    with open('./results/'+filename+'.xlsx','w') as fwrite:
        for result in data:

            fwrite.write(result['usn']+"\t"+result['name']+"\t"+result['sgpa']+"\n")

            for subject in result['grades']:
                fwrite.write(str(subject[0])+ "\t" +str(subject[1])+"\n")

            fwrite.write("\n")
