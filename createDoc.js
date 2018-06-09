
var fs = require("fs");
var escapeHtml = require("escape-html");

var cssPath = "./documentation.css";
var destinationPath = "./documentation.html";

function generateStyleSpans(text) {
    while (true) {
        var index = text.indexOf("){");
        if (index < 0) {
            break;
        }
        var tempStartIndex = text.lastIndexOf("(", index - 1);
        var tempEndIndex = text.indexOf("}", index + 2);
        var tempClassName = text.substring(tempStartIndex + 1, index);
        var tempContent = text.substring(index + 2, tempEndIndex);
        text = text.substring(0, tempStartIndex) + "<span class=\"" + tempClassName + "\">" + tempContent + "</span>" + text.substring(tempEndIndex + 1, text.length);
    }
    return text;
}

var content = fs.readFileSync("./description.txt", "utf8");
var lineList = content.split("\n");
var paragraphList = [];
var paragraphLineList = [];
var index = 0;
while (true) {
    var tempLine = lineList[index];
    index += 1;
    var tempShouldBreak = (index >= lineList.length);
    tempLine = tempLine.trim();
    var tempShouldAddParagraph = false;
    if (tempLine.length > 0) {
        tempLine = tempLine.replace("--->", "\u2192");
        if (tempLine.charAt(0) == ">") {
            tempLine = "\u2022" + tempLine.substring(1, tempLine.length);
        }
        tempLine = escapeHtml(tempLine);
        tempLine = generateStyleSpans(tempLine);
        paragraphLineList.push(tempLine);
    } else {
        tempShouldAddParagraph = true;
    }
    if (tempShouldBreak) {
        tempShouldAddParagraph = true;
    }
    if (tempShouldAddParagraph) {
        paragraphList.push("<p>" + paragraphLineList.join("<br />\n") + "</p>");
        paragraphLineList = [];
    }
    if (tempShouldBreak) {
        break;
    }
}

var cssContent = fs.readFileSync(cssPath, "utf8");

var tempHead = "<head>\n<meta charset=\"UTF-8\">\n<style>\n" + cssContent + "\n</style>\n</head>";
var tempBody = "<body>\n" + paragraphList.join("\n") + "\n</body>";
var content = "<html>\n" + tempHead + "\n" + tempBody + "\n</html>";

console.log(destinationPath);
fs.writeFileSync(destinationPath, content);


