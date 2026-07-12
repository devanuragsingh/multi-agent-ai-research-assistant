import { useState } from "react";

function ChatInput({ onSend, disabled, compact = false }) {
  const [query, setQuery] = useState("");
  const submit = () => { if (query.trim() && !disabled) { onSend(query); setQuery(""); } };
  return <div className={`chat-input-container ${compact ? "compact" : ""}`}>
    <span className="search-icon">⌕</span>
    <textarea value={query} rows="1" disabled={disabled} placeholder="Ask about today’s news..." onChange={(event) => setQuery(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); submit(); } }} />
    <button className="send-btn" onClick={submit} disabled={disabled} aria-label="Send question">↑</button>
  </div>;
}
export default ChatInput;
