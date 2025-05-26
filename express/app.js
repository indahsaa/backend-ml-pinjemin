import express from 'express';
import axios from 'axios';

const app = express();
const PORT = process.env.PORT || 5000;
const FASTAPI_URL = 'http://127.0.0.1:8000'; 

app.use(express.json());

// POST /api/recommend/user
app.post('/api/recommend/user', async (req, res) => {
  try {
    const response = await axios.post(`${FASTAPI_URL}/recommend/user`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: 'Failed to fetch user recommendation' });
  }
});

// POST /api/recommend/item
app.post('/api/recommend/item', async (req, res) => {
  try {
    const response = await axios.post(`${FASTAPI_URL}/recommend/item`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: 'Failed to fetch item recommendation' });
  }
});

// POST /api/recommend/search
app.post('/api/recommend/search', async (req, res) => {
  try {
    const response = await axios.post(`${FASTAPI_URL}/recommend/search`, req.body);
    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: 'Failed to fetch search recommendation' });
  }
});

app.listen(PORT, () => {
  console.log(`Express server running at http://localhost:${PORT}`);
});
