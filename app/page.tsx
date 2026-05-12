import OptionsList from '@/components/OptionsList'

export default function Home() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex flex-col items-center gap-6 text-center">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
          Decisor
        </h1>
        <p className="text-lg text-zinc-500 dark:text-zinc-400">
          El sorteador de opciones cuando no podés decidir
        </p>
        <div className="mt-4 w-96 rounded-2xl border border-zinc-200 p-4 dark:border-zinc-800">
          <OptionsList />
        </div>
      </main>
    </div>
  );
}
