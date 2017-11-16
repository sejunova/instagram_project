from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sdk.api.message import Message

from utils.sms.serializer import SMSSerializer


class SendSMS(APIView):
    API_KEY = 'NCSGLMHSQ2FTVZUA                                              '
    API_SECRET = '2ZNM5ZPZR07QHSLHVIFAH3XZR1GAGM2F'

    def post(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            params = {
                'type': 'sms',
                'to': serializer.validated_data['receiver'],
                'from': '01029953874',
                'text': serializer.validated_data['message'],
            }
            cool = Message(self.API_KEY, self.API_SECRET)
        else:
            return Response({'error_message': '전화번호가 이상함'}, status=status.HTTP_400_BAD_REQUEST)

        response = cool.send(params)
        if "error_list" in response:
            return Response(status=status.HTTP_200_OK)