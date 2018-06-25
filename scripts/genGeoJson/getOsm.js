// source: https://docs.google.com/spreadsheets/d/1iW_ICmF8DslGSA4o0--KRcxYnDEN5HuJwq0aey-7H2Q
const Papa = require('papaparse');
const osmtogeojson = require('osmtogeojson');
const fs = require('fs');
const https = require('https');
const DOMParser = require('xmldom').DOMParser;

const base_url = 'https://api.openstreetmap.org/api/0.6/way/';
const csvFile = fs.readFileSync('zones-osm-ids.csv', 'utf8');

let data;

Papa.parse(csvFile, {
  delimiter: ',',
  header: true,
  complete: (res) => {
    data = res.data;
  }
});

[data[1]].forEach((zone) => {
  const osmUrl = `${base_url}${zone['OSM ID']}/full`;
  https.get(osmUrl, (res) => {
    let body = '';
    res.on('data', function(chunk) {
      body += chunk;
    });
    res.on('end', function() {
      const doc = new DOMParser().parseFromString(body, 'text/xml');
      console.log(JSON.stringify(osmtogeojson(doc), null, 2));
    });
  });
})
  
