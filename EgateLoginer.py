import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def collect_data(text, name, endtag):
    start_idx = text.find(f'name="{name}"')
    if name == 'pwdEncryptSalt':
        start_idx = text.find(f'id="{name}"')
    end_idx = text[start_idx:].find(endtag) + start_idx
    raw_data = text[start_idx:end_idx]
    res = raw_data[raw_data.find('value=')+7:-2]##-2
    return res

def login(studentid, password):
    url = r"https://ids.shanghaitech.edu.cn/authserver/login?service="
    new_session = requests.session()
    new_session.cookies.clear()
    response = new_session.get(url)
    lt = collect_data(response.text, 'lt', r'/>')
    dllt = 'generalLogin'
    execution = collect_data(response.text, 'execution', r'/>')
    _eventId = 'submit'
    rmShown = '1'
    key = collect_data(response.text, 'pwdEncryptSalt', r'/>')
    padded_password = b'Nu1L' * 16 + password.encode()
    pkcs7_padded_password = pad(padded_password, 16, 'pkcs7')
    iv = b'Nu1L' * 4
    aes = AES.new(key.encode(), AES.MODE_CBC, iv)
    password = base64.b64encode(aes.encrypt(pkcs7_padded_password))

    data = {
        'username':studentid,
        'password':password,
        'lt':lt,
        'dllt':dllt,
        'execution':execution,
        '_eventId':_eventId,
        'rmShown':rmShown
    }
    response = new_session.post(url, data=data,headers=headers)
    return new_session

