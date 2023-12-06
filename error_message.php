<!-- error_message.php -->

<div class="error-message">
  <div class="error-content">
    <span class="close-button" onclick="closeErrorMessage()">&times;</span>
    <?php echo $error_message; ?>
  </div>
</div>

<style>
  /* Add styling for the error message */
  .error-message {
    position: fixed;
    top: 4rem; /* Adjust the top position as needed */
    left: 70rem; /* Adjust the left position as needed */
    width: 300px;
    padding: 15px;
    background-color: #f44336;
    color: white;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }

  .error-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .close-button {
    cursor: pointer;
    font-size: 20px;
    font-weight: bold;
  }
</style>

<script>
  // Add JavaScript function to close the error message
  function closeErrorMessage() {
    var errorMessage = document.querySelector('.error-message');
    errorMessage.style.display = 'none';
  }
</script>
