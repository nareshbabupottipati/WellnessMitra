import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { sendChatMessage } from '../services/api';
import './ChatInterface.css';

const QUICK_PROMPTS = [
  { label: '💪 Workout Plan', message: 'Create a personalized workout plan for this week' },
  { label: '🥗 Meal Plan', message: 'Design a healthy meal plan for my fitness goal' },
  { label: '📍 Find Gyms', message: 'Find gyms near my location' },
  { label: '📊 My Progress', message: 'Summarize my fitness progress this month' },
  { label: '🧘 Wellness Tips', message: 'Give me tips for stress relief and better sleep' },
];

export default function ChatInterface({ userId }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `👋 **Hi! I'm FitBot, your WellnessMitra AI coach!**\n\nI can help you with:\n- 💪 Personalized workout plans\n- 🥗 Nutrition & meal guidance\n- 📍 Nearby gym discovery\n- 📊 Progress tracking\n- 🧘 Wellness & mental health\n\nWhat would you like help with today?`,
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    const msg = text || input.trim();
    if (!msg || loading) return;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: msg }]);
    setLoading(true);

    try {
      const data = await sendChatMessage(userId, msg, chatHistory);
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      setChatHistory(data.chat_history || []);
    } catch (error) {
      const status = error.response?.status;
      const detail = error.response?.data?.detail;
      let content = '⚠️ Could not connect to FitBot. Please check your connection and try again.';
      if (status === 404) {
        content = '⚠️ This profile is no longer saved. Return to the start and create it again.';
      } else if (typeof detail === 'string') {
        content = `⚠️ ${detail}`;
      }
      setMessages(prev => [...prev, { role: 'assistant', content }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-header">
        <div className="chat-avatar">🤖</div>
        <div>
          <div className="chat-title">FitBot</div>
          <div className="chat-subtitle">Your AI Fitness Coach • WellnessMitra</div>
        </div>
        <div className="online-dot" />
      </div>

      <div className="messages-container">
        {messages.map((msg, i) => (
          <div key={i} className={`message-row ${msg.role}`}>
            {msg.role === 'assistant' && <div className="msg-avatar">🤖</div>}
            <div className={`message-bubble ${msg.role}`}>
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
            {msg.role === 'user' && <div className="msg-avatar user-avatar">👤</div>}
          </div>
        ))}
        {loading && (
          <div className="message-row assistant">
            <div className="msg-avatar">🤖</div>
            <div className="message-bubble assistant typing">
              <span /><span /><span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="quick-prompts">
        {QUICK_PROMPTS.map((qp, i) => (
          <button key={i} className="quick-btn" onClick={() => sendMessage(qp.message)}>
            {qp.label}
          </button>
        ))}
      </div>

      <div className="input-area">
        <input
          className="chat-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
          placeholder="Ask FitBot anything about fitness, nutrition, or wellness..."
          disabled={loading}
        />
        <button className="send-btn" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
          {loading ? '⏳' : '➤'}
        </button>
      </div>
    </div>
  );
}
