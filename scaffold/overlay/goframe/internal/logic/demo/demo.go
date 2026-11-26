// Package demo 示例业务：演示 logic/<业务>/ 的组织方式。
// 与 api/demo/v1 同名对应；场景函数直接收发 v1 的 Req/Res；一个业务场景一个文件（greet.go），测试同目录。
// 本文件放本业务共用的常量与小工具；首个真实业务落地后删除整个 demo 业务。
package demo
