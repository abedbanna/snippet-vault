import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App, { type Snippet } from './App.tsx'

const older: Snippet = {
  id: '1',
  title: 'Older',
  language: 'python',
  code: 'print(1)',
  createdAt: '2026-01-01T00:00:00.000Z',
}
const newer: Snippet = {
  id: '2',
  title: 'Newer',
  language: 'typescript',
  code: 'console.log(2)',
  createdAt: '2026-02-01T00:00:00.000Z',
}

function jsonResponse(body: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(body), { status }))
}

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('App', () => {
  it('renders the app heading', () => {
    vi.stubGlobal('fetch', vi.fn(() => jsonResponse([])))
    render(<App />)
    expect(screen.getByRole('heading', { name: 'Snippet Vault' })).toBeTruthy()
  })

  it('fetches snippets on load and renders them newest first', async () => {
    const fetchMock = vi.fn(() => jsonResponse([newer, older]))
    vi.stubGlobal('fetch', fetchMock)
    render(<App />)

    const items = await screen.findAllByRole('listitem')
    expect(fetchMock).toHaveBeenCalledWith('/snippets')
    expect(items).toHaveLength(2)
    expect(items[0].textContent).toContain('Newer')
    expect(items[0].textContent).toContain('typescript')
    expect(items[0].querySelector('pre code')?.textContent).toBe('console.log(2)')
    expect(items[1].textContent).toContain('Older')
  })

  it('posts the form, prepends the new snippet and clears the form', async () => {
    const created: Snippet = {
      id: '3',
      title: 'Hello',
      language: 'go',
      code: 'fmt.Println()',
      createdAt: '2026-03-01T00:00:00.000Z',
    }
    const fetchMock = vi.fn((_url: string, init?: RequestInit) =>
      init?.method === 'POST' ? jsonResponse(created, 201) : jsonResponse([older]),
    )
    vi.stubGlobal('fetch', fetchMock)
    render(<App />)
    await screen.findByText('Older')

    const titleInput = screen.getByLabelText('Title') as HTMLInputElement
    const languageInput = screen.getByLabelText('Language') as HTMLInputElement
    const codeInput = screen.getByLabelText('Code') as HTMLTextAreaElement
    fireEvent.change(titleInput, { target: { value: 'Hello' } })
    fireEvent.change(languageInput, { target: { value: 'go' } })
    fireEvent.change(codeInput, { target: { value: 'fmt.Println()' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    await waitFor(() => expect(screen.getAllByRole('listitem')).toHaveLength(2))
    expect(fetchMock).toHaveBeenCalledWith('/snippets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'Hello', language: 'go', code: 'fmt.Println()' }),
    })
    const items = screen.getAllByRole('listitem')
    expect(items[0].textContent).toContain('Hello')
    expect(items[1].textContent).toContain('Older')
    expect(titleInput.value).toBe('')
    expect(languageInput.value).toBe('')
    expect(codeInput.value).toBe('')
  })

  it('clicking Delete calls DELETE /snippets/:id and removes the item', async () => {
    const fetchMock = vi.fn((_url: string, init?: RequestInit) =>
      init?.method === 'DELETE'
        ? Promise.resolve(new Response(null, { status: 204 }))
        : jsonResponse([newer, older]),
    )
    vi.stubGlobal('fetch', fetchMock)
    render(<App />)
    await screen.findByText('Older')

    const deleteButtons = screen.getAllByRole('button', { name: 'Delete' })
    expect(deleteButtons).toHaveLength(2)
    fireEvent.click(deleteButtons[0])

    await waitFor(() => expect(screen.getAllByRole('listitem')).toHaveLength(1))
    expect(fetchMock).toHaveBeenCalledWith('/snippets/2', { method: 'DELETE' })
    expect(screen.queryByText('Newer')).toBeNull()
    expect(screen.getByText('Older')).toBeTruthy()
  })

  describe('search', () => {
    async function renderWithSnippets() {
      const fetchMock = vi.fn(() => jsonResponse([newer, older]))
      vi.stubGlobal('fetch', fetchMock)
      render(<App />)
      await screen.findByText('Older')
      return { fetchMock, search: screen.getByLabelText('Search') as HTMLInputElement }
    }

    it('narrows the list by case-insensitive substring of title or language', async () => {
      const { fetchMock, search } = await renderWithSnippets()

      fireEvent.change(search, { target: { value: 'NEW' } })
      let items = screen.getAllByRole('listitem')
      expect(items).toHaveLength(1)
      expect(items[0].textContent).toContain('Newer')

      fireEvent.change(search, { target: { value: 'pyth' } })
      items = screen.getAllByRole('listitem')
      expect(items).toHaveLength(1)
      expect(items[0].textContent).toContain('Older')

      expect(fetchMock).toHaveBeenCalledTimes(1)
    })

    it('does not search code', async () => {
      const { search } = await renderWithSnippets()
      fireEvent.change(search, { target: { value: 'print' } })
      expect(screen.queryAllByRole('listitem')).toHaveLength(0)
    })

    it('clearing the box restores the full list', async () => {
      const { search } = await renderWithSnippets()
      fireEvent.change(search, { target: { value: 'new' } })
      expect(screen.getAllByRole('listitem')).toHaveLength(1)

      fireEvent.change(search, { target: { value: '' } })
      expect(screen.getAllByRole('listitem')).toHaveLength(2)
      expect(screen.queryByText('No snippets match.')).toBeNull()
    })

    it('shows a no-match message when nothing matches', async () => {
      const { search } = await renderWithSnippets()
      expect(screen.queryByText('No snippets match.')).toBeNull()

      fireEvent.change(search, { target: { value: 'rust' } })
      expect(screen.queryAllByRole('listitem')).toHaveLength(0)
      expect(screen.getByText('No snippets match.')).toBeTruthy()
    })
  })
})
