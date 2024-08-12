document.addEventListener('DOMContentLoaded', () => {
    const useServiceButton = document.getElementById('useServiceButton');
    const messageDiv = document.getElementById('message');
    const formContainer = document.getElementById('formContainer');
    const closeFormButton = document.getElementById('closeForm');
    const serviceForm = document.getElementById('serviceForm');
    const directionsContainer = document.getElementById('directionsContainer');
    const supportContainer = document.getElementById('supportContainer');
    
    // Modal elements
    const modal = document.getElementById('responseModal');
    const closeModalButton = document.getElementsByClassName('close')[0];
    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    } else {
        console.error("Close button not found");
    }
    const spinner = document.getElementById('spinner');
    const fileInput = document.getElementById('photo'); 

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

    // Show / hide the form for a user to fill out
    function showForm() {
        console.log('Showing form');
        formContainer.classList.remove('hidden');
    }

    function hideForm() {
        console.log('Hiding form');
        formContainer.classList.add('hidden');
    }

    // show / hide the spinner when loading
    function showSpinner() {
        console.log('Showing spinner');
        spinner.style.display = 'block';
    }

    function hideSpinner() {
        console.log('Hiding spinner');
        spinner.style.display = 'none';
    }

    function formatContent(content) {
        return `
            <div style="text-align: left;">
                ${content}
            </div>
        `;
    }

    // show the response diagnosis
    function showModal(responseText) {
        console.log('Showing modal with text:', responseText);
        
        // Apply formatting to the response text
        const formattedText = responseText
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text formatting
            .replace(/^\*\*(.*?)\*\*$/gm, '<h1>$1</h1>') // Heading formatting
            .replace(/\n/g, '<br>') // Convert new lines to <br>
            .replace(/<\/li>\s*$/, '</li>'); // Close the last list item
    
        // Inject the formatted text into the modal
        var modal = document.getElementById("responseModal");
        var modalText = document.getElementById("modalText");
        modalText.innerHTML = formatContent(formattedText);
        modal.style.display = "block";
    }

    // Convert file to Base64 string
    function convertFileToBase64(file, callback) {
        const reader = new FileReader();
        reader.onloadend = function () {
            callback(reader.result);
        };
        reader.readAsDataURL(file);
    }
    
    // Display image
    function displayImage(base64String) {
        const imgElement = document.createElement('img');
        imgElement.src = base64String;
        document.body.appendChild(imgElement);
    }

    // submit the form
    function submitForm(event) {
        event.preventDefault();
        showSpinner();
        
        hideForm();
    
        const formData = new FormData(serviceForm);
        const file = fileInput.files[0];
        
        if (file) {
            formData.append('photo', file);
        }
    
        // Log the FormData contents for debugging
        for (const [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }
    
        fetch('/use_service', {
            method: 'POST',
            body: formData // Send FormData directly
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

    // Function to close the modal
    function closeModal() {
        var modal = document.getElementById("responseModal");
        if (modal) {
            modal.style.display = "none";
        } else {
            console.error("Modal element not found");
        }
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
// // Function to display the modal with formatted content
// function showModal(responseText) {
//     console.log('Showing modal with text:', responseText);
//     var modal = document.getElementById("responseModal");
//     var modalText = document.getElementById("modalText");
//     const formattedText = responseText
//         .replace(/^\*\*(.*?)\*\*$/gm, '<h1>$1</h1>') // Heading formatting
//         .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text formatting
//         .replace(/\n/g, '<br>'); // Convert new lines to <br>

//     modalText.innerHTML = formattedText;
//     modal.style.display = "block";
// }

// // Event listener for the test button
// document.getElementById('testModalButton').addEventListener('click', function() {
//     const testContent = `
//         **Diagnosis**: \n
//         Based on the symptoms provided (f, e, c, e, s) and the species being a Discus fish, the most likely condition is **Flukes**. Other possible diagnoses could include **Ich (White Spot Disease)** or **Columnaris**.\n\n
//         **Symptoms to Monitor**: \n
//         - **Additional Symptoms for Flukes**: Scratching against objects, flashing, excessive mucus production, respiratory distress.\n
//         - **Additional Symptoms for Ich**: White spots on the body and fins, flashing, clamped fins, loss of appetite.\n
//         - **Additional Symptoms for Columnaris**: Cotton-like growths on the skin, frayed fins, lethargy, loss of appetite.\n\n
//         **Treatment Recommendations**: \n
//         1. **Praziquantel Treatment**: Since Flukes are the most likely diagnosis, treating the fish with Praziquantel medication can help eliminate the parasites. Follow the instructions on the medication package for dosage and duration.\n
//         2. **Increase Water Temperature**: Raise the water temperature gradually to around 86-88°F (30-31°C) to help speed up the life cycle of the parasites and make them more susceptible to treatment.\n
//         3. **Perform Water Changes**: Regular water changes (around 25% every few days) can help improve water quality and reduce stress on the fish, aiding in its recovery.\n
//         It's important to closely monitor the fish for any changes in symptoms and behavior during treatment. If there is no improvement or if the condition worsens, consulting a veterinarian specializing in fish health is recommended.
//     `;
//     showModal(testContent);
// });