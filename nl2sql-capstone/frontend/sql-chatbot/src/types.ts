export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  type: 'text' | 'sql' | 'table' | 'explanation';
  data?: {
    sql?: string;
    explanation?: string;
    tableData?: string[][];
  };
}

export interface ChatResponse {
  sql_query: string;
  explanation: string;
  result: string[][];
}

export interface TypingAnimationProps {
  speed?: number;
  dotCount?: number;
}