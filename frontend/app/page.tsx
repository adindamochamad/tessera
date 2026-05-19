import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="max-w-4xl text-center space-y-8">
        <div className="space-y-4">
          <h1 className="text-6xl font-bold tracking-tight">
            Tessera
          </h1>
          <p className="text-2xl text-muted-foreground">
            AI-Powered Multi-Tenant Data Isolation Auditor
          </p>
        </div>
        
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Autonomous agent yang mengaudit database multi-tenant untuk detect 
          isolation violations sebelum menyebabkan data breaches atau compliance failures.
        </p>
        
        <div className="flex gap-4 justify-center pt-8">
          <Link 
            href="/dashboard"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors font-medium"
          >
            Buka Dashboard
          </Link>
          <Link 
            href="/docs"
            className="px-6 py-3 border border-border rounded-lg hover:bg-accent transition-colors font-medium"
          >
            Dokumentasi
          </Link>
        </div>
        
        <div className="pt-12 grid grid-cols-3 gap-8 text-left">
          <div className="space-y-2">
            <div className="text-4xl font-bold text-primary">0</div>
            <div className="text-sm text-muted-foreground">Violations Detected</div>
          </div>
          <div className="space-y-2">
            <div className="text-4xl font-bold text-primary">100</div>
            <div className="text-sm text-muted-foreground">Compliance Score</div>
          </div>
          <div className="space-y-2">
            <div className="text-4xl font-bold text-primary">0</div>
            <div className="text-sm text-muted-foreground">Audits Run</div>
          </div>
        </div>
      </div>
    </main>
  )
}
