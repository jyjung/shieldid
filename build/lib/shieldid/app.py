import sys
sys.path.append("..")
import requests
from typing import Tuple, Dict
from string import Template
from .jwtutil import get_kid_from_jwt, get_name_with_company_subfix

iap_edge_controller_template = '''{
    "clientName": "${client_name}",
    "companyId": "${company_id}",
    "authorizedGrantTypes": [
        "password",
        "client_credentials",
        "authorization_code"
    ],
    "registeredRedirectUri": [
        "${redirect_uri}"
    ],
    "customSetting": [],
    "additionalInformation": {
        "info": "${info}"
    },
    "use": true,
    "accessTokenValiditySeconds": 3600,
    "refreshTokenValiditySeconds": 86400,
    "scope": [
      "ClientAppInfo.ReadWrite",
      "GroupInfo.ReadWrite",
      "PolicyInfo.ReadWrite",
      "CompanyInfo.ReadWrite",
      "CustomInfo.ReadWrite",
      "RoleInfo.ReadWrite",
      "read",
      "UserInfo.ReadWrite",
      "AdminInfo.ReadWrite",
      "ProfileSet.ReadWrite",
      "Profile.ReadWrite",
      "ScopeInfo.ReadWrite"
    ],
    "tokenLifetimePolicy": "token_lifetime_until_revoke",
    "notifyBaseURL": "",
    "notifyTarget": []
}'''


def create_iap_edge_controller_app(url: str, client_name: str, info: str, authinfo: dict)-> Tuple[Dict, bool]: 
    try:
        kid = get_kid_from_jwt(authinfo['jwt'])
        redirect_uri = f"{url}/v1/device/callback/{kid}"
        data = {
            "client_name": client_name,
            "company_id": kid,
            "redirect_uri": redirect_uri,
            "info": info
        }
        api_url = f"{url}/v1/device/shieldid/app/{kid}"
        payload = Template(iap_edge_controller_template).substitute(data)
        response = requests.post(api_url, data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {authinfo['jwt']}"})
        if response.status_code != 200:
            return {"error": f"Failed to create app: {response.text}"}, False
        return response.json(), True
    except Exception as e:
        return {"error": f"Error: {e}"}, False


def create_general_app(url: str, payload: str, authinfo: dict)-> Tuple[Dict, bool]: 
    try:
        kid = get_kid_from_jwt(authinfo['jwt'])
        api_url = f"{url}/v1/device/shieldid/app/{kid}"
        response = requests.post(api_url, data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {authinfo['jwt']}"})
        if response.status_code != 200:
            return {"error": f"Failed to create app: {response.text}"}, False
        return response.json(), True
    except Exception as e:
        return {"error": f"Error: {e}"}, False

    
    
