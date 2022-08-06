async function getDataFromServer(url) {
    var response_text = await awaitHttpGet(url);
    
    return JSON.parse(response_text)
}

async function postDataFromServer(url, data) {
    var response_text = await awaitHttpPost(url, data);
    
    return JSON.parse(response_text)
}

function awaitHttpGet(url){
    /*
        Input:
        - url: (string) the url that you want to send request to
        - postProcesses: (function) This is the function that should be executed after
            we got the response from the server `
    */
    

    return new Promise(function(resolve, reject) {

        var xmlHttp = new XMLHttpRequest();

        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState === XMLHttpRequest.DONE) {
                if (xmlHttp.status === 200) {
                    resolve(xmlHttp.responseText)
                }
                else {
                    reject("Error")
                }
            }
        }

        var key = "nanshanddctablet"
        var secret = "238lskdfy923hklegoghi"
        var time_shift = 8

        xmlHttp.open("GET", url);
        xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlHttp.setRequestHeader("Gadgethi-Key", key.toString())
        xmlHttp.setRequestHeader("Hmac256-Result", HMAC256_encryption(key, secret, time_shift).toString())
        xmlHttp.setRequestHeader("time", (time_standard(time_shift)).toString())
        xmlHttp.send(null);

    })
}

function awaitHttpPost(url, postData){
    /*
        Input:
        - url: (string) the url that you want to send request to
        - postProcesses: (function) This is the function that should be executed after
            we got the response from the server `
    */
    

    return new Promise(function(resolve, reject) {

        var xmlHttp = new XMLHttpRequest();

        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState === XMLHttpRequest.DONE) {
                if (xmlHttp.status === 200) {
                    resolve(xmlHttp.responseText)
                }
                else {
                    reject("Error")
                }
            }
        }

        xmlHttp.open("POST", url);
        xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlHttp.send(postData);

    })
}

function dict2urlEncode(dictionary) {
    /*
        This is the helper function that helps change dictionary to 
        urlencoded string. 
    */
    var str = [];
    for(var p in dictionary)
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(dictionary[p]));
    return str.join("&");
}

function time_standard(time_shift) {

    var time = new Date()
    var correct_time = time.getTimezoneOffset() * 60 + time.getTime() / 1000
    return parseInt(correct_time) + (time_shift*60*60)
}

function HMAC256_encryption(key, secret, time_shift) {
    // We standardize Taipei as the standard time
    var CryptoJS = require("crypto-js");

    var time = new Date()
    var correct_time = time.getTimezoneOffset() * 60 + time.getTime() / 1000

    var localtime = parseInt(correct_time) + (time_shift*60*60)
    var hash = CryptoJS.HmacSHA256(key+(localtime).toString(), secret)
    var encryption_result = CryptoJS.enc.Base64.stringify(hash)

    return encryption_result
}