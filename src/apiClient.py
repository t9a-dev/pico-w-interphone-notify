import os
import ssl
import microcontroller
import adafruit_requests
import base64

class notify:
  def __init__(self,socket):
    self.client = adafruit_requests.Session(socket,ssl.create_default_context())
  
  def requestTest(self):
    try:
      self.client.request(method='GET',url = 'https://www.google.com/');
    except:
      # 疎通確認できなければ再起動(ハードリセット)してシステムの回復を試みる。(起動時にネットワーク接続を行っているので)
      # https://learn.adafruit.com/circuitpython-essentials/circuitpython-resetting#hard-reset-3087083
      microcontroller.reset();

  def pushToNtfy(self,topic,message):
    url = f'{os.getenv('NTFY_URL')}{topic}'
    ntfy_auth_value = os.getenv('NTFY_AUTH_VALUE')
    encode_credentials = base64.b64encode(ntfy_auth_value.encode('utf-8')).decode('utf-8')
    print(encode_credentials)
    headers = {
        'Authorization':f'Basic {encode_credentials}',
    }
    data = message
    try:
      self.client.request(
        method='POST',
        url=url,
        headers=headers,
        data = data,
      )
    except:
      pass