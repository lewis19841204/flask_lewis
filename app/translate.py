import json,random,hashlib,http.client,urllib
import requests
from flask_babel import _
from app import app


def translate(q,fromLang,toLang):
    if 'APPID' not in app.config or not app.config['APPID']:
        return _('Error:the translation service is not configured.')
    if 'BD_TRANSLATOR_KEY' not in app.config or not app.config['BD_TRANSLATOR_KEY']:
        return _('Error:the translation service is not configured.')
    appid = app.config['APPID']
    secretKey = app.config['BD_TRANSLATOR_KEY']

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768,65536)

    sign = appid+q+str(salt)+secretKey
    #sign = hashlib.md5(sign.encode()).hexdigest()
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&form='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET',myurl)
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")
        js = json.loads(jsonResponse)
        #response = httpClient.getresponse()    #response是HTTPResponse对象
        dst = str(js["trans_result"][0]["dst"])
        print(dst)
        return(dst)

    except Exception as e:
        print(e)

    finally:
        if httpClient:
            httpClient.close()
