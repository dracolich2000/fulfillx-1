// Function to open the modal and set the product id
function openUpdateInventoryModal(button) {
    const productId = button.getAttribute('data-product-id');
    const productInventory = button.getAttribute('data-product-inventory');

    document.getElementById('product_id').value = productId;
    document.getElementById('product_inventory').value = productInventory;
    document.getElementById('updateInventoryModal').style.display = 'block';  // Show the modal
}

// Function to close the modal
function closeModal() {
    document.getElementById('updateInventoryModal').style.display = 'none';  // Hide the modal
}

// Close modal when clicking outside the modal content
window.onclick = function(event) {
    var modal = document.getElementById('updateInventoryModal');
    if (event.target == modal) {
        closeModal();
    }
}
