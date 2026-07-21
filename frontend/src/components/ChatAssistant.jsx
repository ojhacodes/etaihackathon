import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

export default function ChatAssistant({ station, forecast, attribution, recommendation }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: `Greetings! I am the **AQI Sentinel AI**. I have fully analyzed the live environmental data for **${station.name}**. How can I assist you with mitigation strategies today?` }
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
      { role: 'assistant', content: `Greetings! I am the **AQI Sentinel AI**. I have fully analyzed the live environmental data for **${station.name}**. How can I assist you with mitigation strategies today?` }
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
        recommendations: recommendation ? [recommendation.action, JSON.stringify(recommendation.advisories)] : null
      };

      const res = await axios.post(`https://etaihackathon.onrender.com/api/chat/${station.id}`, payload);
      
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Network error: Unable to reach the AI API." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Premium Floating Action Button */}
      <button 
        className="chat-fab glass-panel"
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed',
          bottom: '32px',
          right: '32px',
          width: '64px',
          height: '64px',
          borderRadius: '50%',
          display: isOpen ? 'none' : 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          cursor: 'pointer',
          padding: 0,
          zIndex: 1000,
          boxShadow: '0 8px 32px rgba(59, 130, 246, 0.4), inset 0 0 0 1px rgba(255,255,255,0.2)',
          border: 'none',
          background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
          animation: 'pulse-glow 3s infinite',
        }}
      >
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          <path d="M12 8v4"></path>
          <path d="M12 16h.01"></path>
        </svg>
      </button>

      {/* Premium Chat Window */}
      {isOpen && (
        <div 
          className="chat-window glass-panel animate-fade-in"
          style={{
            position: 'fixed',
            bottom: '32px',
            right: '32px',
            width: '400px',
            height: '600px',
            display: 'flex',
            flexDirection: 'column',
            padding: 0,
            overflow: 'hidden',
            zIndex: 1000,
            boxShadow: '0 24px 64px rgba(0,0,0,0.6), inset 0 0 0 1px rgba(255,255,255,0.1)',
            border: 'none',
            background: 'rgba(15, 17, 26, 0.85)',
            backdropFilter: 'blur(20px)',
            borderRadius: '24px'
          }}
        >
          {/* Vibrant Header */}
          <div style={{
            padding: '20px 24px',
            background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%)',
            borderBottom: '1px solid rgba(255,255,255,0.08)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ 
                width: '10px', height: '10px', borderRadius: '50%', 
                background: '#10b981', boxShadow: '0 0 12px #10b981',
                animation: 'pulse-glow-green 2s infinite' 
              }}></div>
              <div>
                <strong style={{ fontSize: '16px', display: 'block', color: '#fff' }}>Sentinel AI</strong>
                <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>OSS 70B Advisor</span>
              </div>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              style={{ 
                background: 'rgba(255,255,255,0.1)', border: 'none', 
                color: '#fff', cursor: 'pointer', borderRadius: '50%',
                width: '32px', height: '32px', display: 'flex', alignItems: 'center', justifyContent: 'center',
                transition: 'background 0.2s'
              }}
              onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.2)'}
              onMouseOut={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.1)'}
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>

          {/* Messages Area */}
          <div className="chat-messages-scroll" style={{
            flex: 1,
            overflowY: 'auto',
            padding: '24px',
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
            scrollBehavior: 'smooth'
          }}>
            {messages.map((msg, idx) => (
              <div key={idx} style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '85%',
                display: 'flex',
                flexDirection: 'column',
                gap: '4px'
              }}>
                <span style={{ 
                  fontSize: '11px', color: 'var(--text-secondary)', 
                  alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  textTransform: 'uppercase', letterSpacing: '1px'
                }}>
                  {msg.role === 'user' ? 'You' : 'Sentinel AI'}
                </span>
                <div style={{
                  background: msg.role === 'user' ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' : 'rgba(255, 255, 255, 0.08)',
                  padding: '12px 16px',
                  borderRadius: msg.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                  fontSize: '14px',
                  lineHeight: '1.6',
                  color: '#fff',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.2)',
                  border: msg.role === 'user' ? 'none' : '1px solid rgba(255, 255, 255, 0.05)'
                }}>
                  {msg.role === 'user' ? (
                    msg.content
                  ) : (
                    <div className="markdown-body chat-markdown" style={{ color: '#fff' }}>
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div style={{ alignSelf: 'flex-start', maxWidth: '85%', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <span style={{ fontSize: '11px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Sentinel AI</span>
                <div style={{ padding: '12px 16px', background: 'rgba(255,255,255,0.08)', borderRadius: '16px 16px 16px 4px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <form onSubmit={handleSend} style={{
            padding: '16px 24px',
            borderTop: '1px solid rgba(255,255,255,0.08)',
            display: 'flex',
            gap: '12px',
            background: 'rgba(0,0,0,0.3)',
            alignItems: 'center'
          }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask for mitigation advice..."
              style={{
                flex: 1,
                background: 'rgba(255,255,255,0.06)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '24px',
                padding: '12px 20px',
                color: '#fff',
                outline: 'none',
                fontSize: '14px',
                transition: 'all 0.3s ease'
              }}
              onFocus={(e) => {
                e.target.style.background = 'rgba(255,255,255,0.1)';
                e.target.style.borderColor = 'rgba(59, 130, 246, 0.5)';
                e.target.style.boxShadow = '0 0 0 2px rgba(59, 130, 246, 0.2)';
              }}
              onBlur={(e) => {
                e.target.style.background = 'rgba(255,255,255,0.06)';
                e.target.style.borderColor = 'rgba(255,255,255,0.1)';
                e.target.style.boxShadow = 'none';
              }}
            />
            <button type="submit" disabled={isLoading || !input.trim()} style={{
              background: (isLoading || !input.trim()) ? 'rgba(255,255,255,0.05)' : 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
              border: 'none',
              color: (isLoading || !input.trim()) ? 'var(--text-secondary)' : '#fff',
              cursor: (isLoading || !input.trim()) ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '10px',
              borderRadius: '50%',
              width: '42px',
              height: '42px',
              transition: 'all 0.3s',
              boxShadow: (isLoading || !input.trim()) ? 'none' : '0 4px 12px rgba(59, 130, 246, 0.4)'
            }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
