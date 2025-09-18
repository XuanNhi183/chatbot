import fetch from "node-fetch";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { message } = req.body;
  if (!message) return res.status(400).json({ error: "No message provided" });

  const API_KEY = process.env.OPENROUTER_KEY;  
  const API_URL = "https://openrouter.ai/api/v1/chat/completions";

  const payload = {
    model: "deepseek-chat-v3-0324:free",
    messages: [{ role: "user", content: message }],
    temperature: 0.7,
    max_tokens: 150
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) return res.status(response.status).json({ error: data });

    const reply = data.choices[0].message.content;
    res.status(200).json({ reply });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
