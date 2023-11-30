document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("file");
  const imgArea = document.querySelector(".img-area");

  fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];

    if (file) {
      const reader = new FileReader();

      reader.onload = function (e) {
        imgArea.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
      };

      reader.readAsDataURL(file);
    }
  });
});
