const { OpenAI } = require('openai');
require('dotenv').config();

const openai = new OpenAI({
  apiKey: process.env.GROQ_API_KEY || process.env.OPENAI_API_KEY,
  baseURL: "https://api.groq.com/openai/v1"
});

// Helper function to call Groq
const callGroq = async (prompt) => {
  const completion = await openai.chat.completions.create({
    model: 'llama-3.1-8b-instant',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.2,
    response_format: { type: 'json_object' }
  });

  let resultText = completion.choices[0].message.content.trim();
  if (resultText.startsWith('\`\`\`json')) {
    resultText = resultText.replace(/^\`\`\`json/, '').replace(/\`\`\`$/, '');
  }
  return JSON.parse(resultText);
};

exports.analyzeCodeAdvanced = async (code, language) => {
  const prompt = `
Act as an expert Senior Software Engineer and Technical Interviewer. Analyze the following ${language} code.
You MUST return ONLY a valid JSON object matching this exact schema, with no additional text:
{
  "score": {
    "correctness": <number 0-40>,
    "efficiency": <number 0-30>,
    "readability": <number 0-20>,
    "bestPractices": <number 0-10>,
    "total": <number 0-100>
  },
  "bugs": [
    { "line": <string or number>, "issue": "<string>", "fix": "<string>" }
  ],
  "dryRun": "<string explaining step-by-step execution with a sample input>",
  "complexity": {
    "time": "<string e.g. O(N)>",
    "space": "<string e.g. O(1)>",
    "explanation": "<string>"
  },
  "eli5": "<string explaining the code simply to a 5-year-old>",
  "refactoredCode": "<string containing the complete, improved clean code>",
  "interviewQuestions": [
    "<string question 1>",
    "<string question 2>"
  ],
  "testCases": [
    { "input": "<string>", "expected": "<string>", "type": "<string e.g. Edge Case>" }
  ]
}

Code to analyze:
\`\`\`${language}
${code}
\`\`\`
`;
  return await callGroq(prompt);
};
