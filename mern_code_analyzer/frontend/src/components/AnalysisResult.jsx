import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { motion } from 'framer-motion';
import { CheckCircle, Bug, Clock, HardDrive, Sparkles, Code, Copy, Check } from 'lucide-react';

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 300, damping: 24 } }
};

export default function AnalysisResult({ result, language }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(result.improvedCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const sections = [
    {
      title: "Correctness",
      icon: <CheckCircle className="w-5 h-5 text-green-400" />,
      content: result.correctness,
      glow: "hover:shadow-green-500/10",
      border: "border-green-500/20"
    },
    {
      title: "Bugs & Errors",
      icon: <Bug className="w-5 h-5 text-red-400" />,
      content: result.bugs && result.bugs.length > 0 ? (
        <ul className="list-disc list-inside space-y-1">
          {result.bugs.map((bug, i) => <li key={i}>{bug}</li>)}
        </ul>
      ) : "No bugs found! Clean code.",
      glow: "hover:shadow-red-500/10",
      border: "border-red-500/20"
    },
    {
      title: "Time Complexity",
      icon: <Clock className="w-5 h-5 text-blue-400" />,
      content: result.timeComplexity,
      glow: "hover:shadow-blue-500/10",
      border: "border-blue-500/20"
    },
    {
      title: "Space Complexity",
      icon: <HardDrive className="w-5 h-5 text-purple-400" />,
      content: result.spaceComplexity,
      glow: "hover:shadow-purple-500/10",
      border: "border-purple-500/20"
    },
    {
      title: "Optimization",
      icon: <Sparkles className="w-5 h-5 text-yellow-400" />,
      content: result.optimization,
      glow: "hover:shadow-yellow-500/10",
      border: "border-yellow-500/20"
    },
    {
      title: "Code Quality",
      icon: <Code className="w-5 h-5 text-teal-400" />,
      content: result.codeQuality,
      glow: "hover:shadow-teal-500/10",
      border: "border-teal-500/20"
    }
  ];

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sections.map((section, idx) => (
          <motion.div 
            key={idx} 
            variants={item}
            className={`relative group bg-dark-800/40 p-5 rounded-2xl border border-white/5 transition-all duration-300 hover:bg-dark-800/80 ${section.glow} shadow-lg`}
          >
            {/* Top glowing line indicator */}
            <div className={`absolute top-0 left-6 right-6 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:via-white/40 transition-all duration-500`} />
            
            <div className="flex items-center gap-3 mb-3">
              <div className={`p-2 rounded-lg bg-dark-900 border ${section.border} shadow-inner-light`}>
                {section.icon}
              </div>
              <h3 className="font-semibold text-gray-200 tracking-tight">{section.title}</h3>
            </div>
            <div className="text-sm text-gray-400 leading-relaxed font-light">
              {section.content}
            </div>
          </motion.div>
        ))}
      </div>

      {result.improvedCode && (
        <motion.div variants={item} className="mt-6 rounded-2xl border border-white/10 overflow-hidden bg-[#0d0d0f] shadow-2xl relative group">
          <div className="absolute inset-0 bg-gradient-to-b from-primary-500/5 to-transparent pointer-events-none" />
          
          <div className="flex items-center justify-between px-5 py-4 bg-dark-900/80 border-b border-white/5 backdrop-blur-md">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-primary-400" />
              <h3 className="font-medium text-gray-200 text-sm tracking-wide">Improved Code</h3>
            </div>
            <button 
              onClick={handleCopy}
              className="flex items-center gap-2 text-xs bg-dark-800 hover:bg-dark-700 text-gray-300 px-3 py-1.5 rounded-lg transition-all border border-white/5 shadow-inner-light"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5 text-gray-400" />}
              {copied ? <span className="text-green-400">Copied!</span> : 'Copy'}
            </button>
          </div>
          <div className="p-4 text-sm max-h-[400px] overflow-y-auto custom-scrollbar relative z-10">
            <SyntaxHighlighter 
              language={language === 'cpp' ? 'cpp' : language} 
              style={vscDarkPlus}
              customStyle={{ margin: 0, padding: 0, background: 'transparent' }}
            >
              {result.improvedCode}
            </SyntaxHighlighter>
          </div>
        </motion.div>
      )}
      
    </motion.div>
  );
}
