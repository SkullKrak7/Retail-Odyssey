import { GoogleGenAI, Type } from "@google/genai";
import { UserPreferences, GroundingChunk } from '../types';

// Initialize Gemini Client
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

/**
 * Convert a File object to a Base64 string
 */
export const fileToGenerativePart = async (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64String = reader.result as string;
      // Remove data url prefix (e.g. "data:image/jpeg;base64,")
      const base64Data = base64String.split(',')[1];
      resolve(base64Data);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

/**
 * Agent 1: Vision Agent
 * Analyzes the uploaded clothing image.
 */
export const analyzeClothingImage = async (base64Image: string): Promise<string> => {
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: {
        parts: [
          {
            inlineData: {
              mimeType: 'image/jpeg',
              data: base64Image,
            },
          },
          {
            text: "You are the Vision Agent. Analyze this image of clothing. Describe the items in detail, including color, fabric texture, style (formal/casual), and condition. Be concise but descriptive.",
          },
        ],
      },
    });
    return response.text || "I couldn't analyze the image clearly.";
  } catch (error) {
    console.error("Vision Agent Error:", error);
    return "Error analyzing the clothing image.";
  }
};

/**
 * Agent 2: Intent Agent
 * Synthesizes user preferences into a style strategy.
 */
export const analyzeUserIntent = async (prefs: UserPreferences): Promise<string> => {
  try {
    const prompt = `
      You are the Intent Agent.
      User Inputs:
      - Event: ${prefs.event}
      - Budget: ${prefs.budget}
      - Mood: ${prefs.mood}
      - Presentation: ${prefs.presentation}
      - Weather: ${prefs.weather}
      - Color Prefs: ${prefs.colorPreference}

      Task: Synthesize a brief "Style Strategy".
      CRITICAL: Explicitly state the required Formality Level (e.g., Casual, Smart Casual, Cocktail, Formal, Black Tie) based on the Event. For example, Weddings are typically Formal or Cocktail.
      Describe the target look, fabrics, and vibe required to meet this formality.
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
    });
    return response.text || "Could not determine intent.";
  } catch (error) {
    console.error("Intent Agent Error:", error);
    return "Error analyzing user intent.";
  }
};

/**
 * Agent 3: Recommendation Agent
 * Generates advice and finds shopping links using Search Grounding.
 */
export const generateRecommendations = async (
  visionAnalysis: string,
  intentAnalysis: string
): Promise<{ text: string; chunks: GroundingChunk[] }> => {
  try {
    const prompt = `
      You are the Recommendation Agent. 
      
      Context:
      - User's Uploaded Item (Vision Analysis): "${visionAnalysis}"
      - Event & Formality Strategy (Intent Analysis): "${intentAnalysis}"

      Your Goal: Create a cohesive outfit using the User's Item as the core piece.

      Rules:
      1. **MANDATORY INCLUSION**: You MUST use the User's Uploaded Item in the final outfit. Do NOT replace it. Your job is to make it work for the event by adding the right jacket, shoes, or accessories.
      2. **Styling Strategy**: If the User's Item is too casual for the event, tell them exactly how to "dress it up" (e.g., adding a blazer, formal shoes). If it's too formal, tell them how to "dress it down".
      3. SEARCH: Use the tool to find 3-4 specific COMPLEMENTARY items on "House of Fraser" (e.g., "formal blazer", "chinos", "heels") that complete the look. Do NOT search for the item the user already owns.
      4. **Output Text Rules**: 
         - Write a VERY SHORT summary explaining the look.
         - **CRITICAL**: Do NOT mention specific brand names.
         - **CRITICAL**: Do NOT list the items in the text.
         - Focus on the "Why": "This creates a balanced silhouette..."
      5. Conciseness: STRICT LIMIT: Maximum 30-40 words. 2 sentences maximum. Direct and punchy.
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        tools: [{ googleSearch: {} }],
      },
    });

    const text = response.text || "No recommendations generated.";
    const chunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];

    return { text, chunks: chunks as GroundingChunk[] };
  } catch (error) {
    console.error("Recommendation Agent Error:", error);
    return { text: "Error fetching recommendations.", chunks: [] };
  }
};

/**
 * Visual Generation
 * Creates an image of the outfit on a mannequin.
 */
export const generateOutfitVisual = async (description: string): Promise<string | null> => {
  try {
    const prompt = `
      A realistic fashion photography shot of a mannequin wearing the following outfit: ${description}. 
      Neutral studio background, professional lighting. High resolution, detailed fabrics.
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash-image', // Using standard image gen as per guidelines for general tasks
      contents: {
        parts: [{ text: prompt }],
      },
    });

    // Extract image
    for (const part of response.candidates?.[0]?.content?.parts || []) {
      if (part.inlineData) {
        return part.inlineData.data;
      }
    }
    return null;
  } catch (error) {
    console.error("Image Generation Error:", error);
    return null;
  }
};