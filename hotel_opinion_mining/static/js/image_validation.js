function filevalidation() {
  const file = document.getElementById('image');
    
  var filePath = file.value;
  console.log(filePath);
  var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    
  if (!allowedExtensions.exec(filePath)) {
      alert('Invalid file type');
      file.value = '';
      return false;
  } 
 
}

function onSubmit() {

      alert('Your FeedBack will now be recorded. Thank you for your support');
 
}