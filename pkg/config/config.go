package main

import (
	"fmt"

	"github.com/kirsle/configdir"
	"github.com/spf13/viper"
)

func main() {
	// 1) configdir 로 경로 획득
	configPath := configdir.LocalConfig("my-app")
	fmt.Println(configPath)

	viper.AddConfigPath(configPath)
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	// return viper.ReadInConfig()
}
