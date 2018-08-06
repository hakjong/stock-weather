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

    gen_res(res, {
      speech: stock_name + " 날씨 알려줄게요.",
      shouldEndSession: false
    })
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
