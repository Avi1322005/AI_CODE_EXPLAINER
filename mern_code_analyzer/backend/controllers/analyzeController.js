const aiService = require('../services/aiService');
const Analysis = require('../models/Analysis');

exports.analyzeAdvanced = async (req, res) => {
  const { code, language } = req.body;

  if (!code || !language) {
    return res.status(400).json({ error: 'Code and language are required' });
  }

  try {
    const resultJson = await aiService.analyzeCodeAdvanced(code, language);

    // Save to history if logged in
    if (req.user) {
      const newAnalysis = new Analysis({
        user: req.user.id,
        language,
        code,
        result: resultJson
      });
      await newAnalysis.save();
    }

    res.json(resultJson);
  } catch (error) {
    console.error('Error in advanced analysis:', error);
    res.status(500).json({ error: 'Failed to analyze code', details: error.message });
  }
};

exports.getHistory = async (req, res) => {
  try {
    const history = await Analysis.find({ user: req.user.id }).sort({ createdAt: -1 }).limit(20);
    res.json(history);
  } catch (error) {
    console.error('Error fetching history:', error);
    res.status(500).json({ error: 'Failed to fetch history' });
  }
};
