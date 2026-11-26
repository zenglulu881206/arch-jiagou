/**
 * 防抖唯一入口：搜索框、筛选输入等高频触发统一用它，禁止各页自写定时器。
 * 返回包装后的函数；最后一次调用后等待 wait 毫秒才执行。
 */
export function debounce<A extends unknown[]>(fn: (...args: A) => void, wait = 300) {
  let timer: ReturnType<typeof setTimeout> | undefined
  return (...args: A) => {
    clearTimeout(timer)
    timer = setTimeout(() => fn(...args), wait)
  }
}
