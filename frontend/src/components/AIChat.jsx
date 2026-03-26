import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { sendChatMessage, fetchChatContext } from '../api';
import { useToast } from '../components/ToastProvider';

export default function AIChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hi! I'm your AI nutrition coach. Ask me about meals, swap suggestions, or your daily progress!" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [context, setContext] = useState(null);
  const messagesEndRef = useRef(null);
  const toast = useToast();

  useEffect(() => {
    fetchChatContext()
      .then(setContext)
      .catch(console.error);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function handleSend() {
    if (!input.trim() || loading) return;
    
    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await sendChatMessage(userMessage, messages);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.response,
        suggestions: response.meal_suggestions
      }]);
    } catch (err) {
      toast.error('Chat failed');
    }
    setLoading(false);
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <>
      {/* Floating Bubble */}
      <motion.button
        className="fixed bottom-4 right-4 w-14 h-14 rounded-full bg-[var(--primary-container)] text-[var(--surface)] shadow-neon flex items-center justify-center z-[70]"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(true)}
        style={{ boxShadow: '0 0 20px rgba(57, 255, 20, 0.3)' }}
      >
        <span className="material-icons-outlined">chat</span>
      </motion.button>

      {/* Chat Sidebar */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed top-0 right-0 w-full max-w-md h-full bg-[var(--surface-container)] border-l border-[var(--surface-container-high)] shadow-2xl z-[70] flex flex-col"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-[var(--surface-container-high)]">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[var(--primary-container)] flex items-center justify-center">
                  <span className="material-icons-outlined text-[var(--surface)]">psychology</span>
                </div>
                <div>
                  <h3 className="font-semibold text-[var(--on-surface)]">AI Coach</h3>
                  <p className="text-xs text-[var(--on-surface-variant)]">
                    {context ? `${context.calories_remaining} cal remaining` : 'Loading...'}
                  </p>
                </div>
              </div>
              <button 
                onClick={() => setIsOpen(false)}
                className="p-2 rounded-lg hover:bg-[var(--surface-container-high)] transition-colors"
              >
                <span className="material-icons-outlined text-[var(--on-surface-variant)]">close</span>
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] p-3 rounded-2xl ${
                    msg.role === 'user' 
                      ? 'bg-[var(--primary-container)] text-[var(--surface)]' 
                      : 'bg-[var(--surface-container-high)] text-[var(--on-surface)]'
                  }`}>
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    {msg.suggestions && (
                      <div className="mt-3 pt-3 border-t border-[var(--surface)]/20">
                        <p className="text-xs font-medium mb-2 text-[var(--primary-container)]">Try these alternatives:</p>
                        {msg.suggestions.map((sug, j) => (
                          <div key={j} className="text-xs py-1 opacity-80">
                            • {sug.name} ({sug.serving_size_g}g): {sug.calories} cal
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-[var(--surface-container-high)] p-3 rounded-2xl">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 rounded-full bg-[var(--on-surface-variant)] animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 rounded-full bg-[var(--on-surface-variant)] animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 rounded-full bg-[var(--on-surface-variant)] animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-[var(--surface-container-high)]">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about meals, swaps..."
                  className="flex-1 bg-[var(--surface-container)] rounded-xl px-4 py-3 text-[var(--on-surface)] placeholder:text-[var(--on-surface-variant)] border border-transparent focus:border-[var(--primary-container)] outline-none transition-colors"
                />
                <button
                  onClick={handleSend}
                  disabled={loading || !input.trim()}
                  className="p-3 rounded-xl bg-[var(--primary-container)] text-[var(--surface)] disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[var(--primary-fixed-dim)] transition-colors"
                >
                  <span className="material-icons-outlined">send</span>
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}