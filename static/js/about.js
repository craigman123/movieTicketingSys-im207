function expandCard(selected) {
    const cards = document.querySelectorAll(".card");

    if (selected.classList.contains("expanded")) {
        // Collapse card: restore original image
        const imgTag = selected.querySelector(".card-img img");
        imgTag.src = imgTag.dataset.original; // restore original
        selected.classList.remove("expanded");
        cards.forEach(card => card.classList.remove("hide"));
        return;
    }

    cards.forEach(card => {
        if (card !== selected) {
            card.classList.add("hide");
            card.classList.remove("expanded");
            // Restore their original images too
            const imgTag = card.querySelector(".card-img img");
            if (imgTag.dataset.original) imgTag.src = imgTag.dataset.original;
        }
    });

    // Expand the clicked card
    selected.classList.add("expanded");

    // Swap the image
    const imgTag = selected.querySelector(".card-img img");
    if (!imgTag.dataset.original) {
        imgTag.dataset.original = imgTag.src; // save original image
    }
    imgTag.src = selected.dataset.altImg; // replace with alternate image
}