import { ElMessage } from 'element-plus'

/** 后端统一响应，对应 GoFrame ghttp.MiddlewareHandlerResponse 的 {code,message,data}。 */
type ApiEnvelope<T> = {
  code: number
  message: string
  data: T
}

export type ApiRequestInit = RequestInit & {
  /** 为 true 时出错不弹提示，由调用方自行处理。 */
  silent?: boolean
}

/**
 * 全站唯一请求入口：所有 api/<模块>/ 都经这里发请求。
 * 输入为 /api 下的路径与 fetch 选项；code=0 返回 data，否则弹出后端文案并抛错。
 * 鉴权头、401 跳登录、全屏加载等横切能力只在本函数扩展，禁止页面另建请求实例。
 */
export async function request<T>(url: string, init: ApiRequestInit = {}): Promise<T> {
  const { silent, ...fetchInit } = init
  const headers = new Headers(fetchInit.headers)
  if (fetchInit.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  let message = ''
  try {
    const response = await fetch(url, { ...fetchInit, headers })
    const body = (await response.json()) as ApiEnvelope<T>
    if (response.ok && body.code === 0) {
      return body.data
    }
    message = body.message || `请求失败（${response.status}）`
  } catch {
    message = '网络异常，请稍后重试'
  }

  if (!silent) {
    ElMessage.error(message)
  }
  throw new Error(message)
}
