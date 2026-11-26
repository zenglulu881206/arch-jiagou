import type { GreetResult } from '@/model/demo'
import { request } from '../request'

/** 问候示例：调用后端 GET /api/demo/greet，返回问候语。首个真实业务落地后删除 demo。 */
export function fetchGreet(name: string) {
  const query = new URLSearchParams({ name })
  return request<GreetResult>(`/api/demo/greet?${query}`)
}
