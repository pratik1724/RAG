import React, { useState } from "react";
import axios from "axios";

export default function ChatBox() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [context, setContext] = useState([]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question,
      });

      setAnswer(res.data.answer);
      setContext(res.data.context);
    } catch (err) {
      console.error(err);
      setAnswer("❌ Error connecting to backend.");
    }
  };

  return (
    <div style={{ marginTop: "1rem" }}>
      <textarea
        rows="3"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "100%", padding: "10px" }}
      />
      <br />
      <button onClick={handleAsk} style={{ marginTop: "10px", padding: "8px" }}>
        Ask
      </button>

      {answer && (
        <div style={{ marginTop: "1.5rem" }}>
          <h3>Answer:</h3>
          <p>{answer}</p>
          {context.length > 0 && (
            <>
              <h4>🔎 Context used:</h4>
              <ul>
                {context.map((c, i) => (
                  <li key={i}>{c}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
