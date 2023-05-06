import request from '@/utils/axios'

const uploadAnalysisFile = async (file: File) => {
  const form = new FormData()
  form.append('file', file)
  return request.post<{ hash: string }>('/api/analysis', form)
}

const getAnalysisResult = async (hash: string) => {
  return request.get(`/api/analysis/${hash}`)
}

export { uploadAnalysisFile, getAnalysisResult }
