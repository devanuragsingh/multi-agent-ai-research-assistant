import { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import ChatInput from "../components/chat/ChatInput";
import ChatWindow from "../components/chat/ChatWindow";
import { askNews } from "../services/api";

const starters = [
  "What's happening in the world today?",
  "Latest technology news",
  "Global business headlines",
  "Sports news today",
];

function Home() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (query) => {
    const text = query?.trim();

    if (!text || isLoading) return;

    // Create the user message first
    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      text: text,
    };

    // Immediately show user's message
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      console.log("Sending news query:", text);

      const data = await askNews(text);

      console.log("News API response:", data);

      const assistantMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        text:
          data?.answer ||
          "I received the news response, but there was no answer.",
        sources: data?.articles || [],
      };

      // Add assistant response without removing previous messages
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("NEWS API ERROR:", error);

      const errorMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        text:
          "I couldn't reach the news service. Please make sure the backend API is running and try again.",
        sources: [],
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setIsLoading(false);
  };

  return (
    <div className="app-layout">

      {/* SIDEBAR */}
      <Sidebar onNewChat={handleNewChat} />

      {/* MAIN CONTENT */}
      <main className="main-content">
        <section
          className={
            messages.length > 0
              ? "news-chat active-chat"
              : "news-chat"
          }
        >

          {/* =========================
              WELCOME SCREEN
          ========================== */}
          {messages.length === 0 ? (
            <div className="welcome">

              <div className="eyebrow">
                <span />
                LIVE GLOBAL NEWS
              </div>

              <h1>
                Ask what’s happening <em>anywhere.</em>
              </h1>

              <p className="welcome-copy">
                Your daily briefing on the stories shaping the world —
                from trusted news sources, in one clear conversation.
              </p>

              <ChatInput
                onSend={handleSend}
                disabled={isLoading}
              />

              <div className="starter-list">
                {starters.map((starter) => (
                  <button
                    key={starter}
                    onClick={() => handleSend(starter)}
                    disabled={isLoading}
                  >
                    {starter}
                    <span>↗</span>
                  </button>
                ))}
              </div>

            </div>
          ) : (

            /* =========================
               CHAT SCREEN
            ========================== */
            <>
              <header className="chat-header">
                <div>
                  <span className="live-dot" />
                  Live news desk
                </div>

                <p>
                  Updated from current reporting
                </p>
              </header>

              <ChatWindow
                messages={messages}
                isLoading={isLoading}
              />

              <ChatInput
                onSend={handleSend}
                disabled={isLoading}
                compact
              />
            </>
          )}

        </section>
      </main>
    </div>
  );
}

export default Home;