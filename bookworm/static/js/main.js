$(function() {
    $('#search-input').on('keypress', function(event) {
        if (event.which === 13) {
            $(this).closest('form').submit();
        }
    });
});

// modal profile

document.addEventListener('DOMContentLoaded', function(){
  // Получаем элемент профиля
  var profileUsername = document.querySelector('.profile__pencil_for__edit');

  // Прислушиваемся к событию клика
  profileUsername.addEventListener('click', function () {
    console.log("sdsadas")
    const usernameInput = document.querySelector('#modal_profile form input[name="username"]');
    const firstNameInput = document.querySelector('#modal_profile form input[name="first_name"]');
    const lastNameInput = document.querySelector('#modal_profile form input[name="last_name"]');

    const modalUsername = document.getElementById('modal__profile_example_username');
    const modalFio = document.getElementById('modal__profile_example_fio');

    function updateModalProfileExample() {
        console.log("Editi")
        modalUsername.textContent = usernameInput.value;
        modalFio.textContent = `${firstNameInput.value} ${lastNameInput.value}`;
    }

    // Call the function immediately to update the modal example with initial values
    updateModalProfileExample();

    usernameInput.addEventListener('input', updateModalProfileExample);
    firstNameInput.addEventListener('input', updateModalProfileExample);
    lastNameInput.addEventListener('input', updateModalProfileExample);

  });
});


// Получаем идентификатор комментария из URL
const commentId = window.location.hash.replace('#', '');

// Если идентификатор комментария существует, пролистываем до комментария
if (commentId) {
  const commentElement = document.getElementById(commentId);
  if (commentElement) {
    commentElement.scrollIntoView();
  }
}

// Настройки Toastify

toastr.options = {
  "closeButton": true,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": true,
  "onclick": null,
  "showDuration": "200",
  "hideDuration": "200",
  "timeOut": "3000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

// Копирование ссылки в буфер обмена
document.addEventListener('DOMContentLoaded', function(){
  // Получаем родительский элемент
  var commentsContainer = document.querySelector('.book_comments_list__wrapper');

  // Прислушиваемся к событию клика
  commentsContainer.addEventListener('click', function (event) {
    // Проверяем, является ли целевой элемент элементом с идентификатором copy-link
    if (event.target.id === 'copy-link') {
        // Получаем значение атрибута data-link
        var link = event.target.getAttribute('data-link');

        // Копируем ссылку в буфер обмена
        navigator.clipboard.writeText(link).then(() => {
        toastr.success('Ссылка скопирована в буфер обмена!');
        }).catch((error) => {
        console.error('Error copying link to clipboard:', error);
        });
    }
  });
});
