import { useState } from 'react'
import { Send } from 'lucide-react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function ChatInterface({ documentText }) {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [error, setError] = useState(null)

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage = inputValue.trim()
    setInputValue('')
    setError(null)

    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])

    // Show typing indicator
    setIsTyping(true)

    try {
      // Build history array from messages
      const history = messages.map(msg => [
        msg.role === 'user' ? msg.content : '',
        msg.role === 'assistant' ? msg.content : ''
      ]).filter(([q, a]) => q && a)

      const response = await axios.post(`${API_URL}/chat`, {
        text: documentText,
        question: userMessage,
        history: history
      })

      const result = response.data

      if (!result.success) {
        throw new Error(result.error || 'Failed to get response')
      }

      // Add AI response to chat
      setMessages(prev => [...prev, { role: 'assistant', content: result.answer }])
      setIsTyping(false)

    } catch (err) {
      setIsTyping(false)
      
      if (err.response) {
        setError(err.response.data.detail || 'Server error occurred')
      } else if (err.request) {
        setError('Could not connect to server')
      } else {
        setError(err.message)
      }
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="chat-section">
      <h3 className="section-title">Ask About This Document</h3>
      
      <div className="chat-container">
        {/* Messages */}
        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-empty">
              <p>Ask anything about this document in English or Nepali</p>
              <div className="chat-suggestions">
                <button 
                  className="suggestion-btn"
                  onClick={() => setInputValue("What is the document date?")}
                >
                  What is the document date?
                </button>
                <button 
                  className="suggestion-btn"
                  onClick={() => setInputValue("यो कागजात कहिलेको हो?")}
                >
                  यो कागजात कहिलेको हो?
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div 
              key={index} 
              className={`message ${message.role}`}
            >
              <div className="message-content">
                {message.content}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="message assistant">
              <div className="message-content typing">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="chat-error">
            {error}
          </div>
        )}

        {/* Input */}
        <div className="chat-input-container">
          <input
            type="text"
            className="chat-input"
            placeholder="What does this document say about...?"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isTyping}
          />
          <button 
            className="btn-send"
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isTyping}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
