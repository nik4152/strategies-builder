import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import { OptimizeModal } from './OptimizeModal'

function App() {
  const [live, setLive] = useState(false)
  const positions: string[] = []
  const pnl = 0
  return (
    <div>
      <h1>Strategy Builder</h1>
      <label>
        Live Trading
        <input type="checkbox" checked={live} onChange={e => setLive(e.target.checked)} />
      </label>
      <div>Daily PnL: {pnl}</div>
      <div>Active Positions: {positions.length}</div>
      <OptimizeModal />
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
