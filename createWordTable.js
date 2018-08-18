
var fs = require("fs");
var escapeHtml = require("escape-html");

var consonantSet = ["B", "D", "F", "G", "K", "P", "S", "T", "V", "Z"];
var vowelSet = ["A", "E", "I", "O", "U"];

var cssPath = "./documentation.css";
var destinationPath = "./wordTable.html";

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.substring(1, text.length).toLowerCase();
}

function abbreviatePartOfSpeech(partOfSpeech) {
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

function getEntryInCategoryByWord(category, word) {
    var index = 0;
    while (index < category.entries.length) {
        var tempEntry = category.entries[index];
        var tempWord = tempEntry.word;
        if (tempWord == word) {
            return tempEntry;
        }
        index += 1;
    }
    return null;
}

var dictionaryData = JSON.parse(fs.readFileSync("./dictionary.json"));
dictionaryData.categories.sort(function(category1, category2) {
    if (category1.syllable === null) {
        if (category2.syllable === null) {
            return 0;
        } else {
            return -1;
        }
    } else if (category2.syllable === null) {
        return 1;
    }
    var tempIndex1 = consonantSet.indexOf(category1.syllable.charAt(0));
    var tempIndex2 = consonantSet.indexOf(category2.syllable.charAt(0));
    if (tempIndex1 > tempIndex2) {
        return 1;
    }
    if (tempIndex1 < tempIndex2) {
        return -1;
    }
    var tempIndex1 = consonantSet.indexOf(category1.syllable.charAt(1));
    var tempIndex2 = consonantSet.indexOf(category2.syllable.charAt(1));
    if (tempIndex1 > tempIndex2) {
        return 1;
    }
    if (tempIndex1 < tempIndex2) {
        return -1;
    }
    return 0;
});
var tempRowList = [];
var tempConsonantIndex = 0;
while (tempConsonantIndex < consonantSet.length) {
    var tempConsonant = consonantSet[tempConsonantIndex];
    var tempVowelIndex = 0;
    while (tempVowelIndex < vowelSet.length) {
        var tempVowel = vowelSet[tempVowelIndex];
        var tempSyllable = tempConsonant + tempVowel;
        var tempCellList = [];
        var tempCategoryIndex = 0;
        while (tempCategoryIndex < dictionaryData.categories.length) {
            var tempCategory = dictionaryData.categories[tempCategoryIndex];
            var tempWord;
            if (tempCategory.syllable === null) {
                tempWord = tempSyllable;
            } else {
                tempWord = tempCategory.syllable + tempSyllable;
            }
            var tempEntry = getEntryInCategoryByWord(tempCategory, tempWord);
            tempWord = capitalize(tempWord);
            var tempCellContent;
            if (tempEntry === null) {
                tempCellContent = "&ndash;";
            } else {
                tempCellContent = "<span class=\"bs\">" + tempWord + "</span> (" + abbreviatePartOfSpeech(tempEntry.partOfSpeech) + ")<br />" + escapeHtml(tempEntry.shortDefinition);
            }
            tempCell = "<td><div class=\"wordTableCell\">" + tempCellContent + "</div></td>";
            tempCellList.push(tempCell);
            tempCategoryIndex += 1;
        }
        tempRowList.push("<tr>" + tempCellList.join("\n") + "</tr>");
        tempVowelIndex += 1;
    }
    tempConsonantIndex += 1;
}
var tempTable = "<table class=\"wordTable\">" + tempRowList.join("\n") + "</table>";

var cssContent = fs.readFileSync(cssPath, "utf8");

var tempHead = "<head>\n<meta charset=\"UTF-8\">\n<style>\n" + cssContent + "\n</style>\n</head>";
var tempBody = "<body><p class=\"title1\">BREADSPEAK WORD TABLE</p>\n" + tempTable + "\n</body>";
var content = "<html>\n" + tempHead + "\n" + tempBody + "\n</html>";

console.log(destinationPath);
fs.writeFileSync(destinationPath, content);


