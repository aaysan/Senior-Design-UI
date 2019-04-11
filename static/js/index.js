//var http = require('http');
function checkForNewData() {
    //console.log("data");
    const getData = async () => {
    //console.log("data");
     const data = await fetch(
        "https://webhooks.mongodb-stitch.com/api/client/v2.0/app/our_last_hackson-sfrvf/service/Capture_face/incoming_webhook/fetch_face"
    ).then(response => response.json())
    .then(json => {
        console.log(json);
        if(json !== "FAIL"){
            console.log("finally works")
            location.replace("../Sophia?name="+json["name"]);
        }
        return json; // access json.body here
    })
     // console.log(data);
      // Check if there is a new value
      const result = JSON.stringify(data);
      //console.log(result);
      /*if(data !== "FAIL"){
          console.log("finally works")
          location.replace("{{ url_for('static', filename='../Sophia') }}");
      }*/
      // Handle any new values appropriately
      checkForNewData();
    }
    setTimeout(getData, 5000)
  };

  
  function checkForNewData2() {
    //console.log("data");
    const getData = async () => {
    //console.log("data");
     const data = await fetch(
        "https://webhooks.mongodb-stitch.com/api/client/v2.0/app/our_last_hackson-sfrvf/service/upload_img/incoming_webhook/find_latest"
    ).then(response => response.json())
    .then(json => {
        console.log(json);
        // if(json !== "FAIL"){
        //     console.log("finally works")
        //     location.replace("../Sophia?name="+json["name"]);
        // }
        return json; // access json.body here
    })
     // console.log(data);
      // Check if there is a new value
      const result = JSON.stringify(data);
      //console.log(result);
      /*if(data !== "FAIL"){
          console.log("finally works")
          location.replace("{{ url_for('static', filename='../Sophia') }}");
      }*/
      // Handle any new values appropriately
      checkForNewData2();
    }
    setTimeout(getData, 5000)
  };

  