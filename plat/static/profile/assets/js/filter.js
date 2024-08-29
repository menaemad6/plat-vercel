function groupStudentsFilterText() {
  // Get the user input
  var userInput = document.getElementById("group-students-filter-input").value;

  // Get all card-block elements
  var cardBlocks = document.getElementsByClassName("filter-block");

  // Loop through the card-block elements
  for (var i = 0; i < cardBlocks.length; i++) {
    var cardBlock = cardBlocks[i];
    var h6Element = cardBlock.getElementsByTagName("h6")[0];
    var h6Text = h6Element.textContent.toLowerCase();

    // Check if the h6 text matches the user input
    if (h6Text.includes(userInput.toLowerCase())) {
      cardBlock.style.display = "flex"; // Show the matching card block
    } else {
      cardBlock.style.display = "none"; // Hide the non-matching card block
    }
  }
}


function addStudentFilterText() {
  // Get the user input
  var studentInput = document.getElementById("add-student-filter-input").value;

  // Get all card-block elements
  var studentBlocks = document.getElementsByClassName("filter-block-add-student");

  // Loop through the card-block elements
  for (var i = 0; i < studentBlocks.length; i++) {
    var studentBlock = studentBlocks[i];
    var h6Element = studentBlock.getElementsByTagName("h6")[0];
    var h6Text = h6Element.textContent.toLowerCase();

    // Check if the h6 text matches the user input
    if (h6Text.includes(studentInput.toLowerCase())) {
      studentBlock.style.display = "flex"; // Show the matching card block
    } else {
      studentBlock.style.display = "none"; // Hide the non-matching card block
    }
  }
}



  function addLectureFilterText() {
    // Get the user input
    var userInput = document.getElementById("add-lecture-filter-input").value;
  
    // Get all card-block elements
    var cardBlocks = document.getElementsByClassName("filter-block");
  
    // Loop through the card-block elements
    for (var i = 0; i < cardBlocks.length; i++) {
      var cardBlock = cardBlocks[i];
      var h6Element = cardBlock.getElementsByTagName("h6")[0];
      var h6Text = h6Element.textContent.toLowerCase();
  
      // Check if the h6 text matches the user input
      if (h6Text.includes(userInput.toLowerCase())) {
        cardBlock.style.display = "flex"; // Show the matching card block
      } else {
        cardBlock.style.display = "none"; // Hide the non-matching card block
      }
    }
  }
  