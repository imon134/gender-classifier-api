from api.index import classify

def handler(request):
    return classify(request)