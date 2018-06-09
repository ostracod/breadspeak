
var fs = require("fs");
var escapeHtml = require("escape-html");

var destinationPath = "./documentation.html";

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
        paragraphLineList.push(escapeHtml(tempLine));
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

var tempHead = "<head>\n<meta charset=\"UTF-8\">\n</head>";
var tempBody = "<body>\n" + paragraphList.join("\n") + "\n</body>";
var content = "<html>\n" + tempHead + "\n" + tempBody + "\n</html>";

console.log(destinationPath);
fs.writeFileSync(destinationPath, content);


