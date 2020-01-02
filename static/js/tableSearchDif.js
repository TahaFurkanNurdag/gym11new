function myFunction2() {
    // Declare variables
    var input2, filter2, table2, tr2, td2, i2, txtValue2;
    input2 = document.getElementById("myInput2");
    filter2 = input2.value.toUpperCase();
    table2 = document.getElementById("myTable2");
    tr2 = table2.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i2 = 0; i2 < tr2.length; i2++) {
        td2 = tr2[i2].getElementsByTagName("td")[1];
        if (td2) {
            txtValue2 = td2.textContent || td2.innerText;
            if (txtValue2.toUpperCase().indexOf(filter2) > -1) {
                tr2[i2].style.display = "";
                // i nin değerini alıp values arrayine atacak
            } else {
                tr2[i2].style.display = "none";
            }
        }
    }
}