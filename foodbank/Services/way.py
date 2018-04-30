import urllib.request
import http.cookiejar
import sys
class SendSMS():
    @classmethod
    def send(cls,number,messageid):
        uname="9177640926"
        password="G9426M"
        message = "New update. Check Timeline"+messageid
        message = "+".join(message.split(' '))
        #Logging into the SMS Site
        url_for_wsms = 'http://site24.way2sms.com/Login1.action?'
        data_for_wsms = 'username='+uname+'&password='+password+'&Submit=Sign+in'
        data_for_wsms = data_for_wsms.encode('UTF-8')

        cookie_jar = http.cookiejar.CookieJar()
        print(cookie_jar)
        cookie_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        print(cookie_opener)
        cookie_opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
        print(cookie_opener)
        user_open = cookie_opener.open(url_for_wsms, data_for_wsms)
        print(user_open)
        ssionId = str(cookie_jar).split('~')[1].split(' ')[0]
        print(ssionId)
        smsurl = 'http://site24.way2sms.com/smstoss.action?'
        smsdata = 'ssaction=ss&Token='+ssionId+'&mobile='+number+'&message='+message+'&msgLen=136'
        cookie_opener.addheaders = [('Referer', 'http://site25.way2sms.com/sendSMS?Token='+ssionId)]
        smsdata = smsdata.encode('UTF-8')
        try:
            sentpage = cookie_opener.open(smsurl,smsdata)
        except IOError:
            print("Error while sending message")
        print("SMS has been sent.")
        return 0
