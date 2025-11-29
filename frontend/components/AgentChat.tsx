import React, { useEffect, useRef } from 'react';
import { AgentMessage } from '../types';

interface AgentChatProps {
  messages: AgentMessage[];
}

const AgentChat: React.FC<AgentChatProps> = ({ messages }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getAgentColor = (role: AgentMessage['role']) => {
    switch (role) {
      case 'Vision Agent': return 'bg-blue-50 text-blue-900 border-blue-100';
      case 'Intent Agent': return 'bg-purple-50 text-purple-900 border-purple-100';
      case 'Recommendation Agent': return 'bg-emerald-50 text-emerald-900 border-emerald-100';
      default: return 'bg-gray-50 text-gray-900';
    }
  };

  const getAgentIcon = (role: AgentMessage['role']) => {
    switch (role) {
      case 'Vision Agent':
        return (
          <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-6 h-6">
              <path d="M10 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
              <path fillRule="evenodd" d="M.664 10.59a1.651 1.651 0 0 1 0-1.186A10.004 10.004 0 0 1 10 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0 1 10 17c-4.257 0-7.893-2.66-9.336-6.41ZM14 10a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z" clipRule="evenodd" />
            </svg>
          </div>
        );
      case 'Intent Agent':
        return (
          <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-600">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-6 h-6">
              <path d="M10 2a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0v-1.5A.75.75 0 0 1 10 2ZM10 15a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0v-1.5A.75.75 0 0 1 10 15ZM10 7a3 3 0 1 0 0 6 3 3 0 0 0 0-6ZM15.657 5.404a.75.75 0 1 0-1.06-1.06l-1.061 1.06a.75.75 0 0 0 1.06 1.06l1.06-1.06ZM6.464 14.596a.75.75 0 1 0-1.06-1.06l-1.06 1.06a.75.75 0 0 0 1.06 1.06l1.06-1.06ZM18 10a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5A.75.75 0 0 1 18 10ZM5 10a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5A.75.75 0 0 1 5 10ZM14.596 15.657a.75.75 0 0 0 1.06-1.06l-1.06-1.061a.75.75 0 1 0-1.06 1.06l1.06 1.06ZM5.404 6.464a.75.75 0 0 0 1.06-1.06l-1.06-1.06a.75.75 0 1 0-1.061 1.06l1.06 1.06Z" />
            </svg>
          </div>
        );
      case 'Recommendation Agent':
        return (
          <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-6 h-6">
              <path fillRule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z" clipRule="evenodd" />
            </svg>
          </div>
        );
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 pb-4">
      <div className="text-center mb-8">
        <h3 className="text-xl font-serif text-gray-600">AI Stylist Team Collaboration</h3>
      </div>
      
      {messages.map((msg) => (
        <div key={msg.id} className={`flex gap-4 animate-fade-in ${msg.status === 'thinking' ? 'opacity-70' : ''}`}>
          <div className="flex-shrink-0 mt-1">
            {getAgentIcon(msg.role)}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-semibold text-base text-gray-800">{msg.role}</span>
              <span className="text-sm text-gray-400">
                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            <div className={`p-5 rounded-2xl rounded-tl-none border ${getAgentColor(msg.role)} shadow-sm`}>
              {msg.status === 'thinking' ? (
                <div className="flex gap-1 items-center h-6">
                  <div className="w-2.5 h-2.5 bg-current rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2.5 h-2.5 bg-current rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2.5 h-2.5 bg-current rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              ) : (
                 <p className="text-base leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              )}
            </div>
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
};

export default AgentChat;