$(document).ready(function() {
    $('#id_titulo').on('change', function() {
      var selectedOption = $(this).find(':selected');
      var imageUrl = selectedOption.data('url');
      $('#id_archivo').val(imageUrl);
      $('#imagen-preview').attr('src', imageUrl);
    });
  });
  