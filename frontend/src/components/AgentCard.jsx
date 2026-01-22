import React from 'react';

const AgentCard = ({ title, role, icon, isActive, isComplete, dependency, children }) => {
  return (
    <div className={`relative transition-all duration-700 transform ${
      isActive ? 'scale-[1.02] opacity-100' : isComplete ? 'opacity-100' : 'opacity-30'
    }`}>
      {/* Connector Line for Sequence Logic */}
      <div className="absolute -left-8 top-10 w-0.5 h-full bg-slate-800"></div>
      
      <div className={`p-6 rounded-2xl border-2 shadow-2xl ${
        isActive ? 'bg-[#1e293b] border-blue-500 shadow-blue-900/10' : 
        'bg-[#0f172a] border-slate-800'
      }`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <span className="text-3xl p-3 bg-slate-800 rounded-xl">{icon}</span>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-black text-white text-lg">{title}</h3>
                {isComplete && <span className="text-green-500 text-xs font-bold uppercase tracking-widest">● Active</span>}
              </div>
              <p className="text-blue-400 text-[10px] font-bold uppercase tracking-widest">Role: {role}</p>
            </div>
          </div>
          
          {dependency && (
            <div className="bg-[#0f172a] px-3 py-1 rounded-md border border-slate-800">
              <span className="text-[10px] font-mono text-slate-500 uppercase">Input: {dependency}</span>
            </div>
          )}
        </div>

        <div className="relative z-10">
          {children}
        </div>

        {isActive && (
          <div className="mt-4 flex gap-1">
            <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
            <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentCard;