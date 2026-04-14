from api.classify import classify

def handler(request):
    return classify(request)