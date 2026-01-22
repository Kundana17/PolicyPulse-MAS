import React, { useState } from 'react';
import axios from 'axios';

const FeedbackForm = ({ query }) => {
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const userOpinion = e.target.opinion.value;

        try {
            await axios.post('http://127.0.0.1:8000/feedback', {
                policy_name: query,
                state: "Manual Entry",
                user_opinion: userOpinion
            });

            setSubmitted(true);
        } catch (error) {
            console.error("Feedback submission failed:", error);
            alert("Failed to send feedback. Is the backend running on port 8000?");
        } finally {
            setLoading(false);
        }
    };

    if (submitted) {
        return (
            <div className="bg-emerald-500/10 border border-emerald-500/20 p-8 rounded-3xl text-center animate-in fade-in zoom-in duration-500">
                <p className="text-emerald-400 font-bold">✅ Thank you! Our analysts will review this entry.</p>
            </div>
        );
    }

    return (
        <div className="bg-[#1e293b] border border-slate-700/50 p-8 md:p-12 rounded-3xl shadow-2xl text-center">
            <div className="text-5xl mb-6">🚫</div>
            <h2 className="text-2xl md:text-3xl font-black text-white uppercase tracking-tight">
                Policy Record Not Found
            </h2>

            {/* NEW: Nice limitation disclaimer */}
            <div className="mt-4 max-w-md mx-auto">
                <p className="text-slate-400 font-mono text-[11px] leading-relaxed tracking-wide uppercase opacity-80">
                    PolicyPulse is currently in <span className="text-blue-400">Phase 1 (Beta)</span>. Our intelligence
                    engine is currently indexed with flagship national schemes and select state-level logs.
                    If a record is missing, please alert our agents below.
                </p>
            </div>

            <form onSubmit={handleSubmit} className="mt-10 space-y-6 max-w-md mx-auto">
                <div className="text-left">
                    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest ml-1">Missing Policy Name</label>
                    <input
                        className="w-full mt-2 bg-[#0f172a] border border-slate-700 rounded-xl p-4 text-white outline-none opacity-50 cursor-not-allowed"
                        value={query}
                        readOnly
                    />
                </div>

                <div className="text-left">
                    <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest ml-1">Your Context / Need</label>
                    <textarea
                        name="opinion"
                        required
                        className="w-full mt-2 bg-[#0f172a] border border-slate-700 rounded-xl p-4 h-32 text-white outline-none focus:ring-2 focus:ring-blue-500 resize-none transition-all"
                        placeholder="Tell us what you were looking for..."
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-4 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white font-black rounded-xl transition-all uppercase tracking-widest text-sm shadow-lg shadow-blue-900/20"
                >
                    {loading ? "Transmitting..." : "Submit for Indexing"}
                </button>
            </form>
        </div>
    );
};

export default FeedbackForm;