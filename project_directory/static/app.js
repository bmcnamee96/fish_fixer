document.addEventListener('DOMContentLoaded', () => {
    const useServiceButton = document.getElementById('useServiceButton');
    const messageDiv = document.getElementById('message');
    const formContainer = document.getElementById('formContainer');
    const closeFormButton = document.getElementById('closeForm');
    const serviceForm = document.getElementById('serviceForm'); // Ensure 'serviceForm' is an ID
    const directionsContainer = document.getElementById('directionsContainer');
    const supportContainer = document.getElementById('supportContainer');
    
    // Modal elements
    const modal = document.getElementById('responseModal');
    const closeModalButton = document.getElementsByClassName('close')[0];
    const modalText = document.getElementById('modalText');
    const spinner = document.getElementById('spinner');

    console.log('JavaScript loaded'); // Check if script is loaded

    function checkFreeUses() {
        console.log('Button clicked');
        let freeUses = parseInt(localStorage.getItem('freeUses')) || 2;
        if (freeUses > 0) {
            localStorage.setItem('freeUses', freeUses - 1);
            showForm();
        } else {
            messageDiv.textContent = 'Subscription required';
            // Optionally, show subscription options here
        }
    }

    function showForm() {
        console.log('Showing form');
        formContainer.classList.remove('hidden');
    }

    function hideForm() {
        console.log('Hiding form');
        formContainer.classList.add('hidden');
    }

    function showSpinner() {
        console.log('Showing spinner');
        spinner.style.display = 'block';
    }

    function hideSpinner() {
        console.log('Hiding spinner');
        spinner.style.display = 'none';
    }

    function showModal(responseText) {
        console.log('Showing modal with text:', responseText);
        const formattedText = responseText
            .replace(/^\*\*(.*?)\*\*$/gm, '<h1>$1</h1>') // Heading formatting
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text formatting
            .replace(/\n/g, '<br>') // Convert new lines to <br>
            .replace(/<\/li>\s*$/, '</li>'); // Close the last list item

        modalText.innerHTML = formattedText;
        modal.style.display = "block";
    }

    function submitForm(event) {
        event.preventDefault();
        showSpinner();
        
        hideForm();

        const formData = new FormData(serviceForm);
        const formDataObj = {};
        formData.forEach((value, key) => {
            formDataObj[key] = value;
        });
    
        fetch('/use_service', {
            method: 'POST',
            body: JSON.stringify(formDataObj),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Data received:', data);
            if (data.success) {
                showModal(data.response);
                hideForm(); // Ensure hideForm() is defined or remove if unnecessary
            } else {
                messageDiv.textContent = data.message;
            }
        })
        .catch(error => {
            messageDiv.textContent = 'Error: ' + error.message;
        })
        .finally(() => {
            hideSpinner();
        });
    }

    closeModalButton.onclick = function() {
        modal.style.display = "none";
        directionsContainer.classList.remove('hidden');
        supportContainer.classList.remove('hidden'); 
        formContainer.classList.add('hidden'); // Ensure the form is hidden   
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    if (useServiceButton) {
        useServiceButton.addEventListener('click', function() {
            checkFreeUses(); // Call the function with parentheses
            directionsContainer.classList.add('hidden');
            supportContainer.classList.add('hidden')
            formContainer.classList.remove('hidden');
        });
    }

    if (closeFormButton) {
        closeFormButton.addEventListener('click', function() {
            hideForm(); // Call the function with parentheses
            formContainer.classList.add('hidden');
            directionsContainer.classList.remove('hidden');
            supportContainer.classList.remove('hidden');
        });
    }

    if (serviceForm) {
        serviceForm.addEventListener('submit', submitForm);
    }
});
