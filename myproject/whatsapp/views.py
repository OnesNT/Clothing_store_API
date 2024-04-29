# from rest_framework.decorators import api_view  # type: ignore
# from rest_framework.response import Response # type: ignore
# import time
# import webbrowser as web
# # import pyautogui as pg 

# @api_view(['POST'])
# def send_message(request):
#     if request.method == 'POST':
#         phone = "+7" + request.data.get('Phone')
#         message = request.data.get('Message')
#         web.open("https://web.whatsapp.com/send?phone=" + phone + '&text=' + message)
#         time.sleep(30)  
#         # pg.press('enter')
#         return Response({'message': 'Message successfully sent'})
#     else:
#         return Response({'error': 'Only POST requests are allowed'})