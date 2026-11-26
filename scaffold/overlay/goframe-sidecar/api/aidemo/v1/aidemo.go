package v1

import "github.com/gogf/gf/v2/frame/g"

// SummarizeReq 示例场景「摘要」：Go 收参后转给 Python 侧车计算。演示 Go 主后端 + 侧车的调用链；首个真实能力落地后删除 aidemo。
type SummarizeReq struct {
	g.Meta `path:"/aidemo/summarize" method:"post" tags:"示例" summary:"侧车摘要示例"`
	Text   string `json:"text" v:"required|max-length:10000#请填写文字|文字最多10000字"`
}

// SummarizeRes 与侧车 app/schemas/demo.py SummarizeRes 字段一一对应。
type SummarizeRes struct {
	Chars   int    `json:"chars"`
	Lines   int    `json:"lines"`
	Preview string `json:"preview"`
}
