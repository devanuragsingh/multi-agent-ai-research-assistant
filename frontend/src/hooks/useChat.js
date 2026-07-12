import { useState } from "react";

export default function useChat() {

  const [messages, setMessages] = useState([]);

  const addMessage = (message) => {

    setMessages((prev) => [

      ...prev,

      message,

    ]);

  };

  return {

    messages,

    addMessage,

  };

}