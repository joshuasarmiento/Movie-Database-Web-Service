$(document).ready(function() {

    var columnDefs = [{ data: "id", title: "ID", type: "readonly"},
                      { data: "name", title:  "Name" },
                      { data: "price", title: "Price" },
                      { data: "qty", title: "Qty" }, 
                      { data: "exp", title: "Exp" },];
    var remoteURL = 'http://127.0.0.1:5000/api'; 
    myTable = $('#productsbd').DataTable({
        "sPaginationType": "full_numbers",
        ajax: {
            url : remoteURL,
            contentType: 'application/json',
            dataSrc : 'data',
        },
        columns: columnDefs,
        dom: 'Bfrtip',        // Needs button container
        select: 'single',
        responsive: true,
        altEditor: false,     // Enable altEditor
        buttons: [],
    });
});