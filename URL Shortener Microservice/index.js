require('dotenv').config();
const express = require('express');
const cors = require('cors');
const app = express();
const mongoose = require('mongoose');
const dns = require('dns');
const validUrl = require('valid-url');

// Basic Configuration
const port = process.env.PORT || 3000;

// Connect to MongoDB
mongoose.connect(
  process.env.MONGO_URI, 
  { useNewUrlParser: true, useUnifiedTopology: true },
  () => {
    console.log('MongoDB database has been connected');
  }
);

// Webserver
app.use(cors());
app.use('/public', express.static(`${process.cwd()}/public`));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Serve the index.html file
app.get('/', (req, res) => {
  res.sendFile(process.cwd() + '/views/index.html');
});

// URL Schema
const urlSchema = new mongoose.Schema({
  original_url: { type: String, required: true, unique: true },
  short_url: { type: Number, required: true, unique: true },
});

// URL Model
const Url = mongoose.model('Url', urlSchema);

// POST /api/shorturl
app.post('/api/shorturl', async (req, res) => {
  const { url } = req.body;   // format: { url: 'https://www.freecodecamp.org/' }
  // Validate URL
  if (!validUrl.isUri(url)) {
    return res.json({ error: 'invalid url' });
  }
  // Check DNS
  const { hostname } = new URL(url);
  dns.lookup(hostname, async (err) => {
    if (err) {
      return res.json({ error: 'invalid url' });
    }
    try {
      // Check if URL is already in the database
      let data = await Url.findOne({ original_url: url });
      if (data) {
        return res.json({ original_url: data.original_url, short_url: data.short_url });
      }
      // If not found, create a new entry
      const count = await Url.countDocuments();
      const shortUrl = count + 1;
      const newUrl = new Url({ original_url: url, short_url: shortUrl });
      data = await newUrl.save();
      res.json({ original_url: data.original_url, short_url: data.short_url });
    } catch (error) {
      res.status(500).send(error);
    }
  });
});

// GET /api/shorturl/:short_url
app.get('/api/shorturl/:short_url', (req, res) => {
  const { short_url } = req.params;
  Url.findOne({ short_url: parseInt(short_url, 10) }, (err, data) => {
    if (err) return res.status(500).send(err);
    if (data) {
      res.redirect(data.original_url);
    } else {
      res.json({ error: 'No short URL found for the given input' });
    }
  });
});

// listen for requests
app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
