document.addEventListener("DOMContentLoaded", function () {
  const modeToggle = document.getElementById("mode-toggle");
  const modeLabel = document.getElementById("mode-label");

  modeToggle.addEventListener("change", function () {
    document.body.classList.toggle("dark-mode");
    if (document.body.classList.contains("dark-mode")) {
      modeLabel.textContent = "Dark Mode";
    } else {
      modeLabel.textContent = "Light Mode";
    }
  });
});
