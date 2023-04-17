from fastapi import BackgroundTasks
from fastapi.param_functions import Query

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.schemas.web_project import WebPayOrderCreate
from app.src.service import web_project

router = BaseRouter(tags=["twitter"])


@router.get("/getToken")
def twitter_get_token():
    # print(request.ar)
    # code = request.args.get("code")
    # logger.debug(code)
    # url = "https://api.twitter.com/2/oauth2/token"
    # redict_url="http://localhost:8895/api/v1/twitter/getToken"
    # payload=f'code={code}&grant_type=authorization_code&client_id=Sk1EUkxKTl9RVUJGWUtEZ0Y2VEE6MTpjaQ&redirect_uri={redict_url}&code_verifier=challenge'
    # payload=dict(
    #     code=code,
    #     grant_type="authorization_code",
    #     redirect_uri=redict_url,
    #     code_verifier="challenge"
    # )
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     "Authorization": "Basic U2sxRVVreEtUbDlSVlVKR1dVdEVaMFkyVkVFNk1UcGphUTpxOTFNSzNPVHc4b1JERDhlaWpUNWVfeWpyU0dXRmZ0c3Excl96OFlQd20yckc2OGhtSw=="
    # }
    # print("*"*100)
    # print(payload)
    # response = requests.request("POST", url, headers=headers, data=payload)
    # logger.debug(response.status_code)
    # logger.debug(response.content)
    # logger.debug(response.text)
    # logger.debug(response.json())

    # user_me = requests.request(
    #     "GET",
    #     "https://api.twitter.com/2/users/me",
    #     headers={"Authorization": "Bearer bkJuMtp1AFrZpkKnlZz4z8FHRmjj1e3V7sayY7tk0r5Lu"},
    # ).json()
    # logger.debug(user_me)
    # user_id = user_me["data"]["id"]

    # return redirect("/account/bindTwitter2?type=twitter",code=302,Response=None)
    # return BaseResponse.return_success()
    return 200, None
