import React, { useState, useEffect } from 'react';

const AgentLoadingOverlay = ({ sector }) => {
  const steps = [
    { name: "Archivist", task: "Querying Policy Memory in Qdrant..." },
    { name: "Auditor", task: `Analyzing ${sector} Impact Logs...` },
    { name: "Strategist", task: "Synthesizing Cross-Jurisdiction Fixes..." }
  ];

  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev < 2 ? prev + 1 : prev));
    }, 1100);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed inset-0 bg-[#0f172a]/95 backdrop-blur-md z-100 flex flex-col items-center justify-center text-white p-10">
      <div className="w-full max-w-md space-y-8 animate-in fade-in zoom-in duration-300">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
          <h2 className="text-2xl font-black mb-2 tracking-tight">Agent Collaboration</h2>
          <p className="text-slate-400 text-sm font-medium italic">PolicyPulse Multi-Agent System is evaluating data...</p>
        </div>

        <div className="space-y-4">
          {steps.map((step, idx) => (
            <div 
              key={idx} 
              className={`p-5 rounded-2xl border-2 transition-all duration-500 flex items-center justify-between ${
                idx === activeStep 
                  ? 'bg-blue-600/20 border-blue-500 shadow-lg shadow-blue-500/10 scale-105' 
                  : idx < activeStep 
                    ? 'bg-slate-800/50 border-emerald-500/50 opacity-60' 
                    : 'bg-slate-900 border-slate-800 opacity-20'
              }`}
            >
              <div>
                <span className="text-[10px] font-black uppercase tracking-widest text-blue-400">{step.name}</span>
                <p className="font-bold text-sm mt-0.5">{step.task}</p>
              </div>
              {idx < activeStep ? (
                <span className="text-emerald-400 text-xl font-bold animate-in zoom-in">✓</span>
              ) : idx === activeStep ? (
                <div className="flex gap-1">
                  <div className="w-1 h-1 bg-white rounded-full animate-bounce"></div>
                  <div className="w-1 h-1 bg-white rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                </div>
              ) : null}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AgentLoadingOverlay;