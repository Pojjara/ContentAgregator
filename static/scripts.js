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
        form.style.opacity = '1';
        form.style.display = 'block';
    });
});

function validateForm() {
    let link = document.forms["AddingAmazonItem"]["link"].value;
    let price = document.form['AddingAmazonItem']['price'].value;
    if (link == "" && price == '') {
        alert("Link and Price must be filled out");
        return false;
      }
    if (link == "") {
      alert("Link must be filled out");
      return false;
    }
    if (price == "") {
        alert("Link must be filled out");
        return false;
      }
  }