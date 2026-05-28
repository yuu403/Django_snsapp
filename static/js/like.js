document.addEventListener('DOMContentLoaded', () => {

    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(btn => {
        btn.addEventListener('click', async function (e) {
            e.preventDefault();

            const postId = this.dataset.id;

            const res = await fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            });

            const data = await res.json();

            const icon = this.querySelector('i');
            const count = this.nextElementSibling;

            count.textContent = data.like_count;

            icon.classList.toggle('fas', data.liked);
            icon.classList.toggle('far', !data.liked);
        });
    });

});