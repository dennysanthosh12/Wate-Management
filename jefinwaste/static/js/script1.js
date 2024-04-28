document.addEventListener("DOMContentLoaded", function() {
    var footerText = "@DennySanthosh. All rights reserved.";

    // Check if the footer container exists
    var footerContainer = document.getElementById("footer-container");

    // Verify if the footer container exists before manipulating it
    if (footerContainer) {
        // Create a paragraph element for the footer text
        var paragraph = document.createElement("p");
        paragraph.textContent = footerText;

        // Append the paragraph element to the footer container
        footerContainer.appendChild(paragraph);
    } else {
        console.error("Footer container not found!");
    }
});