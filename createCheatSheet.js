
var fs = require("fs");
var escapeHtml = require("escape-html");

var commonUtils = require("./common.js").commonUtils;

var destinationPath = "./cheatSheet.html";
var maximumColumnSize = 105;

var dictionaryData = commonUtils.getDictionaryData();
var tempCategoryList = dictionaryData.categories;
var tempEntryList = [];
var index = 0;
while (index < tempCategoryList.length) {
    var tempCategory = tempCategoryList[index];
    var tempIndex = 0;
    while (tempIndex < tempCategory.entries.length) {
        var tempEntry = tempCategory.entries[tempIndex];
        tempEntryList.push(tempEntry);
        tempIndex += 1;
    }
    index += 1;
}
tempEntryList.sort(function(entry1, entry2) {
    if (entry1.word > entry2.word) {
        return 1;
    }
    if (entry1.word < entry2.word) {
        return -1;
    }
    return 0;
});
var tempLineList = [];
var index = 0;
while (index < tempEntryList.length) {
    var tempEntry = tempEntryList[index];
    var tempWord = commonUtils.capitalize(tempEntry.word);
    var tempLine = "<div><span class=\"bs\">" + tempWord + "</span> (" + commonUtils.abbreviatePartOfSpeech(tempEntry.partOfSpeech) + ") " + escapeHtml(tempEntry.shortDefinition) + "</div>";
    tempLineList.push(tempLine);
    index += 1;
}
var tempColumnList = [["<div><strong>BreadSpeak Cheat Sheet</strong></div>", "<div>&nbsp;</div>"]];
var index = 0;
while (index < tempLineList.length) {
    var tempLine = tempLineList[index];
    var tempColumn = tempColumnList[tempColumnList.length - 1];
    if (tempColumn.length >= maximumColumnSize) {
        tempColumn = [];
        tempColumnList.push(tempColumn);
    }
    tempColumn.push(tempLine);
    index += 1;
}
var tempColumnHtmlList = [];
var index = 0;
while (index < tempColumnList.length) {
    var tempColumn = tempColumnList[index];
    var tempColumnHtml = "<div style=\"float: left; margin-right: 10px;\">\n" + tempColumn.join("\n") + "\n</div>";
    tempColumnHtmlList.push(tempColumnHtml);
    index += 1;
}

var content = commonUtils.createHtmlPage(tempColumnHtmlList.join("\n") + "<br style=\"clear: both;\">");

console.log(destinationPath);
fs.writeFileSync(destinationPath, content);


