import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Message, ChatResponse, TypingAnimationProps } from '../types';
import './Chatbot.css';

// Typing animation component
const TypingAnimation: React.FC<TypingAnimationProps> = ({ 
  speed = 500, 
  dotCount = 3 
}) => {
  const [dots, setDots] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => prev.length >= dotCount ? '' : prev + '.');
    }, speed / dotCount);

    return () => clearInterval(interval);
  }, [speed, dotCount]);

  return <span className="typing-dots">{dots}</span>;
};

// Chatbot component
const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm your SQL Assistant. Ask me questions about students in natural language.",
      sender: 'bot',
      timestamp: new Date(),
      type: 'text'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle sending message
  const handleSend = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      // Simulate typing delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await axios.post<ChatResponse>(
        'http://localhost:8000/query/',
        { question: inputText }
      );

      // Add SQL message
      const sqlMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Here's the SQL query for your question:",
        sender: 'bot',
        timestamp: new Date(),
        type: 'sql',
        data: {
          sql: response.data.sql_query
        }
      };

      // Add explanation message
      const explanationMessage: Message = {
        id: (Date.now() + 2).toString(),
        text: "Explanation:",
        sender: 'bot',
        timestamp: new Date(),
        type: 'explanation',
        data: {
          explanation: response.data.explanation
        }
      };

      // Add table data if exists
      const tableMessage: Message = {
        id: (Date.now() + 3).toString(),
        text: response.data.result.length > 0 
          ? "Query Results:" 
          : "No data returned from query.",
        sender: 'bot',
        timestamp: new Date(),
        type: 'table',
        data: {
          tableData: response.data.result
        }
      };

      setMessages(prev => [...prev, sqlMessage, explanationMessage, tableMessage]);
      
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `Error: ${axios.isAxiosError(error) ? error.response?.data?.message || error.message : 'Failed to process request'}`,
        sender: 'bot',
        timestamp: new Date(),
        type: 'text'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-resize textarea
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  // Format timestamp
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Render message content based on type
  const renderMessageContent = (message: Message) => {
    switch (message.type) {
      case 'sql':
        return (
          <div className="message-content">
            <p>{message.text}</p>
            <pre className="sql-code">
              {message.data?.sql}
            </pre>
          </div>
        );
      
      case 'explanation':
        return (
          <div className="message-content">
            <p><strong>{message.text}</strong></p>
            <div className="explanation">
              {message.data?.explanation}
            </div>
          </div>
        );
      
      case 'table':
        return (
          <div className="message-content">
            <p>{message.text}</p>
            {message.data?.tableData && message.data.tableData.length > 0 && (
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      {message.data.tableData[0].map((_, index) => (
                        <th key={index}>Column {index + 1}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {message.data.tableData.map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                          <td key={cellIndex}>{cell}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        );
      
      default:
        return <div className="message-text">{message.text}</div>;
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h1>🤖 SQL Assistant</h1>
        <p>Ask questions about students in natural language</p>
      </div>

      <div className="chatbot-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender}`}
          >
            <div className="message-bubble">
              <div className="message-header">
                <span className="message-sender">
                  {message.sender === 'user' ? 'You' : 'SQL Assistant'}
                </span>
                <span className="message-time">
                  {formatTime(message.timestamp)}
                </span>
              </div>
              {renderMessageContent(message)}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="message bot">
            <div className="message-bubble typing-indicator">
              <TypingAnimation />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chatbot-input-area">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            value={inputText}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="Type your question here... (e.g., How many students are in Data Science class?)"
            disabled={isLoading}
            rows={1}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !inputText.trim()}
            className="send-button"
          >
            {isLoading ? (
              <div className="spinner"></div>
            ) : (
              'Send'
            )}
          </button>
        </div>
        <div className="input-hint">
          Press <kbd>Enter</kbd> to send • <kbd>Shift + Enter</kbd> for new line
        </div>
      </div>
    </div>
  );
};

export default Chatbot;