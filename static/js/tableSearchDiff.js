function myFunction3() {
    // Declare variables
    var input3, filter3, table3, tr3, td3, i3, txtValue3;
    input3 = document.getElementById("myInput3");
    filter3 = input3.value.toUpperCase();
    table3 = document.getElementById("myTable3");
    tr3 = table3.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i3 = 0; i3 < tr3.length; i3++) {
        td3 = tr3[i3].getElementsByTagName("td")[1];
        if (td3) {
            txtValue3 = td3.textContent || td3.innerText;
            if (txtValue3.toUpperCase().indexOf(filter3) > -1) {
                tr3[i3].style.display = "";
                // i nin değerini alıp values arrayine atacak
            } else {
                tr3[i3].style.display = "none";
            }
        }
    }
}