function displayPoints() {
    fetch('http://127.0.0.1:5000/uploaded', {
        method: 'POST',
        body: JSON.stringify({
            url: "https://i.imgur.com/hVXJKTW.png"
        }),
        headers: {
            'Content-Type': "application/json",
            'Accept': 'application/json'
        }
    })
        .then(function (response) {
            return response.json();
        }).then(
            function (text) {
                var full_text = text["Full-text"];
                var edited_text = full_text.replace("\n", "");
                var list_of_letters = edited_text.replace(/ /g, '');
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


                document.querySelector("body").innerHTML += "<br>Neatness: " + JSON.stringify(deviationAvPercentage) + "% <br>" + "Handwriting: " + JSON.stringify(overallConf) + "% <br>" + "Overall Score: " + JSON.stringify(overallScore) + "% <br>" + "points scored: " + points;


            });
}