require('dotenv').config()
var express = require('express');
var app = express();
var cors = require('cors');
const multer = require('multer');
const path = require('path');

// Web server configuration
app.use(cors());
app.use('/public', express.static(process.cwd() + '/public'));
app.get('/', function (req, res) {
  res.sendFile(process.cwd() + '/views/index.html');
});

// Set up Multer storage
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Define the file upload endpoint
app.post('/api/fileanalyse', upload.single('upfile'), (req, res) => {
  if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
  }
  const { originalname, mimetype, size } = req.file;
  res.json({
      name: originalname,
      type: mimetype,
      size: size
  });
});

const port = process.env.PORT;
app.listen(port, function () {
  console.log('Your app is listening on port ' + port)
});
