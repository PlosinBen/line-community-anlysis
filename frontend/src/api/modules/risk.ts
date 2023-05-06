import request from '@/utils/axios'

const getRisk = (start_date: string, end_date: string, asset: string[], period: string[]) => {
  const params = Object.entries({
    start_date,
    end_date,
  }).map((item) => item.join('='))
  asset.forEach((str) => {
    params.push(`asset[]=${str.trim()}`)
  })
  period.forEach((str) => {
    params.push(`period[]=${str.trim()}`)
  })
  console.log(params.join('&'))
  return request.get<Record<string, any>>(`/api/risk?${params.join('&')}`)
}

export { getRisk }
