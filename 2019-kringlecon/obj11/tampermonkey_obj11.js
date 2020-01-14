// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // lock 2 - in the div libra class
    // ------------------------------------------------------------------------------------
    var code = document.querySelector("div.libra > strong").innerText
    document.querySelector("body > div > ul > li:nth-child(5) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(5) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(5) > div > button").click();

    // lock 4 - in the local storag
    // ------------------------------------------------------------------------------------
    code = window.localStorage.getItem('🛢️🛢️🛢️');
    document.querySelector("body > div > ul > li:nth-child(9) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(9) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(9) > div > button").click();

    // lock 5 - in the title
    // ------------------------------------------------------------------------------------
    code = document.title.substr(document.title.length - 8);
    document.querySelector("body > div > ul > li:nth-child(11) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(11) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(11) > div > button").click();

    // lock 6 - class names are hardcoded and order always the same
    // ------------------------------------------------------------------------------------
    code = document.getElementsByClassName("ZADFCDIV")[0].innerText + document.getElementsByClassName("GMSXHBQH")[0].innerText + document.getElementsByClassName("RPSMZXMY")[0].innerText + document.getElementsByClassName("IDOIJIKV")[0].innerText + document.getElementsByClassName("KXTBRPTJ")[0].innerText + document.getElementsByClassName("AJGXPXJV")[0].innerText + document.getElementsByClassName("ZWYRBISO")[0].innerText + document.getElementsByClassName("KPVVBGSG")[0].innerText;
    document.querySelector("body > div > ul > li:nth-child(13) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(13) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(13) > div > button").click();

    // lock 7 - in CSS class 'instructions'
    // ------------------------------------------------------------------------------------
    code = getComputedStyle(document.querySelector('.instructions')).fontFamily.split(',')[0];
    document.querySelector("body > div > ul > li:nth-child(15) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(15) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(15) > div > button").click();

    // lock 8 - hardcoded
    // ------------------------------------------------------------------------------------
    code = "VERONICA";
    document.querySelector("body > div > ul > li:nth-child(17) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(17) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(17) > div > button").click();

    // lock 9 - parse the CSS files
    // ------------------------------------------------------------------------------------
    // get CSS file content
    var file = document.querySelector("head > link:nth-child(2)").href;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", file, false);
    xmlhttp.send();
    var css=xmlhttp.responseText;

    // extract code values and re-assemble
    css.match(/content: '.+'/g);
    code = '';
    for (var c of css.match(/content: '(.+)'/g)){code = code+c.match(/'.+'/)[0]};
    code = code.replace(/'/g, "");
    document.querySelector("body > div > ul > li:nth-child(19) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(19) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(19) > div > button").click();

    // lock 10 - code is hardcoded, just add 3 divs in lock div
    // ------------------------------------------------------------------------------------
    code = "KD29XJ37";
    var node = document.getElementsByClassName("component macaroni")[0];
    document.querySelector("body > div > ul > li:nth-child(21) > div").appendChild(node);
    node = document.getElementsByClassName("component swab")[0];
    document.querySelector("body > div > ul > li:nth-child(21) > div").appendChild(node);
    node = document.getElementsByClassName("component gnome")[0];
    document.querySelector("body > div > ul > li:nth-child(21) > div").appendChild(node);
    document.querySelector("body > div > ul > li:nth-child(21) > div > input").value = code;
    document.querySelector("body > div > ul > li:nth-child(21) > div > button").disabled=0;
    document.querySelector("body > div > ul > li:nth-child(21) > div > button").click();

    // lock 3 - uses Tesseract
    // import tesseract
    // ------------------------------------------------------------------------------------
    var tes = document.createElement('script');
    tes.src = "https://cdn.rawgit.com/naptha/tesseract.js/1.0.10/dist/tesseract.js";
    document.getElementsByTagName('head')[0].appendChild(tes);

    // get image dynamic filename
    var img = document.querySelector("head > link:nth-child(2)").href
    img = 'images/'+img.split('/').pop()+'.png'

    code='';
    // extract code
    setTimeout(function(){
        Tesseract.recognize(img).then(function(result){code=result.text;});
    }, 500)

    // set lock code and click
    setTimeout(function(){
        code = code.slice(0,8);
        document.querySelector("body > div > ul > li:nth-child(7) > div > input").value = code;
        document.querySelector("body > div > ul > li:nth-child(7) > div > button").disabled=0;
        document.querySelector("body > div > ul > li:nth-child(7) > div > button").click();
    }, 2500)
})();