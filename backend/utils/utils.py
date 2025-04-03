from rest_framework.response import Response

def create_response(status, message, data=None, status_code=200):
    response_data = {
        "status": status,
        "message": message,
    }
    if data is not None:
        response_data["data"] = data
    return Response(response_data, status=status_code)

def create_login_response(status, message, token=None, user=None, status_code=200):
    response_data = {
        "status": status,
        "message": message,
    }
    if token:
        response_data["token"] = token
    if user:
        response_data["user"] = user
    return Response(response_data, status=status_code)
