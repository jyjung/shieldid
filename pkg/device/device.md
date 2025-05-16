
`device_authorization` 함수는 SHIELD ID(Security365 Idaas) OAuth2 흐름을 위한 디바이스 인증을 수행합니다. 코드 분석은 다음과 같습니다:

1. **기본 동작**:
   - 브라우저 입력이 제한된 디바이스에서도 인증할 수 있는 OAuth2 Device Authorization 흐름 구현
   - 사용자에게 인증 URL과 코드를 제공하고, 사용자가 다른 디바이스에서 인증하는 동안 대기

2. **주요 단계**:
   - device code server 는 환경변수에서 입력받음  DEVICE_CODE_SERVER
   - UUID로 임의의 `client_id` 생성
   - 서버에 디바이스 코드 요청 (`POST {device code server}/v1/device/code` )
     -  {
            'client_id': client_id,
            'scope': 'profile'
        }
   - 응답에서 `device_code`, `user_code`, `verification_uri`, `expires_in`, `interval` 추출
   - 콘솔  Print로    verification_url  표시 
   - 최대 5분동안 계속 적으로  토큰 확인 (`POST {device code server}/v1/device/token` 엔드포인트)
     - {
                'client_id': client_id,
                'device_code': device_code
        }
   - 인증 완료되면 토큰 정보 반환, 실패하면 오류 메시지 반환

3. **프로세스 결과**:
   - 성공 시: 액세스 토큰, 리프레시 토큰 등을 포함한 딕셔너리와 `True` 반환
   - 실패 시: 오류 정보를 포함한 딕셔너리와 `False` 반환

4. **예외 처리**:
   - HTTP 상태 코드 확인을 통한 오류 처리

5. **타임아웃 처리**:
   - `expires_in` 값 기반으로 인증 대기 시간 제한
   - 시간 초과 시 "Authorization timed out" 오류 반환
