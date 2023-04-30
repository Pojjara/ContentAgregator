function open_form() {
    document.getElementsByClassName("plus_sign")
}

// get all elements with class "plus_sign"
const plusSigns = document.querySelectorAll('.plus_sign');

// loop through each plus_sign element
plusSigns.forEach(plusSign => {
    // add click event listener to each plus_sign element
    plusSign.addEventListener('click', () => {
        // hide the plus_sign element
        plusSign.style.display = 'none';
        // show the form element
        const form = document.querySelector('.form');
        form.style.display = 'block';
    });
});