function MessageBubble({ question, answer }) {
  return (
    <div className="chat-area">

      <div className="user-message">
        <strong>You:</strong>
        <p>{question}</p>
      </div>

      <div className="ai-message">
        <strong>Research AI:</strong>
        <p>{answer}</p>
      </div>

    </div>
  );
}

export default MessageBubble;