const axios = require('axios');

const data = {
    "cart_id": 80846755,
    "override_conflict": true,
    "source": "web-app",
    "vehicle": 9572570,
    "oa_tag": "2360b00d8c6a476e850525bf076ad275",
    "honkGUID": "yjze4ofcuodwzxbo57ecjm",
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
      return True
    } catch (error) {
      console.error(error.response.data.errors);
      return False
    }
  }


const delay = ms => new Promise(res => setTimeout(res, ms));
let isPurchased = False
while (!isPurchased)
    isPurchased = postRequest()
    await delay(5000)

