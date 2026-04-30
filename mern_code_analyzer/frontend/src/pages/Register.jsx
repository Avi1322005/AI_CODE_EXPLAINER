import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { Sparkles, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(name, email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-gray-50 dark:bg-[#000000] transition-colors duration-300">
      <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-gray-200/50 dark:bg-primary-600/10 blur-[120px] pointer-events-none transition-colors" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[30%] h-[40%] rounded-full bg-gray-200/50 dark:bg-purple-600/10 blur-[120px] pointer-events-none transition-colors" />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel w-full max-w-md p-8 rounded-3xl relative z-10"
      >
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-lightPrimary-500 dark:bg-primary-500 rounded-xl blur shadow-glow shadow-lightPrimary-500/50 dark:shadow-primary-500/50" />
            <div className="relative bg-white dark:bg-dark-900 border border-gray-200 dark:border-white/10 p-3 rounded-xl transition-colors">
              <Sparkles className="w-6 h-6 text-lightPrimary-600 dark:text-primary-400" />
            </div>
          </div>
        </div>
        <h2 className="text-3xl font-display font-bold text-center text-black dark:text-white mb-2">Create Account</h2>
        <p className="text-gray-600 dark:text-gray-400 text-center mb-8">Start analyzing your code like a pro</p>

        {error && <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-sm mb-6 text-center">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Full Name</label>
            <input 
              type="text" required
              value={name} onChange={(e) => setName(e.target.value)}
              className="w-full bg-white dark:bg-dark-900 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-black dark:text-white focus:outline-none focus:border-lightPrimary-500 dark:focus:border-primary-500 focus:ring-1 focus:ring-lightPrimary-500 dark:focus:ring-primary-500 transition-all shadow-inner-light"
              placeholder="John Doe"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Email Address</label>
            <input 
              type="email" required
              value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-white dark:bg-dark-900 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-black dark:text-white focus:outline-none focus:border-lightPrimary-500 dark:focus:border-primary-500 focus:ring-1 focus:ring-lightPrimary-500 dark:focus:ring-primary-500 transition-all shadow-inner-light"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Password</label>
            <input 
              type="password" required
              value={password} onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-white dark:bg-dark-900 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-black dark:text-white focus:outline-none focus:border-lightPrimary-500 dark:focus:border-primary-500 focus:ring-1 focus:ring-lightPrimary-500 dark:focus:ring-primary-500 transition-all shadow-inner-light"
              placeholder="••••••••"
            />
          </div>
          <button 
            type="submit" disabled={loading}
            className="w-full relative group disabled:opacity-50 mt-6"
          >
            <div className="absolute inset-0 bg-lightPrimary-600 dark:bg-primary-600 rounded-xl blur shadow-glow shadow-lightPrimary-500/40 dark:shadow-primary-500/40 group-hover:shadow-lightPrimary-500/60 dark:group-hover:shadow-primary-500/60 transition-all" />
            <div className="relative flex items-center justify-center gap-2 bg-lightPrimary-500 hover:bg-lightPrimary-600 dark:bg-primary-600 dark:hover:bg-primary-500 text-white px-6 py-3 rounded-xl font-medium transition-all shadow-inner-light">
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Sign Up'}
            </div>
          </button>
        </form>
        <p className="text-center text-gray-600 dark:text-gray-400 text-sm mt-8">
          Already have an account? <Link to="/login" className="text-lightPrimary-600 dark:text-primary-400 hover:text-lightPrimary-500 dark:hover:text-primary-300 transition-colors">Sign in</Link>
        </p>
      </motion.div>
    </div>
  );
}
