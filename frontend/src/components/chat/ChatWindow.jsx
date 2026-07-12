function ChatWindow({ messages }) {

  if (!messages.length) return null;

  return (
    <div className="chat-window">

      {messages.map((message) => (
        <div key={message.id}>
          {message.component}
        </div>
      ))}

    </div>
  );

}

export default ChatWindow;