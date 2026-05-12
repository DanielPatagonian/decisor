'use client'

import { useState, useRef } from 'react'

export default function OptionsList() {
  const [options, setOptions] = useState<string[]>([])
  const [inputValue, setInputValue] = useState('')
  const [showDuplicate, setShowDuplicate] = useState(false)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  function addOption() {
    const trimmed = inputValue.trim()
    if (!trimmed) return

    if (options.some(o => o.toLowerCase() === trimmed.toLowerCase())) {
      if (timerRef.current) clearTimeout(timerRef.current)
      setShowDuplicate(true)
      timerRef.current = setTimeout(() => setShowDuplicate(false), 2000)
      return
    }

    setOptions(prev => [...prev, trimmed])
    setInputValue('')
  }

  function removeOption(index: number) {
    setOptions(prev => prev.filter((_, i) => i !== index))
  }

  return (
    <div className="flex flex-col gap-3 w-full">
      <div className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && addOption()}
          placeholder="Agregar una opción..."
          className="flex-1 rounded-lg border border-zinc-200 px-3 py-2 text-sm outline-none focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
        />
        <button
          onClick={addOption}
          className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-700 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-300"
        >
          Agregar
        </button>
      </div>
      {showDuplicate && (
        <p className="text-xs text-red-500">ya existe</p>
      )}
      {options.length === 0 ? (
        <p className="text-sm text-zinc-400 dark:text-zinc-500">Agregá al menos dos opciones para empezar.</p>
      ) : (
        <ul className="flex flex-col gap-1 w-full">
          {options.map((opt, i) => (
            <li key={i} className="flex items-center justify-between rounded-lg bg-zinc-100 px-3 py-2 text-sm dark:bg-zinc-800">
              <span className="text-zinc-800 dark:text-zinc-100">{opt}</span>
              <button
                onClick={() => removeOption(i)}
                className="text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
                aria-label={`Eliminar ${opt}`}
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
