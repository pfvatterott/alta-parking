const axios = require('axios');

// const data = {
//   "cart_id": 80859971,
//   "override_conflict": true,
//   "source": "web-app",
//   "vehicle": 9572570,
//   "oa_tag": "2360b00d8c6a476e850525bf076ad275",
//   "honkGUID": "op4ivnqlmi8f9tch6nzn2v",
//   "app_version": 69000
// };

// const config = {
//   headers: {
//     'Content-Type': 'application/json'
//   }
// };

// async function postRequest() {
//   try {
//     const response = await axios.post('https://platform.honkmobile.com/parking_sessions', data, config);
//     console.log(`Status: ${response.status}`);
//     console.log(`Body: ${JSON.stringify(response.data)}`);
//     exit()
//   } catch (error) {
//     console.error(`${Date.now()} - ${error.response.data.errors}`);
//   }
// }

// setInterval(function() {
//   postRequest()
// }, 3000)

let data = JSON.stringify({
  "operationName": "AccountPromoCodes",
  "variables": {
    "zoneId": "elP1Tp"
  },
  "query": "fragment CorePromoCodeFields on PromoCode{hashid redeemCode shortDesc totalUses totalUsesCount expiry __typename}query AccountPromoCodes($zoneId: ID){accountPromoCodes(zoneId: $zoneId){...CorePromoCodeFields timezone startDate expiry promoCodesRates{activeSessionLimit activeSessionCount rate{hashid description zone{hashid __typename}__typename}__typename}__typename}}"
});

let config = {
  method: 'post',
  maxBodyLength: Infinity,
  url: 'https://platform.honkmobile.com/graphql?honkGUID=b7h8uio8uue5niap19x14e',
  headers: { 
    'Content-Type': 'application/json', 
    'X-Authentication': 'ae482aeb21854d089ab2e60434a204b6'
  },
  data : data
};

axios.request(config)
.then((response) => {
  console.log(JSON.stringify(response.data));
})
.catch((error) => {
  console.log(error);
});
