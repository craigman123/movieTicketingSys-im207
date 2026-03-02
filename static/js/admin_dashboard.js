window.addEventListener('DOMContentLoaded', () => {
    // Poster
    const posterInput = document.getElementById('fileposter');
    const posterHeader = posterInput.closest('.file-container').querySelector('.file-header');

    posterInput.addEventListener('change', function () {
        const file = this.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            posterHeader.innerHTML = `<img src="${e.target.result}" style="width:101%; height:285px; object-fit:cover; border-radius:10px;">`;
        };
        reader.readAsDataURL(file);
        BorderPoster(document.getElementById('borderposter'));
    });
});

window.addEventListener('DOMContentLoaded', () => {

    // Trailer
    const trailerInput = document.getElementById('filetrailer');
    const trailerHeader = trailerInput.closest('.file-container').querySelector('.file-header');

    trailerInput.addEventListener('change', function () {
        const file = this.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            trailerHeader.innerHTML = `<img src="${e.target.result}" style="width:101%; height:285px; object-fit:cover; border-radius:10px;">`;
        };
        reader.readAsDataURL(file);
        BorderTrial(document.getElementById('bordertrial'));
    });
});

function BorderPoster(border){
    const finalbackgroundColor = "linear-gradient(120deg, rgba(98, 255, 0, 0.521), rgba(57, 67, 55, 0.2))";
    border.style.background = `${finalbackgroundColor}`;
}

function BorderTrial(border){
    const finalbackgroundColor = "linear-gradient(120deg, rgba(98, 255, 0, 0.521), rgba(57, 67, 55, 0.2))";
    border.style.background = `${finalbackgroundColor}`;
}