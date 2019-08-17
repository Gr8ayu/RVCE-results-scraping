import requests
import re
from bs4 import BeautifulSoup as bs

# it request form from results.rvce.edu.in
# return 0 if page failed to load
# otherwise return "captcha_str. captcha_value, PHPSESSID"
def requestForm():
    s =requests.session()

    try:
        page =  s.get("http://results.rvce.edu.in/")
    except Exception as e:
        print(e)


    # print("url status :", page)

    if(page.status_code!=200):
        print("HTML form load failed, ERROR ",page.status_code)
        return 0


    PHPSESSID =  page.cookies['PHPSESSID']
    # print("PHP ID",PHPSESSID)

    soup = bs(page.content,'html.parser')
    captcha = soup.find_all("label")[1].get_text()

    captcha_str = re.match(r'What is (. \+ .) ?',captcha)
    captcha_str = captcha_str.group(1)
    #print("captcha is :"+captcha_str)
    captcha_value = eval(captcha_str)
    #print("returning :"+ str(captcha_value))

    return {"captcha_str":captcha_str,"captcha_value":captcha_value,"PHPSESSID":PHPSESSID}

# submit form data through POST with required data{USN,captcha_value,PHPSESSID} and return HTML recieved
def submitForm(USN,captcha_value,PHPSESSID):

    payload = {'usn': USN, 'captcha': captcha_value}
    cookie = {'PHPSESSID': PHPSESSID}

    try:
        post = requests.post("http://results.rvce.edu.in/viewresult2.php",data = payload, cookies=cookie)
    except Exception as e:
        print(e)

    # print("url status :", post)
    #print(post.content)
    return post
