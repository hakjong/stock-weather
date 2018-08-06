exports.stock_weather = function(req, res) {

  var intent = req.body.request.intent;

  switch (req.body.request.type) {

    // Requests

    case "LaunchRequest":
      guide();
      break;

    case "IntentRequest":

      console.log(intent.name);

      switch (intent.name) {
        case "StockWeather":
          stock_weather_handler();
          break;

        // Built-in intents

        case "Clova.GuideIntent":
        case "Clova.CancelIntent":
        case "Clova.YesIntent":
        case "Clova.NoIntent":
          guide();
          break;

        // 핸들링 할 수 없는 인텐트

        default:
          guide();
          break;
      }

      break;

    case "SessionEndedRequest":
      // 자원 정리
      break;

    default:
      break;
  }


  function guide() {
    gen_res(res, {
      speech: "어떤 종목이 궁금한가요? 네이버날씨 알려줘. 와 같이 말 해 보세요.",
      shouldEndSession: false
    })
  }


  function stock_weather_handler() {
    var stock_name = intent.slots.stock_item.value;

    var sql = "SELECT news.sentiment as sentiment, count(*) as cnt FROM news JOIN (" +
      "SELECT id FROM news WHERE fk_stock_id IN (" +
      "SELECT id FROM stock WHERE name='" + stock_name + "'" +
      ") ORDER BY pubdate DESC LIMIT 100" +
      ") AS lim ON news.id=lim.id GROUP BY sentiment;";

    db.query(sql, function (err, result) {
      if (err) {
        return;
      }

      var s = {sum: 0};
      for (var i = 0; i < result.length; ++i) {
        s[result[i].sentiment] = result[i].cnt;
        s.sum += result[i].cnt;
      }

      var percentage = parseInt((s.NEG / s.sum) * 100);

      var weather;
      if (percentage < 30)
        weather = '맑아요';
      else if (percentage < 50)
        weather = '흐려요';
      else
        weather = '비가 올 것 같아요';

      gen_res(res, {
        speech: '오늘 ' + stock_name + ' 는 ' + weather + '. 비 올 확률은 ' + percentage + ' 퍼센트 입니다.'
      })
    });
  }
};


function gen_res(res, args) {
  res.send({
    "version": "0.1.0",
    "sessionAttributes": pick (args.sessionAttributes, {}),
    "response": {
      "outputSpeech": {
        "type": "SimpleSpeech",
        "values": {
          "type": "PlainText",
          "lang": "ko",
          "value": pick(args.speech, "")
        }
      },
      "card": {},
      "directives": [],
      "shouldEndSession": pick(args.shouldEndSession, true)
    }
  });

  function pick(arg, default_value) {
    if (arg || arg === false) {
      return arg;
    }
    return default_value;
  }
}
