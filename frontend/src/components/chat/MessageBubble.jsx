import ReactMarkdown from "react-markdown";

function MessageBubble({ role, text, sources = [] }) {
  const isUser = role === "user";

  return (
    <div className={`message ${isUser ? "user" : "assistant"}`}>

      <div className="message-avatar">
        {isUser ? "YOU" : "AI"}
      </div>

      <div className="message-content">

        {isUser ? (
          <p>{text}</p>
        ) : (
          <div className="markdown-content">
            <ReactMarkdown
              components={{
                h1: ({ children }) => <h1>{children}</h1>,
                h2: ({ children }) => <h2>{children}</h2>,
                h3: ({ children }) => <h3>{children}</h3>,

                p: ({ children }) => <p>{children}</p>,

                strong: ({ children }) => (
                  <strong>{children}</strong>
                ),

                ul: ({ children }) => <ul>{children}</ul>,
                ol: ({ children }) => <ol>{children}</ol>,

                li: ({ children }) => <li>{children}</li>,

                blockquote: ({ children }) => (
                  <blockquote>{children}</blockquote>
                ),

                a: ({ href, children }) => (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {children}
                  </a>
                ),
              }}
            >
              {text}
            </ReactMarkdown>

            {sources.length > 0 && (
              <div className="source-grid">
                {sources.map((source, index) => (
                  <a
                    key={index}
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <span>
                      {source.source || "SOURCE"}
                    </span>

                    <strong>
                      {source.title || "Read article"}
                    </strong>

                    <small>
                      {source.published || ""}
                    </small>
                  </a>
                ))}
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}

export default MessageBubble;