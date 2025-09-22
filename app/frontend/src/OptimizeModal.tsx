import React, { useState } from 'react'

interface Result {
  params: Record<string, number>
  metrics: Record<string, number>
}

export const OptimizeModal: React.FC = () => {
  const [open, setOpen] = useState(false)
  const [results, setResults] = useState<Result[]>([])

  const run = async () => {
    const space = { x: [1, 2, 3] }
    const start = new Date().toISOString()
    const end = new Date().toISOString()
    const resp = await fetch('/api/optimize/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ space, start, end, k_folds: 2 })
    }).then(r => r.json())
    const id = resp.id
    const poll = setInterval(async () => {
      const data = await fetch(`/api/optimize/${id}`).then(r => r.json())
      if (data.run.status === 'done') {
        clearInterval(poll)
        setResults(data.results)
      }
    }, 1000)
  }

  const exportCsv = () => {
    const rows = results.map(r => ({ ...r.params, ...r.metrics }))
    const header = Object.keys(rows[0]).join(',')
    const body = rows.map(r => Object.values(r).join(',')).join('\n')
    const blob = new Blob([header + '\n' + body], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'report.csv'
    a.click()
  }

  return (
    <div>
      <button onClick={() => setOpen(true)}>Optimize</button>
      {open && (
        <div>
          <button onClick={run}>Run</button>
          <button onClick={exportCsv}>Export CSV</button>
          <table>
            <thead>
              <tr>
                <th>Params</th><th>PF</th><th>Sharpe</th><th>MaxDD</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{JSON.stringify(r.params)}</td>
                  <td>{r.metrics.PF}</td>
                  <td>{r.metrics.Sharpe}</td>
                  <td>{r.metrics.MaxDD}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
