from shieldid import IapBuilder

builder = IapBuilder()
info, ok, err_msg = ( builder.device_authorize("https://dev-iapapi.softcamp.co.kr")
            .create_edge_app("devsecaas", "iap edge controller app")
            .build())
if not ok:
    print(err_msg)
else: 
    print(info.get_jwt())  # jwt
    print(info.get_company_id())  # company id
    print(info.get_access_token())  # access token
  
    # create_edge_app 호출후 부를 수 있는 함수들
    print(info.get_app_id())       # iapController.env.iapIdgpId
    print(info.get_app_secret())   # iapController.env.iapIdgpSecret
    print(info.get_app_extra())    # iapController.env.iapExtra
    print(info.get_app_name())