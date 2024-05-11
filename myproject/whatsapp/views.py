# from rest_framework.decorators import api_view  # type: ignore
# from rest_framework.response import Response # type: ignore
# import time
# import webbrowser as web
# import pyautogui as pg 
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome('./chromedriver')
# driver.get("https://www.python.org")
# from whatsapp_api_client_python import API

# @api_view(['POST'])
def send_message(request):
    pass
#     if request.method == 'POST':
#         phone = "+7" + request.data.get('Phone')
#         message = request.data.get('Message')
#         web.open("https://web.whatsapp.com/send?phone=" + phone + '&text=' + message)
#         time.sleep(30)  
#         # driver.find_element(By.CLASS_NAME("x1c4vz4f x2lah0s xdl72j9 xfect85 x1iy03kw x1lfpgzf")).click()
#         # pg.click(button="send")
#         return Response({'message': 'Message successfully sent'})
#     else:
#         return Response({'error': 'Only POST requests are allowed'})