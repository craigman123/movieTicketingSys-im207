function previewImage(event){
    const reader = new FileReader();
    reader.onload = function(){
        const img = document.getElementById("imagePreview");
        img.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

function previewVideo(event){
    const file = event.target.files[0];
    const video = document.getElementById("videoPreview");
    video.src = URL.createObjectURL(file);
}

function selectType(button){
    document.querySelectorAll(".availability button")
        .forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");
}