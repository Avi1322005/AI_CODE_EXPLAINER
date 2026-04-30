const express = require('express');
const router = express.Router();
const analyzeController = require('../controllers/analyzeController');
const auth = require('../middleware/authMiddleware');

// Public route for analysis
router.post('/', analyzeController.analyzeAdvanced);

// Protected route for logged-in users to save analysis
router.post('/auth', auth, analyzeController.analyzeAdvanced);

// Protected route to get history
router.get('/history', auth, analyzeController.getHistory);

module.exports = router;
