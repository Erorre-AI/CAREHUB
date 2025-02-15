import React from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

const SpeechFeatures = () => {
  const { transcript, resetTranscript } = useSpeechRecognition();

  const handleListen = () => {
    SpeechRecognition.startListening();
  };

  const handleStop = () => {
    SpeechRecognition.stopListening();
  };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div>
      <button onClick={handleListen}>Start Listening</button>
      <button onClick={handleStop}>Stop Listening</button>
      <p>{transcript}</p>
    </div>
  );
};

export default SpeechFeatures;