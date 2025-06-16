import { useState } from 'react'
import axios from 'axios'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const { data } = await axios.post('http://127.0.0.1:8000/chat', {
        message: input
      })
  
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-4 h-screen flex flex-col">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div key={index} className={`p-3 rounded-lg max-w-[70%] break-words ${ message.role === 'user' ? 'bg-blue-200 text-gray-800 ml-auto' : 'bg-gray-100 text-gray-800' }`}>
            {message.content}
          </div>
        ))}
        {isLoading && (
        //   <div className="p-3 rounded-lg max-w-[70%] bg-gray-100 text-gray-800">
        //   <div className="flex space-x-2 items-center">
        //     <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
        //     <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
        //     <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
        //   </div>
        // </div>
          <div className="p-3 rounded-lg max-w-[70%] bg-gray-100 text-gray-800">
            Thinking...
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2 p-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Send
        </button>
      </form>
    </div>
  )
}

export default App
