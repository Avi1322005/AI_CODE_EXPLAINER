import React, { useState, useContext } from 'react';
import api from '../api/axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Loader2, Sparkles, AlertCircle, RefreshCw, ChevronDown } from 'lucide-react';
import CodeEditor from '../components/CodeEditor';
import { ThemeContext } from '../context/ThemeContext';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';

const LANGUAGES = [
  { value: 'javascript', label: 'JavaScript' },
  { value: 'python', label: 'Python' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
];

export default function AnalyzerPage() {
  const [code, setCode] = useState('// Paste your code here to begin\\n');
  const [language, setLanguage] = useState('javascript');
  const [isLangOpen, setIsLangOpen] = useState(false);
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('analysis');
  const { isDark } = useContext(ThemeContext);

  const handleAnalyze = async () => {
    if (!code || code.trim() === '') return;
    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const res = await api.post('/analyze/auth', { code, language });
      setResult(res.data);
      setActiveTab('analysis');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const tabs = [
    { id: 'analysis', label: 'Analysis & Score' },
    { id: 'interview', label: 'Interview' },
    { id: 'refactored', label: 'Refactored' },
    { id: 'testcases', label: 'Test Cases' }
  ];

  return (
    <div className="h-full flex flex-col gap-4 relative">
      
      {/* Top Bar */}
      <div className="flex items-center justify-between glass-panel px-6 py-4 rounded-2xl z-20">
        <div className="relative">
          <button 
            onClick={() => setIsLangOpen(!isLangOpen)}
            className="flex items-center gap-2 bg-gray-50 dark:bg-dark-800 border border-gray-200 dark:border-white/5 px-4 py-2 rounded-xl text-sm text-gray-700 dark:text-gray-300 transition-all shadow-sm dark:shadow-inner-light"
          >
            {LANGUAGES.find(l => l.value === language)?.label}
            <ChevronDown className="w-4 h-4 text-gray-500" />
          </button>
          <AnimatePresence>
            {isLangOpen && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 10 }}
                className="absolute top-full left-0 mt-2 w-40 glass-panel rounded-xl overflow-hidden border border-gray-200 dark:border-white/10 shadow-lg"
              >
                {LANGUAGES.map(lang => (
                  <button key={lang.value} onClick={() => { setLanguage(lang.value); setIsLangOpen(false); }} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors">
                    {lang.label}
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <button 
          onClick={handleAnalyze} disabled={isAnalyzing}
          className="relative group disabled:opacity-50"
        >
          <div className="absolute inset-0 bg-lightPrimary-600 dark:bg-primary-600 rounded-xl blur shadow-glow shadow-lightPrimary-500/40 dark:shadow-primary-500/40 group-hover:shadow-lightPrimary-500/60 dark:group-hover:shadow-primary-500/60 transition-all" />
          <div className="relative flex items-center gap-2 bg-lightPrimary-500 dark:bg-primary-600 text-white px-6 py-2.5 rounded-xl font-medium shadow-inner-light overflow-hidden">
            {isAnalyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            <span>{isAnalyzing ? 'Analyzing...' : 'Run Advanced Analysis'}</span>
          </div>
        </button>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row gap-6 min-h-0">
        {/* Editor */}
        <section className="flex-1 glass-panel rounded-2xl overflow-hidden flex flex-col border border-gray-200 dark:border-white/5 shadow-md dark:shadow-2xl relative">
          <div className="bg-gray-100 dark:bg-dark-900/50 px-4 py-3 flex items-center justify-between border-b border-gray-200 dark:border-white/5">
             <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Editor</span>
             <div className="flex gap-1.5"><div className="w-2.5 h-2.5 rounded-full bg-red-500/80"/><div className="w-2.5 h-2.5 rounded-full bg-yellow-500/80"/><div className="w-2.5 h-2.5 rounded-full bg-green-500/80"/></div>
          </div>
          <div className="flex-1 bg-white dark:bg-[#0d0d0f]">
            <CodeEditor code={code} onChange={setCode} language={language} />
          </div>
        </section>

        {/* Output */}
        <section className="flex-[1.2] glass-panel rounded-2xl flex flex-col border border-gray-200 dark:border-white/5 shadow-md dark:shadow-2xl overflow-hidden">
          
          {/* Tabs */}
          <div className="flex px-4 pt-4 border-b border-gray-200 dark:border-white/5 bg-gray-50 dark:bg-dark-900/30 gap-2 overflow-x-auto custom-scrollbar">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2.5 text-sm font-medium rounded-t-lg transition-colors relative ${activeTab === tab.id ? 'text-black dark:text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-300'}`}
              >
                {tab.label}
                {activeTab === tab.id && (
                  <motion.div layoutId="activeTab" className="absolute bottom-0 left-0 right-0 h-0.5 bg-lightPrimary-500 dark:bg-primary-500 shadow-glow shadow-lightPrimary-500 dark:shadow-primary-500" />
                )}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-y-auto p-6 custom-scrollbar relative">
            {isAnalyzing && (
              <div className="absolute inset-0 flex flex-col items-center justify-center text-primary-500 bg-dark-900/50 backdrop-blur-sm z-10">
                <Loader2 className="w-10 h-10 animate-spin mb-4" />
                <p className="animate-pulse">Running advanced AI models...</p>
              </div>
            )}
            
            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl mb-4">
                <AlertCircle className="w-5 h-5 mb-2" />
                <p>{error}</p>
              </div>
            )}

            {!result && !isAnalyzing && !error && (
              <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-50">
                <Sparkles className="w-16 h-16 mb-4" />
                <p>Output will appear here</p>
              </div>
            )}

            {result && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-6 pb-10">
                
                {/* TAB CONTENT: ANALYSIS */}
                {activeTab === 'analysis' && (
                  <>
                    <div className="flex items-center gap-4 bg-white dark:bg-dark-800/50 p-6 rounded-2xl border border-gray-200 dark:border-white/5 transition-colors">
                      <div className="w-20 h-20 rounded-full border-4 border-lightPrimary-500 dark:border-primary-500 flex items-center justify-center shadow-glow shadow-lightPrimary-500/30 dark:shadow-primary-500/30 transition-colors">
                        <span className="text-2xl font-bold text-black dark:text-white">{result.score?.total}</span>
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-black dark:text-white mb-2">Code Score</h3>
                        <div className="grid grid-cols-2 gap-x-6 gap-y-1 text-sm">
                          <span className="text-gray-500 dark:text-gray-400">Correctness: <span className="text-gray-900 dark:text-gray-200 font-medium">{result.score?.correctness}/40</span></span>
                          <span className="text-gray-500 dark:text-gray-400">Efficiency: <span className="text-gray-900 dark:text-gray-200 font-medium">{result.score?.efficiency}/30</span></span>
                          <span className="text-gray-500 dark:text-gray-400">Readability: <span className="text-gray-900 dark:text-gray-200 font-medium">{result.score?.readability}/20</span></span>
                          <span className="text-gray-500 dark:text-gray-400">Best Practices: <span className="text-gray-900 dark:text-gray-200 font-medium">{result.score?.bestPractices}/10</span></span>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white dark:bg-dark-800/50 p-5 rounded-2xl border border-gray-200 dark:border-white/5 transition-colors">
                      <h4 className="text-black dark:text-white font-semibold mb-3 border-b border-gray-200 dark:border-white/5 pb-2">Complexity</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-1"><span className="text-blue-600 dark:text-blue-400 font-mono font-semibold">Time:</span> {result.complexity?.time}</p>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3"><span className="text-purple-600 dark:text-purple-400 font-mono font-semibold">Space:</span> {result.complexity?.space}</p>
                      <p className="text-sm text-gray-500 italic">{result.complexity?.explanation}</p>
                    </div>

                    {result.bugs?.length > 0 && (
                      <div className="bg-red-50 dark:bg-red-900/10 p-5 rounded-2xl border border-red-200 dark:border-red-500/20 transition-colors">
                        <h4 className="text-red-600 dark:text-red-400 font-semibold mb-3 border-b border-red-200 dark:border-red-500/10 pb-2">Detected Bugs</h4>
                        <ul className="space-y-3">
                          {result.bugs.map((b, i) => (
                            <li key={i} className="text-sm">
                              <span className="text-red-600 dark:text-red-300 font-mono bg-red-100 dark:bg-red-900/30 px-2 py-0.5 rounded">Line {b.line}</span>
                              <p className="text-gray-800 dark:text-gray-300 mt-1">{b.issue}</p>
                              <p className="text-green-600 dark:text-green-400 mt-1 font-medium">Fix: {b.fix}</p>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="bg-white dark:bg-dark-800/50 p-5 rounded-2xl border border-gray-200 dark:border-white/5 transition-colors">
                      <h4 className="text-green-600 dark:text-green-400 font-semibold mb-3 border-b border-gray-200 dark:border-white/5 pb-2">Explain Like I'm 5</h4>
                      <p className="text-sm text-gray-800 dark:text-gray-300 leading-relaxed">{result.eli5}</p>
                    </div>

                    <div className="bg-white dark:bg-dark-800/50 p-5 rounded-2xl border border-gray-200 dark:border-white/5 transition-colors">
                      <h4 className="text-yellow-600 dark:text-yellow-400 font-semibold mb-3 border-b border-gray-200 dark:border-white/5 pb-2">Dry Run Simulation</h4>
                      <p className="text-sm text-gray-800 dark:text-gray-300 leading-relaxed">{result.dryRun}</p>
                    </div>
                  </>
                )}

                {/* TAB CONTENT: INTERVIEW */}
                {activeTab === 'interview' && (
                  <div className="space-y-4">
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">The AI interviewer asks you these questions based on your code:</p>
                    {result.interviewQuestions?.map((q, i) => (
                      <div key={i} className="bg-white dark:bg-dark-800/50 p-4 rounded-xl border border-gray-200 dark:border-white/5 shadow-sm dark:shadow-inner-light transition-colors">
                        <p className="text-gray-900 dark:text-gray-200 font-medium">Q: {q}</p>
                      </div>
                    ))}
                  </div>
                )}

                {/* TAB CONTENT: REFACTORED */}
                {activeTab === 'refactored' && (
                  <div>
                    <div className="flex justify-between items-center mb-4">
                      <p className="text-gray-600 dark:text-gray-400 text-sm">Clean, optimized version of your code:</p>
                      <button onClick={() => setCode(result.refactoredCode)} className="flex items-center gap-2 bg-lightPrimary-500/10 dark:bg-primary-600/20 hover:bg-lightPrimary-500/20 dark:hover:bg-primary-600/40 text-lightPrimary-600 dark:text-primary-400 px-3 py-1.5 rounded-lg transition-colors text-sm border border-lightPrimary-500/20 dark:border-primary-500/30">
                        <RefreshCw className="w-4 h-4" /> Apply Fixes to Editor
                      </button>
                    </div>
                    <div className="rounded-xl overflow-hidden border border-gray-200 dark:border-white/5 bg-gray-50 dark:bg-[#0d0d0f] transition-colors">
                      <SyntaxHighlighter language={language === 'cpp' ? 'cpp' : language} style={isDark ? vscDarkPlus : vs} customStyle={{ margin: 0, padding: '16px', background: 'transparent' }}>
                        {result.refactoredCode || '// No refactored code provided'}
                      </SyntaxHighlighter>
                    </div>
                  </div>
                )}

                {/* TAB CONTENT: TEST CASES */}
                {activeTab === 'testcases' && (
                  <div className="space-y-4">
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">Auto-generated edge cases to test your code:</p>
                    <div className="grid gap-4">
                      {result.testCases?.map((tc, i) => (
                        <div key={i} className="bg-white dark:bg-dark-800/50 p-4 rounded-xl border border-gray-200 dark:border-white/5 grid grid-cols-1 md:grid-cols-3 gap-4 transition-colors">
                          <div>
                            <span className="text-xs text-gray-500 uppercase tracking-wider block mb-1">Type</span>
                            <span className="text-sm text-purple-600 dark:text-purple-400 font-medium">{tc.type}</span>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500 uppercase tracking-wider block mb-1">Input</span>
                            <code className="text-sm text-gray-800 dark:text-gray-300 font-mono bg-gray-100 dark:bg-dark-900 px-2 py-1 rounded transition-colors">{tc.input}</code>
                          </div>
                          <div>
                            <span className="text-xs text-gray-500 uppercase tracking-wider block mb-1">Expected Output</span>
                            <code className="text-sm text-green-600 dark:text-green-400 font-mono bg-gray-100 dark:bg-dark-900 px-2 py-1 rounded transition-colors">{tc.expected}</code>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
              </motion.div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
