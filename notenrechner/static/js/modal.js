var modal = document.querySelector('.modal');
var closeButtons = document.querySelectorAll('.close-modal');
var openButtons = document.querySelectorAll('.open-modal');

if (openButtons!=null) {
  // set open modal behaviour
  for (i = 0; i < openButtons.length; ++i) {
    openButtons[i].addEventListener('click', function() {
      url = $(this).attr('action')
      $("#modal-decision").attr('action', url)
      $(".modal-content-inner").load(url, function () {
        modal.classList.toggle('modal-open');
      });
    });
  }
  // set close modal behaviour
  for (i = 0; i < closeButtons.length; ++i) {
    closeButtons[i].addEventListener('click', function() {
      modal.classList.toggle('modal-open');
  	});
  }
  // close modal if clicked outside content area
  document.querySelector('.modal-inner').addEventListener('click', function() {
    modal.classList.toggle('modal-open');
  });
  // prevent modal inner from closing parent when clicked
  document.querySelector('.modal-content').addEventListener('click', function(e) {
  	e.stopPropagation();
  });
  modal.classList.toggle('modal-open');
}
else {
  modal.classList.toggle('modal-open');
}
