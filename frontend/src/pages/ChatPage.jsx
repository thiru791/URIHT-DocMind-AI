import { useState, useRef, useEffect } from "react";
import Logo from "../components/Logo";
import api from "../services/api";

function ChatPage() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "👋 Hello! Your document is ready. Ask me anything about it."
    }
  ]);

  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const sendMessage = async () => {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userQuestion
      }
    ]);

    setQuestion("");

    setLoading(true);

    try {
      const response = await api.post("/chat", {
        question: userQuestion
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: response.data.answer
        }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text:
            "❌ Sorry, I couldn't process your request. Please try again."
        }
      ]);
    }

    setLoading(false);
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages, loading]);

  return (
    <div className="upload-page">

      <div className="upload-card">

        <Logo />

        <div className="chat-toolbar">

          <button
            className="new-chat-btn"
            onClick={() =>
              setMessages([
                {
                  sender: "ai",
                  text:
                    "👋 Hello! Your document is ready. Ask me anything about it."
                }
              ])
            }
          >
            🆕 New Chat
          </button>

        </div>

        <div className="document-info">

          <div className="doc-badge">
            📄 PDF Loaded
          </div>

          <div className="doc-name">
            Ready for AI Analysis
          </div>

        </div>

        <div className="chat-box">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={
                msg.sender === "user"
                  ? "user-message"
                  : "ai-message"
              }
            >
              {msg.text}
            </div>

          ))}

          {loading && (

            <div className="ai-message">

              <div className="typing">

                <span></span>
                <span></span>
                <span></span>

              </div>

            </div>

          )}

          <div ref={chatEndRef}></div>

        </div>

        <div className="chat-input">

          <input
            type="text"
            placeholder="Ask anything about your PDF..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (
                e.key === "Enter" &&
                question.trim() &&
                !loading
              ) {
                sendMessage();
              }
            }}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
          >
            {loading ? "Thinking..." : "Send"}
          </button>

        </div>

      </div>

    </div>
  );
}

export default ChatPage;