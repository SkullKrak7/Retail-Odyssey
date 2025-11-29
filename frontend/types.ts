export enum AppStep {
  UPLOAD = 'UPLOAD',
  QUESTIONS = 'QUESTIONS',
  PROCESSING = 'PROCESSING',
  RESULTS = 'RESULTS',
}

export interface UserPreferences {
  event: string;
  budget: string;
  mood: string;
  presentation: string;
  weather: string;
  colorPreference: string;
}

export interface AgentMessage {
  id: string;
  agentName: string;
  role: 'Vision Agent' | 'Intent Agent' | 'Recommendation Agent';
  content: string;
  timestamp: number;
  status: 'thinking' | 'done';
}

export interface GroundingChunk {
  web?: {
    uri: string;
    title: string;
  };
}

export interface OutfitResult {
  recommendationText: string;
  groundingChunks: GroundingChunk[];
  visualImageBase64?: string;
}
