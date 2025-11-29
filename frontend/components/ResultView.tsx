import React from 'react';
import { OutfitResult } from '../types';

interface ResultViewProps {
  outfit: OutfitResult;
  onReset: () => void;
}

const ResultView: React.FC<ResultViewProps> = ({ outfit, onReset }) => {
  return (
    <div className="w-full max-w-6xl mx-auto animate-slide-up">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        
        {/* Visual Column */}
        <div className="order-2 lg:order-1 space-y-6">
          <div className="bg-white p-2 rounded-2xl shadow-lg border border-gray-100 sticky top-24">
            {outfit.visualImageBase64 ? (
              <img 
                src={`data:image/jpeg;base64,${outfit.visualImageBase64}`} 
                alt="Generated Outfit" 
                className="w-full h-auto rounded-xl object-cover aspect-[3/4]"
              />
            ) : (
              <div className="w-full aspect-[3/4] bg-gray-50 rounded-xl flex flex-col items-center justify-center text-gray-400 gap-4 animate-pulse">
                <div className="w-16 h-16 border-4 border-gray-200 border-t-primary rounded-full animate-spin"></div>
                <p className="text-lg">Generating Visualization...</p>
              </div>
            )}
            <div className="mt-3 px-2 pb-2">
              <p className="text-sm text-center text-gray-400 uppercase tracking-widest font-semibold">AI Generated Visualization</p>
            </div>
          </div>
        </div>

        {/* Info Column */}
        <div className="order-1 lg:order-2 space-y-10">
          <div>
            <div className="flex items-center gap-3 mb-3">
               <span className="bg-primary/10 text-primary text-sm font-bold px-4 py-1.5 rounded-full uppercase tracking-wider">Final Recommendation</span>
            </div>
            <h2 className="text-5xl font-serif text-gray-900 mb-8 leading-tight">Your Curated Look</h2>
            <div className="prose prose-xl text-gray-600 leading-relaxed whitespace-pre-line">
              {outfit.recommendationText}
            </div>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
            <h3 className="font-serif text-2xl mb-6 flex items-center gap-3 text-gray-900">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
              </svg>
              Complete Your Look
            </h3>
            
            {outfit.groundingChunks && outfit.groundingChunks.length > 0 ? (
              <ul className="space-y-4">
                {outfit.groundingChunks.slice(0, 4).map((chunk, idx) => (
                  chunk.web?.uri && (
                    <li key={idx} className="group">
                      <a 
                        href={chunk.web.uri} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="flex items-center justify-between p-4 rounded-xl bg-gray-50 hover:bg-white hover:shadow-md hover:shadow-gray-100 hover:ring-1 hover:ring-primary/20 transition-all"
                      >
                        <div className="flex flex-col">
                           <span className="text-gray-900 font-semibold text-lg group-hover:text-primary transition-colors line-clamp-1">
                             {chunk.web.title || "View on House of Fraser"}
                           </span>
                           <span className="text-sm text-gray-400 mt-1 truncate max-w-xs">{chunk.web.uri}</span>
                        </div>
                        <div className="bg-gray-100 p-2 rounded-full group-hover:bg-primary/10 transition-colors">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5 text-gray-400 group-hover:text-primary">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                          </svg>
                        </div>
                      </a>
                    </li>
                  )
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic p-6 bg-gray-50 rounded-xl text-lg">No direct links found, but searching for items with similar descriptions on House of Fraser should yield results.</p>
            )}
            <div className="mt-6 pt-4 border-t border-gray-100 flex items-center justify-center gap-2">
               <span className="text-sm text-gray-400">Links provided by</span>
               <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png" alt="Google" className="h-5 opacity-50" />
            </div>
          </div>

          <button 
            onClick={onReset}
            className="w-full py-5 px-6 bg-gray-900 hover:bg-gray-800 text-white rounded-xl font-medium text-lg transition-all shadow-lg shadow-gray-200"
          >
            Start A New Session
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultView;