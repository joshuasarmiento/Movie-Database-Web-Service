$(document).ready(function() {

    var columnDefs = [
        {
            data: "id",
            title: "ID",
            type: "readonly"
        },
        {
            data: "name",
            title:  "Name"
        },
        {
            data: "price",
            title: "Price"
        },
        {
            data: "qty",
            title: "Qty"
        },
        {
            data: "exp",
            title: "Exp"
        },
    ];

    var remoteURL = 'http://127.0.0.1:5000/api';
    
    myTable = $('#crud').DataTable({
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
        altEditor: true,     // Enable altEditor
        buttons: [
        {
            text: 'Add',
            name: 'add'        // do not change name
        },
        {
            extend: 'selected', // Bind to Selected row
            text: 'Edit',
            name: 'edit'        // do not change name
        },
        {
            extend: 'selected', // Bind to Selected row
            text: 'Delete',
            name: 'delete'      // do not change name
        },
        {
            text: 'Refresh',
            name: 'refresh'      // do not change name
        }
        ],
        onAddRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: remoteURL,
                type: 'POST',
                data: JSON.stringify(rowdata),
                dataType: 'json',
                success: success,
                error: error
            });
        },
        onDeleteRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: remoteURL + "/" + rowdata.id,
                type: 'DELETE',
                data: rowdata,
                success: success,
                error: error
            });
        },
        onEditRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: remoteURL + "/" + rowdata.id,
                type: 'PUT',
                dataType: 'json',
                data: JSON.stringify(rowdata),
                success: success,
                error: error
            });
        }
    });
});