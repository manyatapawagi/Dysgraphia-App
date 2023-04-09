fetch("http://127.0.0.1:5000/").then(
    function (response) {
        return response.json();
    }
).then(
    function (text) {
        document.querySelector("body").append(JSON.stringify(text["Letter-Sizes"][0]["T"]));
    }
)