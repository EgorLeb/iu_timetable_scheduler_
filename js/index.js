const uplDesign = document.getElementById("upload-design");
const uploadButton = document.getElementById("upl");
const huge = document.getElementById("huge");
const closeBtn = document.getElementById("closeBtn");
const dropZone = document.getElementById("drop-zone");
const downDesign = document.getElementById("download-design");
const redo = document.getElementById("redo");
const selectFile = document.getElementById("uploadbtn");

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
    huge.classList.add("hidden");
    downDesign.classList.remove("hidden");
});

redo.addEventListener('click', (event) => {
    uplDesign.classList.remove("hidden");
    downDesign.classList.add("hidden");
});

selectFile.addEventListener('change', (event) => {
    huge.classList.add("hidden");
    downDesign.classList.remove("hidden");
});