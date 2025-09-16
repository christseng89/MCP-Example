// install axios first: npm install axios
const axios = require('axios');

async function run() {
  // Replace with your real values
  const webhookUrl = process.env.WEBHOOK_URL || "https://<yourname/>.app.n8n.cloud/webhook/<workid/>";
  const company = process.env.COMPANY || "nvda";
  const query = "What is NVIDIA's business overview according to the latest SEC 10-K filing?";

  const options = {
    method: 'POST',
    url: webhookUrl,
    headers: {
      'Content-Type': 'application/json'
    },
    data: {
      input: query,
      company: company
    },
    timeout: 60000
  };

  try {
    const response = await axios(options);
    console.log("Response:", response.data);
    return response.data;  // in plain node, return just for consistency
  } catch (error) {
    console.error("Error:", error.message);
    return "error";
  }
}

run();
