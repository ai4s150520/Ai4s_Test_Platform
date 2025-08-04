document.addEventListener("DOMContentLoaded", () => {
  // --- FEATURE 1: INLINE PROFILE EDITING ---
  const editProfileBtn = document.getElementById("editProfileBtn");
  const saveProfileBtn = document.getElementById("saveProfileBtn");
  const cancelEditBtn = document.getElementById("cancelEditBtn");
  const editActionsDiv = document.getElementById("editActions");

  const emailText = document.getElementById("emailText");
  const emailInput = document.getElementById("emailInput");

  if (editProfileBtn) {
    editProfileBtn.addEventListener("click", () => {
      // Hide the 'Edit' button and the static text
      editProfileBtn.style.display = "none";
      emailText.style.display = "none";

      // Show the 'Save/Cancel' buttons and the input field
      editActionsDiv.style.display = "flex";
      emailInput.style.display = "block";
      emailInput.focus();
    });
  }

  if (cancelEditBtn) {
    cancelEditBtn.addEventListener("click", () => {
      // Hide the 'Save/Cancel' buttons and the input field
      editActionsDiv.style.display = "none";
      emailInput.style.display = "none";

      // Show the 'Edit' button and the static text again
      editProfileBtn.style.display = "block";
      emailText.style.display = "block";

      // Reset input value to original, in case it was changed
      emailInput.value = emailText.textContent;
    });
  }

  if (saveProfileBtn) {
    // In a real app, this would submit the form via AJAX (fetch)
    // For now, it just reverts the UI like the cancel button
    saveProfileBtn.addEventListener("click", () => {
      // Update the text with the new input value
      emailText.textContent = emailInput.value;

      // Revert UI back to view mode
      cancelEditBtn.click();
    });
  }

  // --- FEATURE 2: AVATAR UPLOAD PREVIEW ---
  const avatarUploadInput = document.getElementById("avatarUpload");
  const avatarPreview = document.getElementById("avatarPreview");

  if (avatarUploadInput) {
    avatarUploadInput.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file) {
        // Use FileReader to get a temporary URL for the selected image
        const reader = new FileReader();
        reader.onload = (e) => {
          avatarPreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // --- FEATURE 3: DELETE ACCOUNT CONFIRMATION MODAL ---
  document.addEventListener('DOMContentLoaded', function() {
  var btn = document.getElementById('deleteAccountBtn');
  var modal = document.getElementById('deleteConfirmModal');
  var cancel = document.getElementById('cancelDeleteBtn');
  var confirm = document.getElementById('confirmDeleteBtn');

  if(btn && modal) {
    btn.onclick = function() {
      modal.style.display = 'flex'; // or 'block' — depends on your CSS!
    };
  }
  if(cancel && modal) {
    cancel.onclick = function() {
      modal.style.display = 'none';
    };
  }
  if(confirm) {
    confirm.onclick = function() {
      document.getElementById('deleteForm').submit();
    };
  }
});
