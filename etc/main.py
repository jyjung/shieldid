
from shieldid import IapBuilder

def my_show_url(url: str,user_code: str):
    print(f"!!!!!!!!!!!!!!Please visit \n\n{url}/{user_code} \n\nto log in.\n\n")
    print("Waiting for login...")    


builder = IapBuilder()
info, ok, err_msg = ( builder.device_authorize("https://dev-iapapi.softcamp.co.kr",my_show_url)
            .build())
if not ok:
    print(err_msg)
else: 
    print(info.get_company_id())  # company id
    print(info.get_access_token())  # access token
