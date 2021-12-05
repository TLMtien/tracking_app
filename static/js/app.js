// Modal da du 18t

const modalBtns = document.querySelectorAll('.js-modal-btn');
const modalOpen = document.querySelector('.js-modal-open');
const modalContainer = document.querySelector('.js-modal-container');
const modalClose = document.querySelector('.js-modal-close');

//Hàm hiển thị tab modal (thêm class open vào modal)
function showModalTab() {
    modalOpen.classList.add('open');
}

//Hàm đóng tab mocal (gỡ bỏ class open của modal)
function hideModalTab() {
    modalOpen.classList.remove('open');
}

//Dùng cho nhiều button mở modal (lặp qua từng thẻ button và nghe hành vi click)
for (const modalBtn of modalBtns) {
    modalBtn.addEventListener('click', showModalTab);
}

// Click vào icon "X" để close Tab Modal (nghe hành vi click vào button close)
modalClose.addEventListener('click', hideModalTab);

// Click vào ngoài màn hình sẽ đóng Tab Modal
modalOpen.addEventListener('click', hideModalTab);
modalContainer.addEventListener('click', function (event) {
    event.stopPropagation();
})
