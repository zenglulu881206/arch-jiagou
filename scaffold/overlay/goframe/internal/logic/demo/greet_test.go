package demo

import (
	"context"
	"testing"

	"__APP_MODULE__/api/demo/v1"
)

func TestGreet(t *testing.T) {
	res, err := Greet(context.Background(), &v1.GreetReq{Name: " 张三 "})
	if err != nil || res.Message != "你好，张三" {
		t.Fatalf("正常名字: res=%+v err=%v", res, err)
	}

	if _, err := Greet(context.Background(), &v1.GreetReq{Name: "  "}); err == nil {
		t.Fatal("空名字应返回业务错误")
	}
}
