package device

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
)

// 응답 구조체 정의
type DeviceAuthResponse struct {
	DeviceCode      string `json:"device_code"`
	UserCode        string `json:"user_code"`
	VerificationURI string `json:"verification_uri"`
	ExpiresIn       int    `json:"expires_in"`
	Interval        int    `json:"interval"`
}

type TokenResponse struct {
	AccessToken  string `json:"access_token"`
	TokenType    string `json:"token_type"`
	RefreshToken string `json:"refresh_token"`
	ExpiresIn    int    `json:"expires_in"`
	Scope        string `json:"scope"`
	JWT          string `json:"jwt"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}

// DeviceAuthorization SHIELD ID(Security365 Idaas) OAuth2 흐름을 위한 디바이스 인증을 수행합니다.
// 성공 시 토큰 정보와 true를 반환하고, 실패 시 오류 정보와 false를 반환합니다.
func DeviceAuthorization() (map[string]interface{}, bool) {
	// 결과를 저장할 맵 초기화
	result := make(map[string]interface{})

	// 환경변수에서 디바이스 코드 서버 URL 가져오기
	baseURL := os.Getenv("DEVICE_CODE_SERVER")
	if baseURL == "" {
		result["error"] = "DEVICE_CODE_SERVER 환경변수가 설정되지 않았습니다"
		return result, false
	}

	// UUID 생성
	clientID := uuid.New().String()

	// 엔드포인트 URL 구성
	deviceAuthURL := baseURL + "/v1/device/code"
	tokenURL := baseURL + "/v1/device/token"

	// 디바이스 코드 요청
	deviceAuthRequest := map[string]string{
		"client_id": clientID,
		"scope":     "profile",
	}

	deviceAuthJSON, err := json.Marshal(deviceAuthRequest)
	if err != nil {
		result["error"] = fmt.Sprintf("JSON 변환 오류: %v", err)
		return result, false
	}

	resp, err := http.Post(deviceAuthURL, "application/json", bytes.NewBuffer(deviceAuthJSON))
	if err != nil {
		result["error"] = fmt.Sprintf("디바이스 코드 요청 오류: %v", err)
		return result, false
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		result["error"] = fmt.Sprintf("디바이스 코드 요청 실패, 상태 코드: %d", resp.StatusCode)
		return result, false
	}

	// 응답 파싱
	var authResp DeviceAuthResponse
	if err := json.NewDecoder(resp.Body).Decode(&authResp); err != nil {
		result["error"] = fmt.Sprintf("응답 파싱 오류: %v", err)
		return result, false
	}

	// 필수 응답 데이터 확인
	if authResp.DeviceCode == "" || authResp.UserCode == "" || authResp.VerificationURI == "" || authResp.ExpiresIn == 0 {
		result["error"] = "필수 응답 데이터가 누락되었습니다"
		return result, false
	}

	// 인터벌이 지정되지 않은 경우 기본값 설정
	if authResp.Interval == 0 {
		authResp.Interval = 5
	}

	// 사용자에게 인증 URL 표시
	fmt.Printf("다음 URL을 방문하여 로그인하세요\n\n%s/%s\n\n로그인을 기다리는 중...\n\n",
		authResp.VerificationURI, authResp.UserCode)

	// 토큰 폴링
	expiresAt := time.Now().Add(time.Duration(authResp.ExpiresIn) * time.Second)

	for time.Now().Before(expiresAt) {
		tokenRequest := map[string]string{
			"client_id":   clientID,
			"device_code": authResp.DeviceCode,
		}

		tokenJSON, err := json.Marshal(tokenRequest)
		if err != nil {
			result["error"] = fmt.Sprintf("JSON 변환 오류: %v", err)
			return result, false
		}

		tokenResp, err := http.Post(tokenURL, "application/json", bytes.NewBuffer(tokenJSON))
		if err != nil {
			result["error"] = fmt.Sprintf("토큰 요청 오류: %v", err)
			return result, false
		}

		defer tokenResp.Body.Close()

		if tokenResp.StatusCode == http.StatusOK {
			// 인증 성공
			var tokenData TokenResponse
			if err := json.NewDecoder(tokenResp.Body).Decode(&tokenData); err != nil {
				result["error"] = fmt.Sprintf("토큰 응답 파싱 오류: %v", err)
				return result, false
			}

			// 결과 맵에 토큰 정보 추가
			result["access_token"] = tokenData.AccessToken
			result["token_type"] = tokenData.TokenType
			result["refresh_token"] = tokenData.RefreshToken
			result["expires_in"] = tokenData.ExpiresIn
			result["scope"] = tokenData.Scope
			result["jwt"] = tokenData.JWT

			return result, true
		} else if tokenResp.StatusCode == http.StatusNoContent {
			// 아직 인증되지 않음, 대기 후 재시도
			time.Sleep(time.Duration(authResp.Interval) * time.Second)
		} else {
			// 예상치 못한 오류
			result["error"] = fmt.Sprintf("예상치 못한 오류: %d", tokenResp.StatusCode)
			return result, false
		}
	}

	// 시간 초과
	result["error"] = "인증 시간이 초과되었습니다"
	return result, false
}
