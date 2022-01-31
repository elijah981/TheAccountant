class base_dt {
    constructor(name, columnDefs) {
        this.name = name;
        this.columnDefs = columnDefs;
    }

    load_search() {
        // Setup - add a text input to each footer cell
        $(this.name + ' tfoot th').each(function () {
            var title = $(this).text();
            $(this).html('<input type="text" placeholder="Search ' + title + '" />');
        });
    }

    load_dataTable(dt_url) {

        $(this.name).DataTable({
            "sPaginationType": "full_numbers",
            "ajax": dt_url,
            columns: this.columnDefs,
            dom: 'Bfrtip',        // Needs button container
            select: 'single',
            responsive: true,
            altEditor: true,     // Enable altEditor
            encodeFiles: true,
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
            onAddRow: function (datatable, rowdata, success, error) {
                console.log("On Add Row editor");
                console.log(dt_url);
                $.ajax({
                    // a tipycal url would be / with type='POST'
                    url: "api/accounts",
                    type: "POST",
                    data: JSON.stringify(rowdata),
                    success: success,
                    error: error
                });
            },
            onDeleteRow: function (datatable, rowdata, success, error) {
                $.ajax({
                    // a tipycal url would be /{id} with type='DELETE'
                    url: dt_url + "/" + rowdata['id'],
                    type: 'DELETE',
                    data: JSON.stringify(rowdata),
                    success: success,
                    error: error
                });
            },
            onEditRow: function (datatable, rowdata, success, error) {
                $.ajax({
                    // a tipycal url would be /{id} with type='PUT'
                    url: dt_url + "/" + rowdata['id'],
                    type: 'PUT',
                    data: JSON.stringify(rowdata),
                    success: success,
                    error: error
                });
            },
            initComplete: function () {
                // Apply the search
                this.api().columns().every(function () {
                    var that = this;

                    $('input', this.footer()).on('keyup change clear', function () {
                        if (that.search() !== this.value) {
                            that
                                .search(this.value)
                                .draw();
                        }
                    });
                });
            },
        });
    }
}
