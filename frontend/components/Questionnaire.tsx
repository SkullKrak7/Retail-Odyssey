import React, { useState } from 'react';
import { UserPreferences } from '../types';

interface QuestionnaireProps {
  onSubmit: (prefs: UserPreferences) => void;
  isProcessing?: boolean;
  hasSubmitted?: boolean;
}

const Questionnaire: React.FC<QuestionnaireProps> = ({ onSubmit, isProcessing, hasSubmitted }) => {
  const [formData, setFormData] = useState<UserPreferences>({
    event: '',
    budget: '',
    mood: '',
    presentation: '',
    weather: '',
    colorPreference: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-4xl bg-white p-10 rounded-3xl shadow-sm border border-gray-100 transition-all">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Event */}
        <div className="space-y-3">
          <label className="text-base font-semibold text-gray-700">What is the event?</label>
          <input
            type="text"
            name="event"
            required
            disabled={isProcessing}
            placeholder="e.g. Wedding, Job Interview, Date Night"
            className="w-full p-4 text-base border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition disabled:bg-gray-50 disabled:text-gray-500"
            value={formData.event}
            onChange={handleChange}
          />
        </div>

        {/* Presentation */}
        <div className="space-y-3">
          <label className="text-base font-semibold text-gray-700">How do you want to be perceived?</label>
          <select
            name="presentation"
            required
            disabled={isProcessing}
            className="w-full p-4 text-base border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition bg-white disabled:bg-gray-50 disabled:text-gray-500"
            value={formData.presentation}
            onChange={handleChange}
          >
            <option value="">Select a vibe</option>
            <option value="Confident & Professional">Confident & Professional</option>
            <option value="Friendly & Approachable">Friendly & Approachable</option>
            <option value="Elegant & Sophisticated">Elegant & Sophisticated</option>
            <option value="Creative & Bold">Creative & Bold</option>
            <option value="Relaxed & Effortless">Relaxed & Effortless</option>
          </select>
        </div>

        {/* Mood */}
        <div className="space-y-3">
          <label className="text-base font-semibold text-gray-700">Current Mood</label>
          <input
            type="text"
            name="mood"
            disabled={isProcessing}
            placeholder="e.g. Excited, Nervous, Chill"
            className="w-full p-4 text-base border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition disabled:bg-gray-50 disabled:text-gray-500"
            value={formData.mood}
            onChange={handleChange}
          />
        </div>

        {/* Weather */}
        <div className="space-y-3">
          <label className="text-base font-semibold text-gray-700">Weather Forecast</label>
          <input
            type="text"
            name="weather"
            disabled={isProcessing}
            placeholder="e.g. Sunny and 25°C"
            className="w-full p-4 text-base border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition disabled:bg-gray-50 disabled:text-gray-500"
            value={formData.weather}
            onChange={handleChange}
          />
        </div>

        {/* Budget */}
        <div className="space-y-3">
          <label className="text-base font-semibold text-gray-700">Budget for new items</label>
          <select
            name="budget"
            disabled={isProcessing}
            className="w-full p-4 text-base border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition bg-white disabled:bg-gray-50 disabled:text-gray-500"
            value={formData.budget}
            onChange={handleChange}
          >
            <option value="Low">Low (£0 - £50)</option>
            <option value="Medium">Medium (£50 - £150)</option>
            <option value="High">High (£150+)</option>
            <option value="None">None (Use what I have)</option>
          </select>
        </div>

        {/* Colors */}
        <div className="space-y-3">
          <label className="text-base font-semibold text-gray-700">Color Preferences</label>
          <input
            type="text"
            name="colorPreference"
            disabled={isProcessing}
            placeholder="e.g. Earth tones, No black"
            className="w-full p-4 text-base border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition disabled:bg-gray-50 disabled:text-gray-500"
            value={formData.colorPreference}
            onChange={handleChange}
          />
        </div>
      </div>

      <div className="mt-10 flex justify-end">
        <button
          type="submit"
          disabled={isProcessing}
          className={`
            bg-secondary text-white font-medium py-4 px-10 rounded-xl hover:bg-gray-800 transition-all shadow-lg shadow-gray-200 flex items-center justify-center gap-2 text-lg
            ${isProcessing ? 'opacity-70 cursor-wait' : ''}
          `}
        >
          {isProcessing ? (
            <span>Processing...</span>
          ) : hasSubmitted ? (
             <>
               <span>Update & Regenerate</span>
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                 <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
               </svg>
             </>
          ) : (
             <>
               <span>Generate My Look</span>
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                 <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
               </svg>
             </>
          )}
        </button>
      </div>
    </form>
  );
};

export default Questionnaire;