import { useState, useEffect } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Client } from 'xrpl';
import { toast } from 'sonner';

// XRPL Client instance
const xrplClient = new Client('wss://testnet.xrpl-labs.com');

interface TransactionData {
  txid: string;
  timestamp: string;
  amount: string;
  memo: {
    type: string;
    data: any;
  } | null;
}

export default function TransactionViewer() {
  const [txHash, setTxHash] = useState('');
  const [loading, setLoading] = useState(false);
  const [transaction, setTransaction] = useState<TransactionData | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  // Initialize XRPL connection
  useEffect(() => {
    const connectXRPL = async () => {
      try {
        await xrplClient.connect();
        setIsConnected(true);
        console.log('Connected to XRPL');
      } catch (error) {
        console.error('Failed to connect to XRPL:', error);
        toast.error('Failed to connect to XRPL network');
      }
    };

    connectXRPL();

    return () => {
      if (xrplClient.isConnected()) {
        xrplClient.disconnect();
      }
    };
  }, []);

  const decodeHex = (hex: string) => {
    try {
      return decodeURIComponent(
        hex.replace(/(..)/g, '%$1')
      );
    } catch {
      return '[Invalid UTF-8]';
    }
  };

  const fetchTransaction = async () => {
    if (!txHash) {
      toast.error('Please enter a transaction hash');
      return;
    }

    if (!isConnected) {
      toast.error('Not connected to XRPL network');
      return;
    }

    setLoading(true);
    setTransaction(null);

    try {
      // Ensure we're connected
      if (!xrplClient.isConnected()) {
        await xrplClient.connect();
        setIsConnected(true);
      }

      const response = await xrplClient.request({
        command: 'tx',
        transaction: txHash,
        binary: false
      });

      const tx = response.result;
      
      if (!tx) {
        throw new Error('Transaction not found');
      }

      const memo = tx.Memos?.[0]?.Memo;
      let memoData = null;

      if (memo) {
        const type = memo.MemoType ? decodeHex(memo.MemoType) : 'No memo type';
        const data = memo.MemoData ? decodeHex(memo.MemoData) : 'No memo data';
        
        try {
          memoData = {
            type,
            data: JSON.parse(data)
          };
        } catch {
          memoData = {
            type,
            data
          };
        }
      }

      // Handle date conversion safely
      let timestamp = 'Unknown';
      if (tx.date) {
        try {
          // XRPL dates are in seconds since epoch, convert to milliseconds
          const dateInMs = tx.date * 1000;
          timestamp = new Date(dateInMs).toISOString();
        } catch (err) {
          console.error('Error converting date:', err);
          timestamp = 'Invalid date';
        }
      }

      setTransaction({
        txid: tx.hash,
        timestamp,
        amount: tx.Amount,
        memo: memoData
      });

      toast.success('Transaction fetched successfully');
    } catch (err) {
      console.error('Error fetching transaction:', err);
      toast.error('Failed to fetch transaction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex items-center justify-between">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold">XRPL Transaction Viewer</h1>
            <div className="text-sm text-muted-foreground">
              {isConnected ? (
                <span className="text-green-500">Connected to XRPL Testnet</span>
              ) : (
                <span className="text-red-500">Connecting to XRPL Testnet...</span>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Input
              placeholder="Enter XRPL Transaction Hash"
              value={txHash}
              onChange={(e) => setTxHash(e.target.value)}
              className="w-[500px]"
            />
            <Button 
              onClick={fetchTransaction} 
              disabled={loading || !isConnected}
              className="px-8"
            >
              {loading ? 'Loading...' : 'View Transaction'}
            </Button>
          </div>
        </div>

        {transaction && (
          <div className="grid grid-cols-12 gap-8">
            {/* Transaction Details */}
            <Card className="col-span-4">
              <CardHeader>
                <CardTitle>Transaction Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <div className="text-sm font-medium text-muted-foreground">Transaction ID</div>
                  <a
                    href={`https://testnet.xrpscan.com/tx/${transaction.txid}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline break-all block"
                  >
                    {transaction.txid}
                  </a>
                </div>
                <div className="space-y-2">
                  <div className="text-sm font-medium text-muted-foreground">Amount</div>
                  <div className="font-mono text-lg">{transaction.amount}</div>
                </div>
                <div className="space-y-2">
                  <div className="text-sm font-medium text-muted-foreground">Timestamp</div>
                  <div className="text-lg">
                    {transaction.timestamp === 'Unknown' || transaction.timestamp === 'Invalid date'
                      ? transaction.timestamp
                      : new Date(transaction.timestamp).toLocaleString()}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Memo Data */}
            {transaction.memo && (
              <Card className="col-span-8">
                <CardHeader>
                  <CardTitle>Memo Data</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-2">
                    <div className="text-sm font-medium text-muted-foreground">Memo Type</div>
                    <div className="text-lg text-blue-500">{transaction.memo.type}</div>
                  </div>
                  <div className="space-y-2">
                    <div className="text-sm font-medium text-muted-foreground">Memo Content</div>
                    <div className="bg-muted rounded-lg p-6">
                      <pre className="text-sm overflow-x-auto whitespace-pre-wrap">
                        {typeof transaction.memo.data === 'string'
                          ? transaction.memo.data
                          : JSON.stringify(transaction.memo.data, null, 2)}
                      </pre>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 