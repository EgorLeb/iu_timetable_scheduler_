const uplDesign = document.getElementById("upload-design");
const uploadButton = document.getElementById("upl");
const huge = document.getElementById("huge");
const closeBtn = document.getElementById("closeBtn");
const dropZone = document.getElementById("drop-zone");
const downDesign = document.getElementById("download-design");
const redo = document.getElementById("redo");
const selectFile = document.getElementById("uploadbtn");
const selfile = document.getElementById("selfile")

const regEx = /[\s\S]*\\pages\\([\S]*).html/;

function ext(name) {
    return name.match(/\.([^.]+)$|$/)[1]
}

function resolve(paths) {
    const result = regEx.exec(paths);
    if (result && result.length >= 2) {
            return result[1].replace('index', '');
    }
    return null;
}

uploadButton.addEventListener('click', (event) => {
    uplDesign.classList.add("hidden");
    huge.classList.remove("hidden");
});

closeBtn.addEventListener('click', (event) => {
    uplDesign.classList.remove("hidden");
    huge.classList.add("hidden");
});

dropZone.addEventListener('dragover', event => {
  event.stopPropagation();
  event.preventDefault();
  event.dataTransfer.dropEffect = 'copy';
});

dropZone.addEventListener('drop', event => {
    event.stopPropagation();
    event.preventDefault();
});


redo.addEventListener('click', (event) => {
    uplDesign.classList.remove("hidden");
    downDesign.classList.add("hidden");
});

function processSelectedFiles(fileInput) {
    var files = fileInput.files;
    console.log(3)
    if (ext(files[0].name)==="xlsx") {
        selfile.innerHTML = files[0].name
    } else {
        alert("Invalid file type")
    }
};