// Simple React app to fetch memo hash from an XRPL transaction
import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

export default function NGOHashViewer() {
  const [txHash, setTxHash] = useState('')
  const [ngoMemo, setNgoMemo] = useState<{ type: string; data: string } | null>(null)
  const [loading, setLoading] = useState(false)

  const fetchHash = async () => {
    setLoading(true)
    setNgoMemo(null)
    try {
      const res = await fetch('http://localhost:4000/xrpl', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          method: 'tx',
          params: [{
            transaction: txHash,
            binary: false
          }]
        })
      })

      const data = await res.json()
      console.log('TX Memo object:', data.result?.Memos)

      const memos = data.result?.Memos || []

      if (!Array.isArray(memos) || memos.length === 0 || !memos[0].Memo) {
        setNgoMemo({ type: 'No memo', data: 'No memo' })
        setLoading(false)
        return
      }

      const hexType = memos[0].Memo.MemoType
      const hexData = memos[0].Memo.MemoData

      const type = hexType ? decodeHex(hexType) : 'No memo type'
      const dataStr = hexData ? decodeHex(hexData) : 'No memo data'

      setNgoMemo({ type, data: dataStr })
    } catch (err) {
      console.error(err)
      setNgoMemo({ type: 'Error', data: 'Error fetching data' })
    }
    setLoading(false)
  }

  const decodeHex = (hex: string) => {
    try {
      return decodeURIComponent(
        hex.replace(/(..)/g, '%$1')
      )
    } catch {
      return '[Invalid UTF-8]'
    }
  }

  return (
    <div className="p-6 max-w-xl mx-auto space-y-6">
      <Card>
        <CardContent className="space-y-4 p-4">
          <h2 className="text-xl font-semibold">Verify NGO Metadata on XRPL</h2>
          <Input
            placeholder="Enter XRPL Transaction Hash"
            value={txHash}
            onChange={(e) => setTxHash(e.target.value)}
          />
          <Button onClick={fetchHash} disabled={loading}>
            {loading ? 'Checking...' : 'Fetch NGO Hash'}
          </Button>
          {ngoMemo && (
            <div className="break-all bg-muted p-3 rounded-md space-y-1">
              <div><strong>Memo Type:</strong> {ngoMemo.type}</div>
              <div><strong>Memo Data:</strong> {ngoMemo.data}</div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

