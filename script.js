const firebaseConfig = {
    apiKey: "AIzaSyCB9yEwIJszbDZuIEOMJOHf2CPSVQnBzrc",
    authDomain: "uploaded-images-34308.firebaseapp.com",
    projectId: "uploaded-images-34308",
    storageBucket: "uploaded-images-34308.appspot.com",
    messagingSenderId: "255164297862",
    appId: "1:255164297862:web:dfc02f9ed728e53ca41707",
    measurementId: "G-DHLLLVW8NZ"
};
firebase.initializeApp(firebaseConfig);

function displayPoints() {
    document.querySelector("#send").disabled = true;
    const ref = firebase.storage().ref();
    const file = $('#files').get(0).files[0];
    const name = (+new Date()) + '-' + file.name;
    const metadata = { contentType: file.type };
    const task = ref.child(name).put(file, metadata);
    var imageURL = "";
    task
        .then(snapshot => snapshot.ref.getDownloadURL())
        .then((url) => {
            imageURL = url;
            fetch('http://127.0.0.1:5000/uploaded', {
                method: 'POST',
                body: JSON.stringify({
                    url: imageURL
                }),
                headers: {
                    'Content-Type': "application/json",
                    'Accept': 'application/json'
                }
            })
                .then(function (response) {
                    return response.json();
                })
                .then(
                    function (text) {
                        var full_text = text["Full-text"];
                        var edited_text = full_text.replace("\n", "");
                        var list_of_letters = edited_text.replace(/\s/g,'');
                        console.log(list_of_letters);
                        var heightList = [];
                        var widthList = [];
                        var overallConf = Number(((text["Paragraph-Confidence"] + text["Block-Confidence"]) / 2).toFixed(2));
                        for (var x = 0; x < text["Letter-Sizes"].length; x++) {
                            heightList.push(text["Letter-Sizes"][x][list_of_letters[x]]["height"]);
                            widthList.push(text["Letter-Sizes"][x][list_of_letters[x]]["width"]);

                            var heightMean = math.mean(heightList);
                            var widthMean = math.mean(widthList);
                            var heightStd = math.std(heightList);
                            var widthStd = math.std(widthList);
                            var heightPercentage = Number((heightStd / heightMean * 100).toFixed(2));
                            var widthPercentage = Number((widthStd / widthMean * 100).toFixed(2));
                            var deviationAvPercentage = Number((100 - ((heightPercentage + widthPercentage) / 2)).toFixed(2));
                            var overallScore = Number(((overallConf + deviationAvPercentage) / 2).toFixed(2));
                        }

                        var points = math.ceil(math.floor(overallConf) / 5);

                        document.querySelector("#result").innerHTML += "<br>Neatness: " + JSON.stringify(deviationAvPercentage) + "% <br>" + "Handwriting: " + JSON.stringify(overallConf) + "% <br>" + "Overall Score: " + JSON.stringify(overallScore) + "% <br>" + "points scored: " + points;

                        plotGraph(text);

                    });

        }).catch(console.error);
}

function plotGraph(data) {
    heightsData = [];
    deviationData = [];
    labels = [];
    data["Letter-Sizes"].forEach(function (letter) {
        var char = Object.keys(letter)[0];
        var H = letter[char].height;
        heightsData.push(H);
        labels.push(char);
    });
    var averageHeight = 0;
    heightsData.forEach(function(h){averageHeight += h;});
    averageHeight /= heightsData.length;
    deviationData = heightsData.map(function(h){
        return h - averageHeight;
    })
    new Chart("myChart", {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: deviationData
          }]
        },
        options: {
          legend: {display: false}
        }
    });
}