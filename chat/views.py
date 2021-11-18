from django.shortcuts import render


def connection_test(request):
    return render(request, 'chat/connection_test.html')
