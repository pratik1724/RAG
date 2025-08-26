import React, { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const ask = async (e) => {
    e.preventDefault()
    setLoading(true); setError(''); setAnswer('')
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ query: question })
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setAnswer(data.answer || '')
    } catch (err) {
      setError(err.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{maxWidth: 820, margin: '40px auto', fontFamily: 'Inter, system-ui, Arial'}}>
      <h1>RAG Chat (Ollama + ChromaDB)</h1>
      <form onSubmit={ask} style={{ display:'flex', gap: 8 }}>
        <input
          value={question}
          onChange={(e)=>setQuestion(e.target.value)}
          placeholder="Ask a question..."
          style={{ flex:1, padding:12, borderRadius:8, border:'1px solid #ccc' }}
        />
        <button disabled={loading || !question.trim()} style={{ padding:'12px 16px', borderRadius:8 }}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {error && <p style={{color:'crimson', marginTop:12}}>Error: {error}</p>}
      {answer && (
        <div style={{marginTop:20, padding:16, border:'1px solid #eee', borderRadius:8, background:'#fafafa'}}>
          <strong>Answer:</strong>
          <div style={{whiteSpace:'pre-wrap'}}>{answer}</div>
        </div>
      )}
    </div>
  )
}
