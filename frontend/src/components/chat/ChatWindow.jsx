import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

function ChatWindow({ messages, isLoading }) {
  return (
    <div className="chat-window">

      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          role={message.role}
          text={message.text}
          sources={message.sources || []}
        />
      ))}

      {isLoading && (
        <div className="message assistant">
          <div className="message-avatar">AI</div>

          <div className="message-content">
            <TypingIndicator />
          </div>
        </div>
      )}

    </div>
  );
}

export default ChatWindow;