// proxy.js
import express from 'express'
import cors from 'cors'
import fetch from 'node-fetch'
import dotenv from 'dotenv'

dotenv.config()

const app = express()
app.use(cors())
app.use(express.json())

app.post('/xrpl', async (req, res) => {
  try {
    const xrplRes = await fetch('https://s.altnet.rippletest.net:51234', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    })

    const data = await xrplRes.json()
    res.json(data)
  } catch (err) {
    console.error(err)
    res.status(500).json({ error: 'XRPL proxy error' })
  }
})

// 🔥 NEW XUMM FORWARDER ENDPOINT
app.post('/xumm', async (req, res) => {
  try {
    const xummRes = await fetch('https://xumm.app/api/v1/platform/payload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.XUMM_API_KEY // Put your public XUMM API key in .env
      },
      body: JSON.stringify(req.body)
    })

    const data = await xummRes.json()
    res.json(data)
  } catch (err) {
    console.error(err)
    res.status(500).json({ error: 'XUMM proxy error' })
  }
})

app.listen(4000, () => console.log('Proxy running on http://localhost:4000'))
