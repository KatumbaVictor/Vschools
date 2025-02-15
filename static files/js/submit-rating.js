const stars = document.getElementsByClassName('star');
const form = document.getElementById('rating-form');
const submit_button = document.getElementById('submit-button');
const review_title = document.getElementById('id_review_title');
const review_comment = document.getElementById('id_review_comment')

Array.from(stars).forEach(star => {
    star.addEventListener('mouseover', () => {
        var rating_value = star.dataset.value;

        Array.from(stars).forEach(item => {
            if (item.dataset.value <= rating_value) {
                item.innerHTML = `
                    <svg class="w-6 h-6 ms-2 text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                `
            }else {
                item.innerHTML = `
                    <svg class="w-6 h-6 ms-2 text-gray-300 dark:text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>
                `
            }
        })

        document.getElementById('rating_value').innerHTML = `${rating_value} out of 5`;
        document.getElementById('rating').value = rating_value;

        if (rating_value >= 1 && review_title.value.length >= 1 && review_comment.value.length >= 1) {
            submit_button.removeAttribute('disabled');
            submit_button.classList.remove('bg-blue-400');
            submit_button.classList.add('bg-blue-700');
            submit_button.classList.add('focus:ring-4');
            submit_button.classList.remove('cursor-not-allowed');
        }
    })

    star.addEventListener('mouseleave', () => {
        Array.from(stars).forEach(item => {
            item.innerHTML = `
                <svg class="w-6 h-6 ms-2 text-gray-300 dark:text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                    <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                </svg>
            `
        })

        document.getElementById('rating_value').innerHTML = `0 out of 5`;
        document.getElementById('rating').value = 0;
    })
 })


form.addEventListener('submit', (event) => {
    event.preventDefault();

    let csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    let formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {"X-CSRFToken": csrf_token}
    }).then(response => {
        response.json().then(data => {
            if (data.success) {

            }
        })
    })
})


let manage_review_inputs = () => {
    if (review_title.value.length >= 1 && review_comment.value.length >= 1 && document.getElementById('rating').value.length != 0) {
        submit_button.removeAttribute('disabled');
        submit_button.classList.remove('bg-blue-400');
        submit_button.classList.add('bg-blue-700');
        submit_button.classList.add('focus:ring-4');
        submit_button.classList.remove('cursor-not-allowed');
    }
}

review_title.addEventListener('input', manage_review_inputs)
review_comment.addEventListener('input', manage_review_inputs)