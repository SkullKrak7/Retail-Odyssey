import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: string;
  sender: string;
  content: string;
  timestamp: Date;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const FRASERS_BRANDS = [
  { name: 'House of Fraser', url: 'https://www.houseoffraser.co.uk' },
  { name: 'Sports Direct', url: 'https://www.sportsdirect.com' },
  { name: 'Flannels', url: 'https://www.flannels.com' },
  { name: 'USC', url: 'https://www.usc.co.uk' },
  { name: 'Jack Wills', url: 'https://www.jackwills.com' },
  { name: 'Evans Cycles', url: 'https://www.evanscycles.com' },
  { name: 'Game', url: 'https://www.game.co.uk' }
];

const MultiAgentChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      sender: 'System',
      content: 'Welcome! Ask our AI fashion agents for outfit advice, style tips, or recommendations. You can optionally upload images of your wardrobe.',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [showBrands, setShowBrands] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'You',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          image_url: uploadedImage
        })
      });

      const data = await response.json();
      
      const agentMessages: Message[] = data.responses.map((r: any) => ({
        id: `${Date.now()}-${r.agent}`,
        sender: r.agent,
        content: r.message,
        timestamp: new Date(r.time)
      }));

      setMessages(prev => [...prev, ...agentMessages]);
      setUploadedImage(null);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        sender: 'System',
        content: 'Error connecting to agents. Please try again.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      setUploadedImage(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const getAgentColor = (sender: string) => {
    if (sender === 'You') return 'bg-blue-500 text-white';
    if (sender === 'System') return 'bg-gray-200 text-gray-700';
    if (sender === 'VisionAgent') return 'bg-purple-100 text-purple-900';
    if (sender === 'RecommendationAgent') return 'bg-green-100 text-green-900';
    if (sender === 'ConversationAgent') return 'bg-yellow-100 text-yellow-900';
    if (sender === 'ImageGenAgent') return 'bg-pink-100 text-pink-900';
    return 'bg-gray-100 text-gray-900';
  };

  return (
    <div className="flex flex-col h-screen max-w-6xl mx-auto">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 shadow-lg">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">StyleSense AI</h1>
            <p className="text-blue-100 mt-1">Multi-Agent Fashion Assistant</p>
          </div>
          <button
            onClick={() => setShowBrands(!showBrands)}
            className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition"
          >
            🛍️ Shop Frasers
          </button>
        </div>
      </div>

      {showBrands && (
        <div className="bg-white border-b shadow-sm p-4">
          <h3 className="font-semibold text-gray-700 mb-3">Shop at Frasers Group Brands:</h3>
          <div className="flex flex-wrap gap-2">
            {FRASERS_BRANDS.map(brand => (
              <a
                key={brand.name}
                href={brand.url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition text-sm font-medium"
              >
                {brand.name} →
              </a>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 bg-gray-50 overflow-y-auto p-6 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'You' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-2xl ${msg.sender === 'You' ? 'order-2' : 'order-1'}`}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold text-gray-700">{msg.sender}</span>
                <span className="text-xs text-gray-400">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <div className={`rounded-2xl px-4 py-3 shadow-sm ${getAgentColor(msg.sender)}`}>
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 rounded-2xl px-4 py-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="bg-white border-t shadow-lg p-4">
        {uploadedImage && (
          <div className="mb-3 relative inline-block">
            <img src={uploadedImage} alt="Upload" className="h-20 rounded-lg border-2 border-blue-200" />
            <button
              onClick={() => setUploadedImage(null)}
              className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600"
            >
              ×
            </button>
          </div>
        )}
        <div className="flex gap-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleImageUpload}
            accept="image/*"
            className="hidden"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="px-4 py-3 bg-gray-100 hover:bg-gray-200 rounded-xl transition text-lg"
            title="Upload wardrobe image (optional)"
          >
            📎
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
            placeholder="Ask for outfit advice, style tips, or recommendations..."
            className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 transition"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition font-semibold"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2 text-center">
          Powered by OpenAI GPT-4 • Multi-Agent Collaboration
        </p>
      </div>
    </div>
  );
};

export default MultiAgentChat;
