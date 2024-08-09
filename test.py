from shieldid import IapBuilder
import requests
def change_base_image(iap_base_url: str, companyid: str, jwt: str, image: str):
    url = iap_base_url + '/v1/info/iap-base-info/' + companyid
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+ jwt,
        'Content-Type': 'application/json'
    }
    data = {
        "image": image,
        "provider": "security365",
        "display": "ms,security365"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print("change base image fail",response.text)
    else:
        print("change base image success")

iap_url = "https://dev-iapapi.softcamp.co.kr"
image = "scharbor.security365.com/iap/socam-oauth2-proxy:20240607.10"
builder = IapBuilder()
info, ok, err_msg = ( builder.device_authorize(iap_url)
                     .create_edge_app("abcd","iap edge controller")
            .build())

if not ok:
    print(err_msg)
else: 
    change_base_image(iap_url, info.get_company_id(), info.get_jwt(), image)
    print(info.get_jwt())  # jwt
    print(info.get_company_id())  # company id
    print(info.get_access_token())  # access token
    # create_edge_app 호출후 부를 수 있는 함수들
    print(info.get_app_id())       # iapController.env.iapIdgpId
    print(info.get_app_secret())   # iapController.env.iapIdgpSecret
    print(info.get_app_extra())    # iapController.env.iapExtra
    print(info.get_app_name())