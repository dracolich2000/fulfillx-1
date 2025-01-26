document.addEventListener("DOMContentLoaded", () => {
    // Get all tab elements and content containers
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");
    const container = document.querySelector(".tab-container") || document.querySelector(".product-container") || document.querySelector(".container");

    if (!tabs.length || !contents.length || !container) {
        console.warn("No tabs, contents, or container found. Ensure your HTML structure includes .tab and .tab-content elements.");
        return;
    }

    // Determine the active tab based on the hash in the URL
    const hash = window.location.hash;
    let activeTab = tabs[0].dataset.tab; // Default to the first tab

    if (hash) {
        const hashTab = hash.substring(1);
        const validTab = Array.from(tabs).some(tab => tab.dataset.tab === hashTab);
        if (validTab) activeTab = hashTab;
    }

    // Activate the correct tab and content on load
    tabs.forEach(tab => {
        tab.classList.toggle("active", tab.dataset.tab === activeTab);
    });
    contents.forEach(content => {
        content.classList.toggle("active", content.id === activeTab);
    });

    // Show the container after initializing the tabs
    container.removeAttribute("hidden");

    // Add click event listeners for tabs
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const targetTab = tab.dataset.tab;

            // Remove active class from all tabs and contents
            tabs.forEach(tab => tab.classList.remove("active"));
            contents.forEach(content => content.classList.remove("active"));

            // Add active class to the clicked tab and its content
            tab.classList.add("active");
            document.getElementById(targetTab).classList.add("active");

            // Update the URL hash without reloading the page
            history.replaceState(null, null, `#${targetTab}`);
        });
    });
});

function openSourcingForm(requestId) {
    // Populate user_id in the hidden input
    document.getElementById("request_id").value = requestId;

    // Display the modal
    const modal = document.getElementById("SourcingModal");
    modal.style.display = "block";
}

function closeSourcingForm() {
    // Hide the modal
    const modal = document.getElementById("SourcingModal");
    modal.style.display = "none";
}

// Optional: Close modal when clicking outside of it
window.onclick = function (event) {
    const modal = document.getElementById("SourcingModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

function deleteImage(imageId) {
    // Get the image element and the associated checkbox
    const imageItem = document.getElementById('image-' + imageId); // The div containing the image
    const checkbox = imageItem.querySelector('input[name="delete_images"]'); // The hidden checkbox for deletion

    if (imageItem && checkbox) {
        // Mark the checkbox as checked (indicating that this image is to be deleted)
        checkbox.checked = true;

        // Hide the image and the delete button
        imageItem.style.display = 'none';
    }
}

// Optional: You can add logic to ensure that images marked for deletion are passed correctly when the form is submitted.
document.querySelector('form').addEventListener('submit', function() {
    let deleteImages = document.querySelectorAll('input[name="delete_images"]:checked');
    deleteImages.forEach(input => {
        console.log(input.value); // Log the IDs of images being deleted
    });
});

//add product page: select vendor
//
jQuery(document).ready(function() {
    jQuery('#vendor').select2({
        placeholder: "Select a vendor",
        allowClear: true
    });
});

//upload csv modal
//
function openCsvForm(userId) {
    const modal = document.getElementById("csvModal");
    modal.style.display = "block";
}

function closeCsvForm() {
    const modal = document.getElementById("csvModal");
    modal.style.display = "none";
}

// Close modal when clicking outside of it
window.onclick = function (event) {
    const modal = document.getElementById("csvModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};