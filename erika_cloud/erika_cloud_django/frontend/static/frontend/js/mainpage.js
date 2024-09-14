

document.addEventListener("DOMContentLoaded", function(event) {
    setTimeout(reload_online_typewriters, 1000)
    setInterval(reload_online_typewriters, 5000)
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
//
// function reload_online_typewriters(){
//     var xhr = new XMLHttpRequest();
//         var url = "/api/typewriter/online";
//
//         xhr.open("GET", url, true);
//         xhr.onreadystatechange = function () {
//             if (xhr.readyState === 4 && xhr.status === 200) {
//                 // Replace content of select:
//                 var select_field = document.getElementById("typewriters_online")
//                 if ( xhr.responseText.trim().replace(/"/g, "") !=
//                     select_field.outerHTML.trim().replace(/"/g, "") ) {
//                     select_field.outerHTML = xhr.responseText
//                     count_before_update = select_field.outerHTML.match(/<option/g).length
//                     count_after_update = xhr.responseText.match(/<option/g).length
//                     console.log("Online typewriters updated " + count_before_update + "->" + count_after_update)
//                     // console.log(xhr.responseText.trim().replace(/"/g, ""))
//                     // console.log(select_field.outerHTML.trim().replace(/"/g, ""))
//                 } else {
//                     console.log("Typewriter count did not change")
//                 }
//             }
//         };
//         xhr.send(null);
//     }


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

            // Clear existing options
            select_field.innerHTML = '';

            if (data.length > 0) {
                data.forEach(typewriter => {
                    const option = document.createElement('option');
                    option.value = typewriter.uuid;
                    option.textContent = `${typewriter.erika_name} (${typewriter.user_firstname})`;
                    select_field.appendChild(option);
                });
                select_field.disabled = false;
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