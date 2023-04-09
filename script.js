fetch("http://127.0.0.1:5000/").then(
    function (response) {
        return response.json();
    }
).then(
    function (text) {
        // 
        var full_text = text["Full-text"]
        var edited_text = full_text.replace("\n", "");
        var list_of_letters = edited_text.replace(/ /g, '');
        var heightList = [];
        var widthList = [];
        for (var x = 0; x < text["Letter-Sizes"].length; x++) {
            heightList.push(text["Letter-Sizes"][x][list_of_letters[x]]["height"]);
            widthList.push(text["Letter-Sizes"][x][list_of_letters[x]]["width"]);

            var heightMean = math.mean(heightList);
            var widthMean = math.mean(widthList);
            var heightStd = math.std(heightList);
            var widthStd = math.std(widthList);
            var heightPercentage = heightStd / heightMean * 100;
            var widthPercentage = widthStd / widthMean * 100;
            var deviationAv = (heightPercentage + widthPercentage) / 2;
        }
        document.querySelector("body").append(JSON.stringify(widthStd));
    }
)