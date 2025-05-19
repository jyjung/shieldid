package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"strings"

	"shieldid/pkg/device"

	"github.com/kirsle/configdir"
	"github.com/spf13/viper"
)

// JWTPayloadToMap JWT 토큰의 payload 부분을 map[string]interface{} 형태로 변환합니다.
func JWTPayloadToMap(tokenString string) (map[string]interface{}, error) {
	// JWT 형식: header.payload.signature
	parts := strings.Split(tokenString, ".")
	if len(parts) != 3 {
		return nil, fmt.Errorf("유효하지 않은 JWT 토큰 형식")
	}

	// payload 부분 (base64url 인코딩됨)
	payloadBase64 := parts[1]

	// base64url을 일반 base64로 변환 (패딩 처리)
	if l := len(payloadBase64) % 4; l > 0 {
		payloadBase64 += strings.Repeat("=", 4-l)
	}

	// '-'와 '_'를 각각 '+'와 '/'로 변환
	payloadBase64 = strings.ReplaceAll(payloadBase64, "-", "+")
	payloadBase64 = strings.ReplaceAll(payloadBase64, "_", "/")

	// base64 디코딩
	payloadBytes, err := base64.StdEncoding.DecodeString(payloadBase64)
	if err != nil {
		return nil, fmt.Errorf("payload base64 디코딩 실패: %v", err)
	}

	// JSON 디코딩
	var payloadMap map[string]interface{}
	if err := json.Unmarshal(payloadBytes, &payloadMap); err != nil {
		return nil, fmt.Errorf("payload JSON 디코딩 실패: %v", err)
	}

	return payloadMap, nil
}

func main() {
	// 1) configdir 로 경로 획득
	configPath := configdir.LocalConfig("my-app")
	fmt.Println(configPath)

	err := configdir.MakePath(configPath)
	if err != nil {
		log.Fatal(err)
	}

	authinfo, sucess := device.DeviceAuthorization()
	if !sucess {
		log.Fatal("Device Authorization Failed")
	}
	fmt.Println(authinfo)

	// JWT 토큰에서 payload 추출
	if jwtToken, ok := authinfo["jwt"].(string); ok {
		payloadMap, err := JWTPayloadToMap(jwtToken)
		if err != nil {
			log.Printf("JWT payload 추출 실패: %v", err)
		} else {
			fmt.Println("JWT Payload:")
			// user_name
			// user_email
			// companyId
			for key, value := range payloadMap {
				fmt.Printf("  %s: %v\n", key, value)
			}
		}
	} else {
		fmt.Println("JWT 토큰이 없거나 문자열이 아닙니다")
	}

	viper.AddConfigPath(configPath)
	viper.SetConfigType("json")

	// TODO:viper를 이용해서 지정한 환경설정에  authinfo 저장
	viper.Set("authinfo", authinfo)
	err = viper.WriteConfigAs(configPath + "/config.json")
	if err != nil {
		log.Fatal(err)
	}
}
