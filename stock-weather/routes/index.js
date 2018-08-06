var express = require('express');
var stock_weather = require('../controllers/stock_weather');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.redirect('./health_check');
});

router.get('/health_check', function(req, res, next) {
  res.send({status: 200, message: "I'm alive!"});
});

router.post('/', stock_weather.stock_weather);

module.exports = router;
