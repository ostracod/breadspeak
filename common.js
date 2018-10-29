
var fs = require("fs");

var cssPath = "./documentation.css";


function CommonUtils() {

}

var commonUtils = new CommonUtils();

CommonUtils.prototype.capitalize = function(text) {
    return text.charAt(0).toUpperCase() + text.substring(1, text.length).toLowerCase();
}

CommonUtils.prototype.abbreviatePartOfSpeech = function(partOfSpeech) {
    if (partOfSpeech == "Enclosing Particle") {
        return "EP";
    }
    if (partOfSpeech == "Singleton Particle") {
        return "SP";
    }
    if (partOfSpeech == "Delimiting Particle") {
        return "DP";
    }
    if (partOfSpeech == "Narrow Conjunction") {
        return "NC";
    }
    if (partOfSpeech == "Wide Conjunction") {
        return "WC";
    }
    if (partOfSpeech == "Numeric") {
        return "Num";
    }
    return partOfSpeech;
}

CommonUtils.prototype.createHtmlPage = function(bodyContent) {
    var cssContent = fs.readFileSync(cssPath, "utf8");
    var tempHead = "<head>\n<meta charset=\"UTF-8\">\n<style>\n" + cssContent + "\n</style>\n</head>";
    var tempBody = "<body>\n" + bodyContent + "\n</body>";
    return "<html>\n" + tempHead + "\n" + tempBody + "\n</html>";
}

CommonUtils.prototype.getDictionaryData = function() {
    return JSON.parse(fs.readFileSync("./dictionary.json"));
}

module.exports = {
    commonUtils: commonUtils,
    CommonUtils: CommonUtils
};


