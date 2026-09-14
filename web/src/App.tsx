import { useEffect, useState, type FormEvent } from 'react'

export type Snippet = {
  id: string
  title: string
  language: string
  code: string
  createdAt: string
}

function App() {
  const [snippets, setSnippets] = useState<Snippet[]>([])
  const [title, setTitle] = useState('')
  const [language, setLanguage] = useState('')
  const [code, setCode] = useState('')
  const [query, setQuery] = useState('')

  const needle = query.trim().toLowerCase()
  const visible = needle
    ? snippets.filter(
        (s) => s.title.toLowerCase().includes(needle) || s.language.toLowerCase().includes(needle),
      )
    : snippets

  useEffect(() => {
    fetch('/snippets')
      .then((res) => res.json())
      .then((data: Snippet[]) => setSnippets(data))
  }, [])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const res = await fetch('/snippets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, language, code }),
    })
    const created: Snippet = await res.json()
    setSnippets((prev) => [created, ...prev])
    setTitle('')
    setLanguage('')
    setCode('')
  }

  return (
    <main>
      <h1>Snippet Vault</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Title
          <input value={title} onChange={(e) => setTitle(e.target.value)} />
        </label>
        <label>
          Language
          <input value={language} onChange={(e) => setLanguage(e.target.value)} />
        </label>
        <label>
          Code
          <textarea value={code} onChange={(e) => setCode(e.target.value)} />
        </label>
        <button type="submit">Save</button>
      </form>
      <label>
        Search
        <input type="search" value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>
      {needle && visible.length === 0 && <p>No snippets match.</p>}
      <ul>
        {visible.map((snippet) => (
          <li key={snippet.id}>
            <h2>{snippet.title}</h2>
            <span>{snippet.language}</span>
            <pre>
              <code>{snippet.code}</code>
            </pre>
          </li>
        ))}
      </ul>
    </main>
  )
}

export default App
