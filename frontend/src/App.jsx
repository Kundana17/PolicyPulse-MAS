import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import AgentLoadingOverlay from './components/AgentLoadingOverlay';
import FeedbackForm from './components/FeedbackForm';

function App() {
  const [query, setQuery] = useState('');
  const [sector, setSector] = useState('Agriculture');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const startAnalysis = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/analyze', {
        text: query,
        sector: sector
      });

      setTimeout(() => {
        setResult(response.data);
        setLoading(false);
      }, 3500);
    } catch (error) {
      console.error("Agent Handoff Failed:", error);
      alert("Backend unreachable. Check if FastAPI is running on port 8000.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 flex flex-col md:flex-row font-sans overflow-x-hidden">

      {loading && <AgentLoadingOverlay sector={sector} />}

      {/* REFINED SIDEBAR: Narrower on tablets (w-64) to save space */}
      <aside className="w-full md:w-64 lg:w-80 bg-[#1e293b] p-5 md:p-6 border-b md:border-b-0 md:border-r border-slate-700 flex flex-col shrink-0">
        <div className="mb-6 md:mb-8">
          <h1 className="text-xl md:text-2xl font-black text-blue-400 tracking-tight flex items-center gap-2">
            <span className="text-2xl md:text-3xl">🧬</span> PolicyPulse
          </h1>
          <p className="text-[9px] md:text-[10px] text-slate-500 font-mono mt-1 tracking-widest uppercase">Civic Intelligence MAS</p>
        </div>

        <div className="space-y-5 md:space-y-6 flex-1">
          <div>
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Sector Filter</label>
            <select
              className="w-full mt-2 bg-[#0f172a] border border-slate-700 rounded-lg p-2.5 md:p-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              value={sector}
              onChange={(e) => setSector(e.target.value)}
            >
              {["Agriculture", "Energy", "Healthcare", "Finance", "Education", "Infrastructure"].map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Natural Language Query</label>
            <textarea
              className="w-full mt-2 bg-[#0f172a] border border-slate-700 rounded-lg p-2.5 md:p-3 h-28 md:h-40 text-sm outline-none focus:ring-2 focus:ring-blue-500 resize-none placeholder-slate-600"
              placeholder="e.g., 'Diversification'..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <button
            onClick={startAnalysis}
            disabled={loading || !query}
            className="w-full py-3.5 md:py-4 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 rounded-xl font-bold text-white shadow-lg shadow-blue-900/20 transition-all active:scale-95 text-sm"
          >
            Run Impact Analysis
          </button>
        </div>
      </aside>

      {/* REFINED DASHBOARD: Reduced padding for tablets (p-4 to p-6) */}
      <main className="flex-1 p-4 sm:p-6 md:p-8 lg:p-10 overflow-y-auto bg-linear-to-br from-[#0f172a] to-[#1e293b]">
        {!result ? (
          <div className="h-full flex flex-col items-center justify-center opacity-30 py-20">
            <div className="text-6xl md:text-7xl mb-6">🏛️</div>
            <p className="font-mono uppercase tracking-[0.4em] text-xs md:text-sm text-center">
              System Idle: Awaiting Handoff
            </p>
          </div>
        ) : result.error || result.status === "no_results" ? (
          /* THIS IS THE NEW SECTION */
          <div className="max-w-4xl mx-auto pt-6 md:pt-10 px-4">
            <FeedbackForm query={query} />
          </div>
        ) : (
          <div className="max-w-4xl lg:max-w-5xl mx-auto space-y-6 md:space-y-8 animate-in fade-in slide-in-from-bottom-6 duration-1000">

            {/* AGENT 1: ARCHIVIST */}
            <div className="bg-[#1e293b]/50 backdrop-blur-md p-6 md:p-8 rounded-2xl md:rounded-3xl border border-blue-500/20 shadow-2xl">
              <div className="flex items-center gap-2 mb-3 text-blue-400 font-bold text-[10px] uppercase tracking-widest">
                <span className="animate-pulse">●</span> {result.status === "fallback_match" ? "Fallback Suggestion" : "Archivist Match Found"}
              </div>

              {/* If the policy is from a different state, show this warning first */}
              {result.status === "fallback_match" && (
                <div className="mb-4 p-3 bg-orange-500/10 border border-orange-500/20 rounded-lg">
                  <p className="text-orange-400 text-xs font-mono">
                    ⚠️ {result.message}
                  </p>
                </div>
              )}

              <h2 className="text-xl sm:text-2xl md:text-4xl font-black text-white leading-tight">
                {result?.policy?.title || result?.policy}
              </h2>
            </div>

            {/* AGENT 2: AUDITOR - Grid logic for better tablet flow */}
            {result?.analysis && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4 md:gap-8">
                {/* AGENT 2: AUDITOR */}
                {/* AGENT 2: AUDITOR */}
                <div className="bg-[#1e293b] p-6 md:p-8 rounded-2xl md:rounded-3xl border border-slate-700/50 shadow-xl">

                  {/* Header with Dynamic Status Color */}
                  <div className="text-slate-500 text-[9px] font-bold uppercase tracking-widest mb-6 flex justify-between">
                    <span>Auditor Metrics</span>
                    <span className={result.analysis.DriftScore === 0 ? "text-emerald-400" : "text-orange-400"}>
                      {result.analysis.DriftScore === 0 ? "STATUS: IN SYNC" : `DRIFT SCORE: ${result.analysis.DriftScore}`}
                    </span>
                  </div>

                  {/* Main Score Display - Unified Logic */}
                  <div className="flex items-center gap-4 mb-4">
                    <h2 className={`text-6xl font-black tracking-tighter ${result.analysis.DriftScore === 0 ? "text-emerald-500" : "text-orange-500"}`}>
                      {result.analysis.DriftScore === 0 ? "100%" : `${(result.analysis.DriftScore * 100).toFixed(0)}%`}
                    </h2>

                    <div className="flex flex-col">
                      <span className={`text-xl font-bold ${result.analysis.DriftScore === 0 ? "text-emerald-500" : "text-orange-500"}`}>
                        {result.analysis.DriftScore === 0 ? "In Sync" : "Drift"}
                      </span>
                      <div className={`text-[10px] font-black px-2 py-0.5 rounded-full mt-1 ${result.analysis.DriftScore === 0 ? 'bg-emerald-500/10 text-emerald-500' : 'bg-orange-500/10 text-orange-500'}`}>
                        {result.analysis.DriftScore === 0 ? 'OK' : 'DRIFT'}
                      </div>
                    </div>
                  </div>

                  {/* Explanation Text */}
                  <p className="mt-6 text-xs md:text-sm text-slate-400 leading-relaxed font-medium pt-6 border-t border-slate-800">
                    {result.analysis.Explanation || "Aligning intent with live field impact data..."}
                  </p>
                </div>

                <div className="bg-[#1e293b] p-6 md:p-8 rounded-2xl md:rounded-3xl border border-slate-700/50 shadow-xl flex flex-col justify-between text-white">
                  <div>
                    <div className="text-slate-500 text-[9px] font-bold uppercase tracking-widest mb-4">Focus Region</div>
                    <div className="text-xl md:text-3xl font-bold mb-2">{result.analysis.Region || "National Coverage"}</div>
                    <span className="text-[9px] bg-blue-600/20 text-blue-400 px-2.5 py-1 rounded-full font-bold uppercase tracking-wider">Live Field Data</span>
                  </div>
                  <div className="mt-8 p-3.5 bg-[#0f172a]/60 rounded-2xl border border-slate-800">
                    <p className="text-[9px] text-slate-500 font-bold uppercase mb-1">Source Authority</p>
                    <p className="text-[11px] text-blue-300 italic font-mono truncate">{result.analysis.source_authority || "Ministry Records"}</p>
                  </div>
                </div>
              </div>
            )}

            {/* AGENT 3: STRATEGIST */}
            <div className="bg-white rounded-3xl shadow-2xl overflow-hidden border border-blue-200">
              <div className="bg-blue-600 px-6 md:px-8 py-4 flex items-center justify-between">
                <h3 className="font-black text-white text-sm md:text-lg flex items-center gap-3">
                  <span>⚡</span> Strategist Engine
                </h3>
                <span className="text-[9px] bg-white/20 text-white px-2.5 py-1 rounded-full font-mono font-bold uppercase">Llama-3</span>
              </div>
              <div className="p-6 md:p-10 text-slate-800">
                <div className="prose prose-sm md:prose-base lg:prose-lg prose-slate max-w-none">
                  <ReactMarkdown>
                    {result?.strategy}
                  </ReactMarkdown>
                </div>
              </div>
            </div>

            <footer className="flex flex-col sm:flex-row justify-between items-center gap-3 text-[9px] text-slate-600 font-mono uppercase tracking-[0.2em] pb-8">
              <span>Agentic Trace: Verified</span>
              <span>Ref: MAS-PP-2026</span>
            </footer>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;