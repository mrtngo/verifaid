import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { AlertCircle, CheckCircle, Smartphone } from 'lucide-react'

export default function NGOOnboardingForm() {
  const [formData, setFormData] = useState({
    org_name: '',
    location_city: '',
    location_country: '',
    focus_areas: '',
    staff_count: '',
    monthly_salaries_usd: '',
    suppliers: '',
    wallet: ''
  })
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')
  const [payloadPreview, setPayloadPreview] = useState('')
  const [history, setHistory] = useState<{ txid: string; payload: string }[]>([])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const generateMockTxId = () => {
    return Array.from({ length: 64 }, () => 
      Math.floor(Math.random() * 16).toString(16)
    ).join('').toUpperCase()
  }

  const handleSubmit = async () => {
    setLoading(true)
    setStatus('')
    
    // Validate required fields
    if (!formData.org_name || !formData.wallet) {
      setStatus('❌ Please fill in required fields (Organization Name and Wallet)')
      setLoading(false)
      return
    }

    try {
      const jsonPayload = {
        org_name: formData.org_name,
        location: {
          city: formData.location_city,
          country: formData.location_country
        },
        focus_areas: formData.focus_areas.split(',').map(s => s.trim()).filter(s => s),
        staff_count: formData.staff_count ? parseInt(formData.staff_count) : null,
        monthly_salaries_usd: formData.monthly_salaries_usd ? parseInt(formData.monthly_salaries_usd) : null,
        suppliers: (() => {
          try {
            return formData.suppliers ? JSON.parse(formData.suppliers) : []
          } catch {
            return []
          }
        })(),
        wallet: formData.wallet
      }

      const memoPayload = JSON.stringify(jsonPayload, null, 2)
      setPayloadPreview(memoPayload)

      // Simulate the hex encoding process
      const toHex = (str: string) =>
        new TextEncoder().encode(str).reduce((acc, b) => acc + b.toString(16).padStart(2, '0'), '')

      const hexMemoType = toHex('ngo_onboarding')
      const hexMemoData = toHex(memoPayload)

      // Show transaction details
      setStatus('📲 Simulating Xaman wallet interaction...')
      
      // Simulate async transaction process
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Simulate successful transaction
      const mockTxId = generateMockTxId()
      setStatus('✅ Transaction simulation completed')
      
      setHistory(prev => [
        ...prev,
        {
          txid: mockTxId,
          payload: memoPayload
        }
      ])

      // Show transaction payload details
      console.log('Transaction Payload Structure:', {
        TransactionType: 'Payment',
        Destination: formData.wallet,
        Amount: '1000000', // 1 XRP in drops
        Memos: [
          {
            Memo: {
              MemoType: hexMemoType,
              MemoData: hexMemoData
            }
          }
        ]
      })

    } catch (err) {
      console.error(err)
      setStatus('❌ Error processing transaction')
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = () => {
    if (status.includes('✅')) return <CheckCircle className="w-4 h-4 text-green-500" />
    if (status.includes('❌')) return <AlertCircle className="w-4 h-4 text-red-500" />
    if (status.includes('📲')) return <Smartphone className="w-4 h-4 text-blue-500" />
    return null
  }

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-6">
      <Card>
        <CardContent className="space-y-4 p-6">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">NGO Registration</h2>
            <p className="text-sm text-gray-600 mt-2">Register your organization metadata to XRPL</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input 
              placeholder="Organization Name *" 
              name="org_name" 
              value={formData.org_name}
              onChange={handleChange}
              className="border-2 focus:border-blue-500"
            />
            <Input 
              placeholder="Destination Wallet (r...) *" 
              name="wallet" 
              value={formData.wallet}
              onChange={handleChange}
              className="border-2 focus:border-blue-500"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input 
              placeholder="City" 
              name="location_city" 
              value={formData.location_city}
              onChange={handleChange} 
            />
            <Input 
              placeholder="Country" 
              name="location_country" 
              value={formData.location_country}
              onChange={handleChange} 
            />
          </div>
          
          <Input 
            placeholder="Focus Areas (comma-separated)" 
            name="focus_areas" 
            value={formData.focus_areas}
            onChange={handleChange} 
          />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input 
              placeholder="Staff Count" 
              name="staff_count" 
              type="number" 
              value={formData.staff_count}
              onChange={handleChange} 
            />
            <Input 
              placeholder="Monthly Salaries (USD)" 
              name="monthly_salaries_usd" 
              type="number" 
              value={formData.monthly_salaries_usd}
              onChange={handleChange} 
            />
          </div>
          
          <Input 
            placeholder='Suppliers (JSON e.g. [{"name":"XYZ","country":"KE"}])' 
            name="suppliers" 
            value={formData.suppliers}
            onChange={handleChange} 
          />
          
          <Button 
            onClick={handleSubmit} 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            {loading ? 'Processing...' : 'Submit with Xaman (Demo)'}
          </Button>
          
          {status && (
            <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
              {getStatusIcon()}
              <span className="text-sm">{status}</span>
            </div>
          )}
          
          {payloadPreview && (
            <div className="mt-4">
              <h4 className="text-sm font-semibold mb-2">Transaction Payload Preview:</h4>
              <div className="text-xs bg-gray-100 p-4 rounded-lg border overflow-auto max-h-60">
                <pre className="whitespace-pre-wrap">{payloadPreview}</pre>
              </div>
            </div>
          )}
          
          {history.length > 0 && (
            <div className="mt-6">
              <h4 className="text-sm font-semibold mb-3">Transaction History</h4>
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {history.map((entry, idx) => (
                  <div key={idx} className="bg-green-50 border border-green-200 p-3 rounded-lg">
                    <div className="text-xs">
                      <div className="font-medium text-green-800">Transaction ID:</div>
                      <div className="font-mono text-green-700 break-all">{entry.txid}</div>
                    </div>
                    <div className="text-xs mt-2">
                      <div className="font-medium text-green-800">Payload Preview:</div>
                      <div className="text-green-700 truncate">{entry.payload.substring(0, 100)}...</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="text-sm font-semibold text-blue-800 mb-2">Demo Mode Notice</h4>
            <p className="text-xs text-blue-700">
              This is a demonstration version. In a real implementation, you would need to:
            </p>
            <ul className="text-xs text-blue-700 mt-1 ml-4 list-disc">
              <li>Install the xumm SDK: <code>npm install xumm</code></li>
              <li>Use your actual Xaman API key</li>
              <li>Handle real XRPL transactions</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}