"use strict";
var $ = jQuery;
$('input:radio[name="datasource"]').change(
    function() {
        if ($(this).is(':checked')) {

            if ($(this).val() === 'mockjson') {
                $('#jsonupload-input').hide(100);
                $('#eventapi-input').hide(100);
            }

            if ($(this).val() === 'jsonupload') {
                $('#jsonupload-input').show(100);
                $('#eventapi-input').hide(100);
            }

            if ($(this).val() === 'eventapi') {
                $('#eventapi-input').show(100);
                $('#jsonupload-input').hide(100);
            }
        }
    });
var timestamp = Number(new Date());
var form = document.querySelector("form");
var config = {
    apiKey: "AIzaSyDTo4TPzUkvYYN5dwvNnI4jVmB_eTc0Lpo",
    authDomain: "app-generator.firebaseapp.com",
    databaseURL: "https://app-generator.firebaseio.com",
    storageBucket: "app-generator.appspot.com",
};
firebase.initializeApp(config);
var file = document.getElementById('uploadZip');
file.onchange = function(e) {
    var ext = this.value.match(/\.([^\.]+)$/)[1];
    switch (ext) {
        case 'zip':
            $('.progress').show();
            $('#upload-progress').show();
            $('#submit').hide();
            uploadFile();
            break;
        default:
            alert('Only zip files are allowed');
            this.value = '';
    }
};
var database = firebase.database();
form.addEventListener("submit", function(event) {
    event.preventDefault();
    $('.progress').css('display', 'block');
    $('#generator-progress').css('display', 'block')
    $('#upload-progress').css('display', 'block')
    var ary = $(form).serializeArray();
    var obj = {};
    updatePercentUpload(10);
    for (var a = 0; a < ary.length; a++) obj[ary[a].name] = ary[a].value;
    console.log("JSON", obj);
    if (obj.Email == "" || obj.App_Name == "") {
        alert("It seems like you forgot to fill up your email address or app's name");
        setTimeout("location.reload(true);", 1);
    } else {
        var file_data = $('#uploadZip').prop('files')[0];
        var form_data = new FormData();
        form_data.append('file', file_data);
        firebase.database().ref('users/' + timestamp).set(obj);
        database.ref('users/' + timestamp).once('value').then(function(snapshot) {
            updatePercentUpload(10);
            console.log("Received value", snapshot.val());
            document.getElementById("status").innerHTML = "Building the app. This might take a while...";
            ajaxCall1();

            function ajaxCall1() {
                updatePercentUpload(35);
                $.ajax({
                    type: "POST",
                    url: "/runPy.php",
                    data: {
                        timestamp: timestamp
                    },
                    success: function(response) {
                        console.log("Success", response);
                        updatePercentUpload(100);
                        window.location = response;
                        document.getElementById("status").innerHTML = "App build completed!";
                    }
                });
            }
        });
    }
}); //after this
function updatePercentUpload(perc) {
    $('#upload-progress').css('width', perc + '%');
    $('#upload-progress').html(parseInt(perc) + '%');
}

function uploadFile() {

    var file_data = $('#uploadZip').prop('files')[0];
    var form_data = new FormData();
    form_data.append('file', file_data);
    form_data.append('timestamp', timestamp);
    var ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.open("POST", "upload.php");
    ajax.send(form_data);

}

function progressHandler(event) {
    var percent = (event.loaded / event.total) * 100;
    updatePercentUpload(Math.round(percent))
    document.getElementById("status").innerHTML = Math.round(percent) + "% uploaded... please wait";
}

function completeHandler(event) {
    document.getElementById("status").innerHTML = "Upload Complete, click on the button below to build your app";
    $('#submit').show();
}
