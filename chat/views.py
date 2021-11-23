from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from django.http import HttpRequest

from chat.models import WSAuth


def connection_test(request):
    return render(request, 'chat/connection_test.html')


class GetWSToken(APIView):
    def get(self, request: Request):
        if self.request.user.is_authenticated:
            auth_obj = WSAuth.objects.create(info=request._request.META['HTTP_USER_AGENT'], user=request.user)
            return Response({'ws_token': auth_obj.token})
        return Response({'result': 'User is not authenticated'}, status=401)
