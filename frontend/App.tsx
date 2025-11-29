import React, { useState, useRef } from 'react';
import FileUpload from './components/FileUpload';
import Questionnaire from './components/Questionnaire';
import AgentChat from './components/AgentChat';
import ResultView from './components/ResultView';
import { UserPreferences, AgentMessage, OutfitResult } from './types';
import { 
  fileToGenerativePart, 
  analyzeClothingImage, 
  analyzeUserIntent, 
  generateRecommendations, 
  generateOutfitVisual 
} from './services/geminiService';

const App: React.FC = () => {
  // State for each stage of the data flow
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [agentMessages, setAgentMessages] = useState<AgentMessage[]>([]);
  const [outfitResult, setOutfitResult] = useState<OutfitResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Refs for auto-scrolling
  const questionsRef = useRef<HTMLDivElement>(null);
  const chatRef = useRef<HTMLDivElement>(null);
  const resultsRef = useRef<HTMLDivElement>(null);
  const topRef = useRef<HTMLDivElement>(null);

  // Helper to add messages to chat
  const addAgentMessage = (role: AgentMessage['role'], content: string, status: 'thinking' | 'done' = 'done') => {
    const newMessage: AgentMessage = {
      id: Math.random().toString(36).substr(2, 9),
      agentName: role,
      role,
      content,
      timestamp: Date.now(),
      status
    };

    setAgentMessages(prev => {
      if (status === 'done') {
        const filtered = prev.filter(m => !(m.role === role && m.status === 'thinking'));
        return [...filtered, newMessage];
      }
      return [...prev, newMessage];
    });
  };

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
    // Reset downstream if re-uploading
    setPreferences(null);
    setAgentMessages([]);
    setOutfitResult(null);
    setIsProcessing(false);
    
    // Scroll to questions after a brief delay for render
    setTimeout(() => {
      questionsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 300);
  };

  const startProcessing = async (prefs: UserPreferences) => {
    if (!uploadedFile) return;
    
    setPreferences(prefs);
    setIsProcessing(true);
    setAgentMessages([]);
    setOutfitResult(null);

    // Scroll to chat
    setTimeout(() => {
      chatRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    try {
      // 1. Convert Image
      const base64Image = await fileToGenerativePart(uploadedFile);

      // 2. Vision Agent
      addAgentMessage('Vision Agent', 'Analyzing garment details...', 'thinking');
      const visionAnalysis = await analyzeClothingImage(base64Image);
      addAgentMessage('Vision Agent', visionAnalysis, 'done');

      // 3. Intent Agent
      addAgentMessage('Intent Agent', 'Synthesizing style strategy...', 'thinking');
      await new Promise(r => setTimeout(r, 800)); 
      const intentAnalysis = await analyzeUserIntent(prefs);
      addAgentMessage('Intent Agent', intentAnalysis, 'done');

      // 4. Recommendation Agent
      addAgentMessage('Recommendation Agent', 'Curating looks and searching House of Fraser...', 'thinking');
      await new Promise(r => setTimeout(r, 1000));
      const { text: recText, chunks: recChunks } = await generateRecommendations(visionAnalysis, intentAnalysis);
      addAgentMessage('Recommendation Agent', recText, 'done');

      // 5. Prepare Results
      setOutfitResult({
        recommendationText: recText,
        groundingChunks: recChunks,
        visualImageBase64: undefined 
      });

      setIsProcessing(false);

      // Scroll to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);

      // 6. Generate Visual (Background)
      const visualBase64 = await generateOutfitVisual(`${visionAnalysis} styled for ${intentAnalysis}`);
      
      if (visualBase64) {
        setOutfitResult(prev => prev ? { ...prev, visualImageBase64: visualBase64 } : null);
      }

    } catch (error) {
      console.error("Workflow failed", error);
      alert("Something went wrong with the AI stylists. Please try again.");
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setUploadedFile(null);
    setPreferences(null);
    setAgentMessages([]);
    setOutfitResult(null);
    setIsProcessing(false);
    topRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Component for section headers with connecting lines
  const StepHeader = ({ number, title, isActive, isCompleted }: { number: number, title: string, isActive: boolean, isCompleted: boolean }) => (
    <div className="flex items-center gap-4 mb-6">
      <div className={`
        w-12 h-12 rounded-full flex items-center justify-center font-serif font-bold text-xl z-10 transition-colors duration-500 flex-shrink-0
        ${isActive || isCompleted ? 'bg-primary text-white shadow-lg' : 'bg-gray-200 text-gray-400'}
      `}>
        {isCompleted ? (
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
          </svg>
        ) : number}
      </div>
      <h2 className={`text-3xl font-serif transition-colors duration-500 ${isActive || isCompleted ? 'text-gray-900' : 'text-gray-300'}`}>
        {title}
      </h2>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <div ref={topRef} />
      
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary text-white rounded-lg flex items-center justify-center font-serif font-bold text-2xl">S</div>
            <h1 className="text-3xl font-serif font-bold text-gray-900 tracking-tight">StyleSense AI</h1>
          </div>
          <button onClick={handleReset} className="text-base font-medium text-gray-500 hover:text-primary transition-colors">
            Reset
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow p-4 md:p-8 max-w-6xl mx-auto w-full">
        
        {/* Intro Section */}
        <div className="max-w-4xl mx-auto text-center mb-20 pt-10 animate-fade-in">
          <h2 className="text-5xl md:text-7xl font-serif text-gray-900 mb-8 leading-tight">
            StyleSense AI
          </h2>
          <p className="text-2xl text-gray-600 mb-12 leading-relaxed font-light">
            Your personal stylist team to find your perfect look for any event.
          </p>
          
          <div className="bg-white/50 backdrop-blur-sm p-8 md:p-10 rounded-3xl shadow-sm border border-gray-100 text-left mx-auto max-w-3xl">
             <h3 className="text-base font-bold text-gray-400 uppercase tracking-wider mb-6">How it works</h3>
             <ul className="space-y-5">
               {[
                 "Upload a picture of clothes you are thinking of wearing to the event",
                 "Share details about the event and the look you are going for",
                 "Let your agentic stylist give a visual preview of the ideal outfit",
                 "Get shopping links to missing clothing for the outfit",
                 "If the look isn’t you, simply restart a new look"
               ].map((step, i) => (
                 <li key={i} className="flex gap-4 text-gray-700 text-lg">
                    <span className="flex-shrink-0 w-7 h-7 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold mt-0.5">{i+1}</span>
                    <span className="leading-relaxed">{step}</span>
                 </li>
               ))}
             </ul>
          </div>
        </div>

        {/* Timeline Container */}
        <div className="relative">
          {/* Continuous vertical line */}
          <div className="absolute left-6 top-6 bottom-0 w-0.5 bg-gray-200 -z-10" />

          {/* Step 1: Upload */}
          <section className="mb-20 animate-fade-in relative">
            <StepHeader 
              number={1} 
              title="Your Wardrobe Item" 
              isActive={true} 
              isCompleted={!!uploadedFile} 
            />
            <div className="ml-16 md:ml-24">
              <FileUpload onFileSelect={handleFileUpload} />
            </div>
          </section>

          {/* Step 2: Questionnaire */}
          <div ref={questionsRef}>
            {uploadedFile && (
              <section className="mb-20 animate-slide-up relative">
                <StepHeader 
                  number={2} 
                  title="Event & Context" 
                  isActive={true} 
                  isCompleted={!!preferences && isProcessing} 
                />
                <div className="ml-16 md:ml-24">
                  <Questionnaire 
                    onSubmit={startProcessing} 
                    isProcessing={isProcessing}
                    hasSubmitted={!!preferences}
                  />
                </div>
              </section>
            )}
          </div>

          {/* Step 3: Agents */}
          <div ref={chatRef}>
            {(isProcessing || agentMessages.length > 0) && (
              <section className="mb-20 animate-slide-up relative">
                <StepHeader 
                  number={3} 
                  title="AI Consultation" 
                  isActive={true} 
                  isCompleted={!!outfitResult} 
                />
                <div className="ml-16 md:ml-24 bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
                  <AgentChat messages={agentMessages} />
                </div>
              </section>
            )}
          </div>

          {/* Step 4: Results */}
          <div ref={resultsRef}>
            {outfitResult && (
              <section className="mb-24 animate-slide-up relative">
                <StepHeader 
                  number={4} 
                  title="Your Curated Look" 
                  isActive={true} 
                  isCompleted={true} 
                />
                <div className="ml-16 md:ml-24">
                  <ResultView outfit={outfitResult} onReset={handleReset} />
                </div>
              </section>
            )}
          </div>
        </div>

      </main>
      
      <footer className="py-8 text-center text-gray-400 text-base bg-white border-t border-gray-100 mt-auto">
        Powered by Google Gemini 2.5 • House of Fraser
      </footer>
    </div>
  );
};

export default App;