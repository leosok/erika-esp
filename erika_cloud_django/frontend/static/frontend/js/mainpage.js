document.addEventListener("DOMContentLoaded", function(event) {
    setTimeout(reload_online_typewriters, 1000)
    setInterval(reload_online_typewriters, 5000)
    
    // Add click pattern detection
    const logo = document.querySelector('.logo_contrainer img');
    let clicks = 0;
    let lastClick = 0;
    
    logo.addEventListener('click', (e) => {
        const now = Date.now();
        if (now - lastClick > 1000) { // Reset if more than 1 second between clicks
            clicks = 0;
        }
        lastClick = now;
        clicks++;
        
        if (clicks === 3) { // After 3 quick clicks
            document.getElementById('print_all_button').style.display = 'inline-block';
            clicks = 0;
        }
    });
});

function send_text_to_printer() {
            text = document.getElementById("erika_text").value.trim();

            var select = document.getElementById('typewriters_online');
            var uuid = select.options[select.selectedIndex].value;

            // Sending and receiving data in JSON format using POST method
            if (uuid != 0) {
                var xhr = new XMLHttpRequest();
                var url = "/api/typewriter/" + uuid + "/print";

                console.log("printig to " + url)

                xhr.open("POST", url, true);
                xhr.setRequestHeader("Content-Type", "application/json");
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        //console.log("Success: " + xhr.responseText);
                    }
                };
                var data = JSON.stringify({"body": text});
                xhr.send(data);
            }
        }

function send_text_to_all_printers() {
    const text = document.getElementById("erika_text").value.trim();
    const url = "/api/typewriter/print/all";

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "body": text })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Printed to all typewriters:", data);
    })
    .catch(error => {
        console.error('Error printing to all typewriters:', error);
    });
}

function reload_online_typewriters() {
    fetch('/api/typewriter/online')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const select_field = document.getElementById("typewriters_online");
            const countBefore = select_field.options.length;
            const previousValue = select_field.value; // Store the currently selected value

            // Clear existing options
            select_field.innerHTML = '';

            if (data.length > 0) {
                data.forEach(typewriter => {
                    const option = document.createElement('option');
                    option.value = typewriter.uuid;
                    // Only show firstname in parentheses if it exists
                    option.textContent = typewriter.user_firstname ? 
                        `${typewriter.erika_name} (${typewriter.user_firstname})` : 
                        typewriter.erika_name;
                    select_field.appendChild(option);
                });
                select_field.disabled = false;
                
                // Restore the previously selected value if it still exists
                if (previousValue && Array.from(select_field.options).some(opt => opt.value === previousValue)) {
                    select_field.value = previousValue;
                }
            } else {
                const option = document.createElement('option');
                option.value = "0";
                option.textContent = "Keine Erikas online";
                select_field.appendChild(option);
                select_field.disabled = true;
            }

            const countAfter = select_field.options.length;
            if (countBefore !== countAfter) {
                console.log(`Online typewriters updated ${countBefore} -> ${countAfter}`);
            } else {
                console.log("Typewriter count did not change");
            }
        })
        .catch(error => {
            console.error('Error fetching typewriters:', error);
            const select_field = document.getElementById("typewriters_online");
            select_field.innerHTML = '<option value="0">Error loading typewriters</option>';
            select_field.disabled = true;
        });
}