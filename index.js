// index.js
// where your node app starts

// init project
var express = require('express');
var app = express();

// enable CORS (https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)
// so that your API is remotely testable by FCC 
var cors = require('cors');
app.use(cors({optionsSuccessStatus: 200}));  // some legacy browsers choke on 204

// http://expressjs.com/en/starter/static-files.html
app.use(express.static('public'));

// http://expressjs.com/en/starter/basic-routing.html
app.get("/", function (req, res) {
  res.sendFile(__dirname + '/views/index.html');
});

// your first API endpoint... 
app.get("/api/hello", function (req, res) {
  res.json({greeting: 'hello API'});
});

app.get('/api/:date?', (req, res) => {
  const dateParam = req.params.date;
  let date;

  // Check if dateParam is empty, so that it defaults to current date
  if (!dateParam) {
    date = new Date();
  } else {
    // Check if dateParam is a number
    // isNaN() returns true if dateParam is not a number
    // !isNaN() returns true if dateParam is a number
    if (!isNaN(dateParam)) {
      date = new Date(parseInt(dateParam));
    // if dateParam is not a number, it is a string  
    } else {
      date = new Date(dateParam);   // dateParam is a string
    }
  }

  // Check for invalid date
  if (date.toString() === 'Invalid Date') {
    return res.json({ error: 'Invalid Date' });
  }
  // Return date in unix and utc format
  res.json({
    unix: date.getTime(),
    utc: date.toUTCString(),
  });
});

// To handle 404 errors or invalid routes
app.use((req, res) => {
  res.status(404).json({ error: 'Invalid Date' });
});

// Listen on port set in environment variable or default to 3000
var listener = app.listen(process.env.PORT || 3000, function () {
  console.log('Your app is listening on port ' + listener.address().port);
});
