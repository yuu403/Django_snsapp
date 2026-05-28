document.addEventListener('DOMContentLoaded', () => {

    const followButtons = document.querySelectorAll('.follow-btn');

    followButtons.forEach(btn => {
        btn.addEventListener('click', async function (e) {
            e.preventDefault();

            const userId = this.dataset.id;

            const res = await fetch(`/users/${userId}/follow/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            });

            const data = await res.json();

            this.textContent = data.followed ? 'フォロー解除' : 'フォロー';
        });
    });

});