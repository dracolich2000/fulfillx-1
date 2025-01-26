document.addEventListener("DOMContentLoaded", () => {
    // Get all tab elements and content containers
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");
    const container = document.querySelector(".tab-container") || document.querySelector(".product-container") || document.querySelector(".container") || document.querySelector(".sourcing-container");

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

// Get modal elements
const modal = document.getElementById('shopifyModal'); // The modal container
const openModalBtn = document.getElementById('openModalBtn'); // The button to open the modal
const closeModalBtn = document.getElementById('closeModalBtn'); // The close button inside the modal

// Open modal
openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block'; // Show the modal
});

// Close modal
closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none'; // Hide the modal
});

// Close modal when clicking outside of it
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

//view product page: image switching
//
function switchImage(imageUrl) {
    const mainImage = document.getElementById('mainImage');
    mainImage.src = imageUrl;
}

function openShopifyModal(button) {
    // Get data from button attributes
    const productId = button.getAttribute('data-product-id');
    const productImage = button.getAttribute('data-product-image');
    const productName = button.getAttribute('data-product-name');
    const productDescription = button.getAttribute('data-product-description');
    const productBasePrice = parseFloat(button.getAttribute('data-product-price'));

    // Set modal content
    document.getElementById('productImage').src = productImage;
    document.getElementById('productName').innerText = productName;
    document.getElementById('productDescription').innerText = productDescription;
    document.getElementById('product_id').value = productId;

    // Store the base price globally
    window.productBasePrice = productBasePrice;

    // Show the modal
    document.getElementById('shopifyModal').style.display = 'block';

    // Attach the event listener for the input field (only once)
    const setPriceInput = document.getElementById('productPrice');
    if (!setPriceInput.dataset.listenerAttached) {
        setPriceInput.addEventListener('input', calculateMargin);
        setPriceInput.dataset.listenerAttached = true; // Mark listener as attached
    }
}

// Close Modal
function closeShopifyModal() {
    document.getElementById('shopifyModal').style.display = 'none';
}

// push to shopify modal: calculate margin
//
function calculateMargin() {
    const setPriceInput = document.getElementById('productPrice');
    const marginDisplay = document.getElementById('margin-display');

    // Get the set price value
    const setPrice = parseFloat(setPriceInput.value);

    if (!isNaN(setPrice) && setPrice > 0) {
        const margin = setPrice - window.productBasePrice;
        marginDisplay.textContent = `Margin: ₹${margin.toFixed(2)}`;
    } else {
        marginDisplay.textContent = 'Margin: ₹0.00';
    }
}

// Close the modal if clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('shopifyModal');
    if (event.target === modal) {
        closeShopifyModal();
    }
};
