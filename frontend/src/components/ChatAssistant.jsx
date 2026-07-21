import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

export default function ChatAssistant({ station, forecast, attribution, recommendation }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: `Hello! I am the AQI Sentinel AI Advisor. I'm currently analyzing the data for **${station.name}**. How can I help you today?` }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  // Reset chat when station changes
  useEffect(() => {
    setMessages([
      { role: 'assistant', content: `Hello! I am the AQI Sentinel AI Advisor. I'm currently analyzing the data for **${station.name}**. How can I help you today?` }
    ]);
  }, [station.id]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const payload = {
        message: userMessage,
        station_id: station.id,
        station_name: station.name,
        forecast_data: forecast ? forecast.series : null,
        attribution_data: attribution,
        recommendations: recommendation ? [recommendation.intervention, ...recommendation.warnings] : null
      };

      const res = await axios.post(`https://etaihackathon.onrender.com/api/chat/${station.id}`, payload);
      
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I am having trouble connecting to the AI API. Please make sure your `LLM_API_KEY` is configured in Render." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <button 
        className="chat-fab glass-panel animate-fade-in"
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          display: isOpen ? 'none' : 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          cursor: 'pointer',
          padding: 0,
          zIndex: 1000,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          background: 'linear-gradient(135deg, rgba(96, 165, 250, 0.2) 0%, rgba(167, 139, 250, 0.2) 100%)',
          backdropFilter: 'blur(12px)'
        }}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div 
          className="chat-window glass-panel animate-fade-in"
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            width: '380px',
            height: '500px',
            display: 'flex',
            flexDirection: 'column',
            padding: 0,
            overflow: 'hidden',
            zIndex: 1000,
            boxShadow: '0 12px 48px rgba(0,0,0,0.6)',
            border: '1px solid rgba(255,255,255,0.1)'
          }}
        >
          {/* Header */}
          <div style={{
            padding: '16px',
            borderBottom: '1px solid rgba(255,255,255,0.05)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            background: 'rgba(0,0,0,0.2)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 8px #10b981' }}></div>
              <strong style={{ fontSize: '15px' }}>AI Advisor</strong>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>

          {/* Messages */}
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px'
          }}>
            {messages.map((msg, idx) => (
              <div key={idx} style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '85%',
                background: msg.role === 'user' ? 'rgba(96, 165, 250, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                padding: '10px 14px',
                borderRadius: msg.role === 'user' ? '12px 12px 2px 12px' : '12px 12px 12px 2px',
                fontSize: '14px',
                lineHeight: '1.5',
                border: msg.role === 'user' ? '1px solid rgba(96, 165, 250, 0.3)' : '1px solid rgba(255, 255, 255, 0.05)'
              }}>
                {msg.role === 'user' ? (
                  msg.content
                ) : (
                  <div className="markdown-body" style={{ color: 'var(--text-primary)' }}>
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div style={{ alignSelf: 'flex-start', padding: '10px 14px', background: 'rgba(255,255,255,0.05)', borderRadius: '12px 12px 12px 2px' }}>
                <span className="typing-dot">.</span><span className="typing-dot">.</span><span className="typing-dot">.</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSend} style={{
            padding: '12px',
            borderTop: '1px solid rgba(255,255,255,0.05)',
            display: 'flex',
            gap: '8px',
            background: 'rgba(0,0,0,0.2)'
          }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about this grid..."
              style={{
                flex: 1,
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '20px',
                padding: '8px 16px',
                color: '#fff',
                outline: 'none',
                fontSize: '14px'
              }}
            />
            <button type="submit" disabled={isLoading || !input.trim()} style={{
              background: 'transparent',
              border: 'none',
              color: (isLoading || !input.trim()) ? 'var(--text-secondary)' : '#60a5fa',
              cursor: (isLoading || !input.trim()) ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '0 8px'
            }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
