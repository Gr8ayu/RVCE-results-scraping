#!/usr/bin/python3
import sendData, ExtractData, generateUSN
import sys, datetime
from urllib.request import urlopen

def internet_on():

	try:
		response = urlopen('https://www.google.com/', timeout=10)
		return True
	except: 
		return False

# fread = open("USNlist"+USN_BEGIN+".txt",'r')

def threads(threadname, usnList):
    # try:
    #     pass
    # except Exception as e:
    #     print(e)

    print("thread started :",threadname,len(usnList))
    ExtractedResults=[]
    for USN in usnList:
        try:
            formSummary = sendData.requestForm()
        except Exception as e:
            print("Form request failed :",e)
            continue


        if formSummary == 0:
            print("Form request failed :")
            continue

        print("sending form data for USN",USN)

        try:
            postHtml = sendData.submitForm(USN,formSummary['captcha_value'],formSummary['PHPSESSID'])
        except Exception as e:
            print(e)
            continue

        if postHtml.status_code == 200:
            data = ExtractData.extractGrades(postHtml.content)
            if data != 0:
                # ExtractData.writeData(data,USN_BEGIN+"results.xlsx")
                ExtractedResults.append(data)

    # print(ExtractedResults)
    # for results in ExtractedResults:
    ExtractData.writeData(ExtractedResults,threadname)




if __name__ == "__main__":

    # USN_BEGIN = "1RV15" # 1RV18 1RV17 1RV16 1RV15
    if len(sys.argv) < 2:
        print("Argument Error ! \n Enter year as format '18' ")
        sys.exit()
    # elif sys.argv[1] not in range(2018, datetime.date.today().year + 1):
    #     print("Argument Error ! \n Enter USN format as '18 IS' ")
    #     sys.exit()

    elif not internet_on():
        print("Failed to connect to Internet. Please check Internet connectivity.")
        sys.exit()


    else:

        USN_BEGIN = "1RV"+sys.argv[1]

    USN_LIST = generateUSN.generateUSN(USN_BEGIN)

    print("starting threads")
    for branch in USN_LIST.keys():
        threads(branch, USN_LIST[branch] )
        print("started threads",branch)


#
# while True:
#     USN = fread.readline()
#     if not USN:
#         break
#
#     USN = USN.strip()
#
