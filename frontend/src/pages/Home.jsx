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
    const text = query.trim();
    if (!text || isLoading) return;

    setMessages((items) => [...items, { id: crypto.randomUUID(), role: "user", text }]);
    setIsLoading(true);
    try {
      const data = await askNews(text);
      setMessages((items) => [
        ...items,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: data.answer,
          sources: data.articles || [],
        },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((items) => [
        ...items,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: "I couldn't reach the news service. Please make sure the API is running, then try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <Sidebar onNewChat={() => setMessages([])} />
      <main className="main-content">
        <section className={messages.length ? "news-chat active-chat" : "news-chat"}>
          {!messages.length ? (
            <div className="welcome">
              <div className="eyebrow"><span /> LIVE GLOBAL NEWS</div>
              <h1>Ask what’s happening <em>anywhere.</em></h1>
              <p className="welcome-copy">Your daily briefing on the stories shaping the world — from trusted news sources, in one clear conversation.</p>
              <ChatInput onSend={handleSend} disabled={isLoading} />
              <div className="starter-list">
                {starters.map((starter) => <button key={starter} onClick={() => handleSend(starter)}>{starter}<span>↗</span></button>)}
              </div>
            </div>
          ) : (
            <>
              <header className="chat-header"><div><span className="live-dot" />Live news desk</div><p>Updated from current reporting</p></header>
              <ChatWindow messages={messages} isLoading={isLoading} />
              <ChatInput onSend={handleSend} disabled={isLoading} compact />
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default Home;
