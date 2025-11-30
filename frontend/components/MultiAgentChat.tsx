import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: string;
  sender: string;
  content: string;
  timestamp: string | Date;
  imageBase64?: string;
  products?: Product[];
}

interface Product {
  name: string;
  price: string;
  brand: string;
  url?: string;
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
      content: 'Welcome to your Style Odyssey! 🧭 Tell me about your journey today - where are you going? Our AI agents will collaborate to guide your fashion choices through every destination.',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [showBrands, setShowBrands] = useState(false);
  const [wishlist, setWishlist] = useState<Product[]>([]);
  const [showWishlist, setShowWishlist] = useState(false);
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
      
      const agentMessages: Message[] = data.responses.map((r: any) => {
        const msg: Message = {
          id: `${Date.now()}-${r.agent}`,
          sender: r.agent,
          content: r.message,
          timestamp: r.timestamp,
          imageBase64: r.image_base64
        };
        
        // Extract products from RecommendationAgent
        if (r.agent === 'RecommendationAgent') {
          msg.products = extractProducts(r.message);
        }
        
        return msg;
      });

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

  const extractProducts = (text: string): Product[] => {
    const products: Product[] = [];
    // Extract products with prices (e.g., "Nike Air Max (£89.99)")
    const pricePattern = /([A-Za-z\s&]+)\s*\(([£€$]\d+(?:\.\d{2})?)\)/g;
    let match;
    while ((match = pricePattern.exec(text)) !== null) {
      products.push({
        name: match[1].trim(),
        price: match[2],
        brand: 'Sports Direct' // Default, could be smarter
      });
    }
    return products;
  };

  const addToWishlist = (product: Product) => {
    if (!wishlist.find(p => p.name === product.name)) {
      setWishlist([...wishlist, product]);
    }
  };

  const getTotalPrice = () => {
    return wishlist.reduce((sum, p) => {
      const price = parseFloat(p.price.replace(/[£€$]/g, ''));
      return sum + (isNaN(price) ? 0 : price);
    }, 0).toFixed(2);
  };

  const getAgentColor = (sender: string) => {
    if (sender === 'You') return 'bg-blue-500 text-white';
    if (sender === 'System') return 'bg-gray-200 text-gray-700';
    if (sender === 'IntentAgent') return 'bg-indigo-100 text-indigo-900';
    if (sender === 'VisionAgent') return 'bg-purple-100 text-purple-900';
    if (sender === 'RecommendationAgent') return 'bg-green-100 text-green-900';
    if (sender === 'ConversationAgent') return 'bg-yellow-100 text-yellow-900';
    if (sender === 'ImageGenAgent') return 'bg-pink-100 text-pink-900';
    return 'bg-gray-100 text-gray-900';
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)]">
      <div className="bg-white border-b shadow-sm p-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Retail Odyssey</h1>
            <p className="text-sm text-gray-600">Your AI-Powered Style Journey - 5 Agents Collaborating</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={async () => {
                try {
                  await fetch(`${API_URL}/api/clear`, { method: 'POST' });
                } catch (e) {}
                setMessages([{
                  id: '0',
                  sender: 'System',
                  content: 'Your journey begins anew! 🧭 Where will your style odyssey take you today?',
                  timestamp: new Date()
                }]);
                setUploadedImage(null);
              }}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition text-sm"
            >
              🔄 New Chat
            </button>
            <button
              onClick={() => setShowWishlist(!showWishlist)}
              className="px-4 py-2 bg-green-50 hover:bg-green-100 text-green-600 rounded-lg transition text-sm relative"
            >
              🛒 Cart {wishlist.length > 0 && `(${wishlist.length})`}
            </button>
            <button
              onClick={() => setShowBrands(!showBrands)}
              className="px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-lg transition text-sm"
            >
              🛍️ Shop Frasers
            </button>
          </div>
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

      {showWishlist && (
        <div className="bg-white border-b shadow-sm p-4">
          <div className="max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-3">
              <h3 className="font-semibold text-gray-700">🛒 Your Shopping Cart</h3>
              {wishlist.length > 0 && (
                <button
                  onClick={() => setWishlist([])}
                  className="text-xs text-red-600 hover:text-red-800"
                >
                  Clear All
                </button>
              )}
            </div>
            {wishlist.length === 0 ? (
              <p className="text-sm text-gray-500">Your cart is empty. Add items from recommendations!</p>
            ) : (
              <>
                <div className="space-y-2 mb-4">
                  {wishlist.map((product, idx) => (
                    <div key={idx} className="flex justify-between items-center bg-gray-50 p-3 rounded-lg">
                      <div>
                        <p className="font-medium text-sm">{product.name}</p>
                        <p className="text-xs text-gray-600">{product.brand}</p>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-semibold text-green-600">{product.price}</span>
                        <button
                          onClick={() => setWishlist(wishlist.filter((_, i) => i !== idx))}
                          className="text-red-500 hover:text-red-700 text-sm"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="border-t pt-3 flex justify-between items-center">
                  <span className="font-bold text-lg">Total: £{getTotalPrice()}</span>
                  <a
                    href="https://www.sportsdirect.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition font-medium"
                  >
                    Shop Complete Look →
                  </a>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      <div className="flex-1 bg-gray-50 overflow-y-auto p-6 space-y-4 max-w-6xl mx-auto w-full">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'You' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-2xl ${msg.sender === 'You' ? 'order-2' : 'order-1'}`}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold text-gray-700">{msg.sender}</span>
                <span className="text-xs text-gray-400">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <div className={`rounded-2xl px-4 py-3 shadow-sm ${getAgentColor(msg.sender)}`}>
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown
                    components={{
                      a: ({node, ...props}) => (
                        <a {...props} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 underline" />
                      )
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                </div>
                {msg.imageBase64 && (
                  <img 
                    src={`data:image/png;base64,${msg.imageBase64}`} 
                    alt="Generated outfit" 
                    className="mt-3 rounded-lg max-w-md w-full"
                  />
                )}
                {msg.products && msg.products.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-600 mb-2">💰 Recommended Products:</p>
                    <div className="space-y-2">
                      {msg.products.map((product, idx) => (
                        <div key={idx} className="flex justify-between items-center bg-white bg-opacity-50 p-2 rounded">
                          <div>
                            <p className="text-xs font-medium">{product.name}</p>
                            <p className="text-xs text-gray-600">{product.price}</p>
                          </div>
                          <button
                            onClick={() => addToWishlist(product)}
                            className="text-xs px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded transition"
                          >
                            + Cart
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {msg.sender === 'RecommendationAgent' && !msg.content.includes('🔗 Product Links') && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-600 mb-2">🛍️ Shop at Frasers Group:</p>
                    <div className="flex flex-wrap gap-2">
                      {FRASERS_BRANDS.map(brand => (
                        <a
                          key={brand.name}
                          href={brand.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs px-3 py-1 bg-blue-50 text-blue-700 rounded-full hover:bg-blue-100 transition-colors"
                        >
                          {brand.name} →
                        </a>
                      ))}
                    </div>
                  </div>
                )}
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
        <div className="max-w-6xl mx-auto">
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
          Powered by Google Gemini 3 Pro • Multi-Agent Collaboration • Frasers Group
        </p>
        </div>
      </div>
    </div>
  );
};

export default MultiAgentChat;
