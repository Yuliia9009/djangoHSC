// document.addEventListener("DOMContentLoaded", function () {
//   const form = document.querySelector("#searchForm");
//   const overlay = document.getElementById("loadingOverlay");
//
//   if (form && overlay) {
//     form.addEventListener("submit", function () {
//       overlay.classList.remove("d-none");
//     });
//   }
// });

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#searchForm");
  const overlay = document.getElementById("loadingOverlay");

  if (form && overlay) {
    form.addEventListener("submit", function (e) {
      console.log("submit triggered");
      // Показать индикатор
      overlay.classList.remove("d-none");

      // Задержка перед отправкой формы
      e.preventDefault();

      setTimeout(() => {
        form.submit();
      }, 300);
    });
  }
});