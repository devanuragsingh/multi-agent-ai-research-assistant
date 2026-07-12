import ChatInput from "../chat/ChatInput";
import FeatureChips from "./FeatureChips";

function WelcomeScreen({ onSend }) {

  return (
    <div className="welcome">

      <h1>
        Where should we start?
      </h1>

      <ChatInput
        onSend={onSend}
      />

      <FeatureChips />

    </div>
  );
}

export default WelcomeScreen;