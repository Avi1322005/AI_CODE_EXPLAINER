import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { History, Code2, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get('/analyze/history');
        setHistory(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="h-full flex flex-col">
      <header className="mb-8">
        <h1 className="text-3xl font-display font-bold text-black dark:text-white tracking-tight">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">View your past code analyses and scores.</p>
      </header>

      {loading ? (
        <div className="flex-1 flex items-center justify-center text-lightPrimary-500 dark:text-primary-500">Loading history...</div>
      ) : history.length === 0 ? (
        <div className="flex-1 glass-panel rounded-3xl flex flex-col items-center justify-center text-gray-500 border border-gray-200 dark:border-white/5 transition-colors">
          <History className="w-16 h-16 opacity-20 mb-4" />
          <p className="text-lg font-medium text-gray-600 dark:text-gray-400">No analyses yet.</p>
          <Link to="/analyze" className="mt-4 text-lightPrimary-600 dark:text-primary-400 hover:text-lightPrimary-500 dark:hover:text-primary-300">Go write some code!</Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 overflow-y-auto custom-scrollbar pb-6">
          {history.map((item, i) => (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              key={item._id} 
              className="glass-panel p-6 rounded-2xl border border-gray-200 dark:border-white/5 hover:bg-white dark:hover:bg-dark-800/80 transition-all group"
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-2">
                  <Code2 className="w-4 h-4 text-lightPrimary-600 dark:text-primary-400" />
                  <span className="text-xs font-medium uppercase tracking-wider text-gray-600 dark:text-gray-400">{item.language}</span>
                </div>
                <span className="text-xs text-gray-500">{new Date(item.createdAt).toLocaleDateString()}</span>
              </div>
              
              <div className="mb-6">
                <p className="text-sm text-gray-800 dark:text-gray-300 font-mono bg-gray-50 dark:bg-dark-900/50 p-3 rounded-lg border border-gray-200 dark:border-white/5 line-clamp-3 transition-colors">
                  {item.code}
                </p>
              </div>

              <div className="flex items-center justify-between border-t border-gray-200 dark:border-white/5 pt-4 transition-colors">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-yellow-500" />
                  <span className="text-sm font-semibold text-black dark:text-gray-200">Score: {item.result?.score?.total || 'N/A'}/100</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
