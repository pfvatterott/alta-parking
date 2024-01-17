const axios = require('axios');

const data = {
  "cart_id": 80859971,
  "override_conflict": true,
  "source": "web-app",
  "vehicle": 9572570,
  "oa_tag": "2360b00d8c6a476e850525bf076ad275",
  "honkGUID": "op4ivnqlmi8f9tch6nzn2v",
  "app_version": 69000
};

const config = {
  headers: {
    'Content-Type': 'application/json'
  }
};

async function postRequest() {
  try {
    const response = await axios.post('https://platform.honkmobile.com/parking_sessions', data, config);
    console.log(`Status: ${response.status}`);
    console.log(`Body: ${JSON.stringify(response.data)}`);
    exit()
  } catch (error) {
    console.error(`${Date.now()} - ${error.response.data.errors}`);
  }
}

setInterval(function() {
  postRequest()
}, 3000)