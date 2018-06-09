
var fs = require("fs");
var escapeHtml = require("escape-html");

var cssPath = "./documentation.css";
var destinationPath = "./documentation.html";

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.substring(1, text.length).toLowerCase();
}

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

function performUnicodeSubstitutions(text) {
    while (true) {
        var tempStartIndex = text.indexOf("#{");
        if (tempStartIndex < 0) {
            break;
        }
        var tempEndIndex = text.indexOf("}", tempStartIndex + 2);
        var tempCode = text.substring(tempStartIndex + 2, tempEndIndex);
        var tempCharacter = String.fromCharCode(parseInt(tempCode, 16));
        text = text.substring(0, tempStartIndex) + tempCharacter + text.substring(tempEndIndex + 1, text.length);
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
        tempLine = performUnicodeSubstitutions(tempLine);
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

var dictionaryData = JSON.parse(fs.readFileSync("./dictionary.json"));
var tempCategoryList = dictionaryData.categories;
var tempLineList = [];
var index = 0;
while (index < tempCategoryList.length) {
    var tempCategory = tempCategoryList[index];
    var tempText = tempCategory.name;
    if (tempCategory.syllable !== null) {
        tempText += " (" + tempCategory.syllable + "&ndash;)";
    }
    tempLineList.push("<p><span class=\"title2\">" + tempText + "</span></p>");
    var tempLineList2 = [];
    var tempIndex = 0;
    while (tempIndex < tempCategory.entries.length) {
        var tempEntry = tempCategory.entries[tempIndex];
        var tempLine = "<span class=\"bs\">" + capitalize(tempEntry.word) + "</span> (" + tempEntry.partOfSpeech + ") " + escapeHtml(tempEntry.definition);
        if (tempEntry.antonym !== null) {
            tempLine += " <span class=\"bs\">" + capitalize(tempEntry.antonym.word) + "</span> (*) " + escapeHtml(tempEntry.antonym.definition);
        }
        tempLineList2.push(tempLine);
        tempIndex += 1;
    }
    tempLineList.push(tempLineList2.join("<br />\n"));
    index += 1;
}
var legendLineList = [];
var index = 0;
while (index < dictionaryData.legend.length) {
    var tempText = dictionaryData.legend[index];
    legendLineList.push(escapeHtml("\u2022 " + tempText));
    index += 1;
}
var legendContent = "<p>Abbreviations:</p>\n" + legendLineList.join("<br /> \n");
var dictionaryContent = "<p><span class=\"title1\">DICTIONARY</span></p>\n" + legendContent + "\n" + tempLineList.join("\n");

var cssContent = fs.readFileSync(cssPath, "utf8");

var tempHead = "<head>\n<meta charset=\"UTF-8\">\n<style>\n" + cssContent + "\n</style>\n</head>";
var tempBody = "<body>\n" + paragraphList.join("\n") + "\n" + dictionaryContent + "\n</body>";
var content = "<html>\n" + tempHead + "\n" + tempBody + "\n</html>";

console.log(destinationPath);
fs.writeFileSync(destinationPath, content);


