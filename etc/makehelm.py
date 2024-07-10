from shieldid import IapBuilder
from string import Template

template = '''
pvc:
  controllerStorage:
    storageClass: local-path
    accessMode: ReadWriteOnce        
    storageRequest: 1Gi

repo:
  url: scharbor.security365.com/iap/

certificates:
  tlsCrt: ${fullcahin}
  tlsKey: ${privkey}

ingress:
  ingressClassName: ingress-nginx-teams
  mainDomainHost: ${main_domain}

iapController:
  image: iap-event-handler:20240621.1
  env:
    iapIdgpId: ${app_id}
    iapIdgpSecret: ${app_secret}
    iapIdgpUrl: ${idgp_url}
    iapExtra: ${app_extra}
    kvBridge: dev-kvbridge.softcamp.co.kr:443
    esBridge: dev-esbridge.softcamp.co.kr:443
optionalInfo:
    edgeDescription: "[cluster]: secaas 쿠버네티스  [ns]: script를 통해 생성된 edge 입니다.  "
    edgePublicIp: "${ip_address}"
useImagePullSecret: false
imagepullsecret : softcamp-secret
'''



builder = IapBuilder()
info, ok, err_msg = ( builder.device_authorize("https://dev-iapapi.softcamp.co.kr")
            .create_edge_app("tt11", "iap edge controller app")
            # .set_dns_record("211.175.134.197")
            # .make_ssl_certificates()
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
    # set_dns_record 호출후 부를 수 있는 함수들
    print(info.get_ip_address())
    print(info.get_main_domain())  # ingress.mainDomainHost
    
    # make_ssl_certificates 호출후 부를 수 있는 함수들
    print(info.get_fullchain())    # certificates.tlsCrt
    print(info.get_privkey())      # certificates.tlsKey
    
    sub = {
        "app_id": info.get_app_id(),
        "app_secret": info.get_app_secret(),
        "app_extra": info.get_app_extra(),
        "ip_address": info.get_ip_address(),
        "idgp_url": "https://devlogin.softcamp.co.kr",
        "main_domain": info.get_main_domain(),
        "fullcahin": info.get_fullchain(),
        "privkey": info.get_privkey(),
    }
    
    output = Template(template).substitute(sub)
    
    # write output to values.yaml file
    with open("values.yaml", "w") as f:
        f.write(output)
    
    