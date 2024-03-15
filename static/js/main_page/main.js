window.addEventListener("load", function () {
    var specificDiv = document.getElementById("bgcolor");
    var imagePaths = [
        "static/images/dashboard/progress-card-bg.jpg",
        "static/images/dashboard/weather-card.jpg",
        "static/images/dashboard/img_1.jpg"
        // Add more image 
    ];

    // Function of background image and match color
    function setBackgroundImageAndMatchColor(imagePath) {
        specificDiv.style.backgroundImage = "url(" + imagePath + ")";
        var colorThief = new ColorThief();
        var img = new Image();
        img.src = imagePath;

        img.onload = function () {
            var dominantColor = colorThief.getColor(img);
            // Convert RGB color to CSS format 
            var backgroundColor = `rgb(${dominantColor[0]}, ${dominantColor[1]}, ${dominantColor[2]})`;
            var buttons = document.querySelectorAll('#portal-button'); //  buttons selected by their ID
            buttons.forEach(function (button) {
                button.style.backgroundColor = backgroundColor;
                button.style.color = "#FFFFFF"; 
            });
        };
    }

    // setup with a random background image
    var randomIndex = Math.floor(Math.random() * imagePaths.length);
    setBackgroundImageAndMatchColor(imagePaths[randomIndex]);
});
