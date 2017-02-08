/**
 * Created by manish on 5/2/17.
 */
var file;
var path;
var obj = $("#dragandrophandler");
$("document").ready(function () {
    $('#selected').hide();
    //Upload Button Events
    $("#uploadImage").click(function () {
        openfileInput()
    });
    $("#file").change(function () {
        file = $('#file').prop("files")[0];
        showFileName($("#file").val());
        if (checkImage($("#file").val())) {
            path = URL.createObjectURL(file);
            console.log(path);
            uploadImage(path);
        }
        else {
            $("#filename").val("");
            alert("wrong File");
        }
    });

    //Drag and Drop
    obj.on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px dotted black');
    });

    obj.on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });

    obj.on('drop', function (e) {
        e.preventDefault();
        file = e.originalEvent.dataTransfer.files[0];
        if (checkImage(file.name)) {
            $("#filename").val(file.name);
            path = URL.createObjectURL(file);
            $("input[type='file']").prop("files", e.originalEvent.dataTransfer.files);
            console.log(path);
            uploadImage(path);
        }
        else {
            $("#filename").val("");
            alert("wrong File");
        }
    });

    // Removes the Image
    $('#remove').on('click', function () {
        $('#selected').hide();
        $('#uploadForm').show();
        $('#file').val("");
    });

    // Submit the Image
    $('#submit').on('click', function () {
        $('#uploadForm').submit();
    });
});

//File Upload using Button
function openfileInput() {
    $('#file').click();
}

function showFileName() {
    var filename = $('#file').val();
    filename = filename.replace(/.*[\/\\]/, '');
    $("#filename").val(filename).focus();
}

//Drag and Drop
$(document).on('dragenter', function (e) {
    e.stopPropagation();
    e.preventDefault();
});

$(document).on('dragover', function (e) {
    e.stopPropagation();
    e.preventDefault();
});

$(document).on('drop', function (e) {
    e.stopPropagation();
    e.preventDefault();
});

//Valid Image
function checkImage(fileName) {
    if (fileName.match(/.(jpg|jpeg|png)$/i)) {
        return 1;
    }
    return 0;
}

//Upload Image
function uploadImage(data) {
    $('#selected').show();
    $('#selectedImage').attr('src', data);
    $('#uploadForm').hide();
    //alert(data);
    //$('#uploadForm').submit();
}
