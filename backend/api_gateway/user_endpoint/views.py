from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseNotAllowed, \
    JsonResponse, HttpResponse, HttpResponseBadRequest
import json
from json import JSONDecodeError
from backend.common.command.user_create_command \
    import UserCreateCommand, USER_CREATE_COMMAND
from backend.common.event.user_login_event \
    import UserLoginEvent
from backend.common.event.user_logout_event \
    import UserLogoutEvent
from backend.common.messaging.infra.redis.redis_message_publisher \
    import RedisMessagePublisher
from backend.common.rpc.infra.adapter.redis.redis_rpc_client \
    import RedisRpcClient


"""
TODO: add exception controller
"""


def with_json_response(status, data):
    return JsonResponse(data=json.dumps(data), status=status, safe=False)


def register_user(request):
    if request.method == 'POST':
        return __register_user(request)
    else:
        return HttpResponseNotAllowed(['POST'])


def __register_user(request):
    body = json.loads(request.body.decode())
    # TODO: check KeyError
    command = UserCreateCommand(
        email=body['email'],
        password=body['password'],
        user_type=body['userType'],
        car_type=body['carType'],
        plate_no=body['plateNo']
        )

    rpc_response = RedisRpcClient().call(USER_CREATE_COMMAND, command)

    # TODO: handling exception
    return JsonResponse(data=rpc_response.result, status=200)


def login_user(request):
    if request.method == 'POST':
        return __login_user(request)
    else:
        return HttpResponseNotAllowed(['POST'])


def __login_user(request):
    try:
        req_data = json.loads(request.body.decode())
        email = req_data['email']
        password = req_data['password']
    except(KeyError, JSONDecodeError) as e:
        return HttpResponseBadRequest(e)
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        event = UserLoginEvent(user_id=request.user.id)
        RedisMessagePublisher().publish_message(event)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=401)


def logout_user(request):
    if request.method == 'GET':
        return __logout_user(request)
    else:
        return HttpResponseNotAllowed(['GET'])


def __logout_user(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        event = UserLogoutEvent(user_id)
        RedisMessagePublisher().publish_message(event)
        logout(request)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=401)


@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])
