
var account_options = getAccountOptions();
var budget_options = getBudgetOptions();

function getAccountOptions() {
    var result = null;
    $.ajax({
        async: false,
        url: "api/accounts",
        type: "GET",
        dataType: "json",
        success: function (data) {
            result = data["data"];
        }
    });

    console.log(result);

    var i;
    var name = {}
    var id = {}
    for (i = 0; i < result.length; i++) {
        name[result[i]["id"]] = result[i]["name"];
        id[result[i]["id"]] = result[i]["id"];
    }
    var data = [name, id];
    return data;
}

function getBudgetOptions() {
    var result = null;
    $.ajax({
        async: false,
        url: "api/budgets",
        type: "GET",
        dataType: "json",
        success: function (data) {
            result = data["data"];
        }
    });

    console.log(result);

    var i;
    var name = {}
    var id = {}
    for (i = 0; i < result.length; i++) {
        name[result[i]["id"]] = result[i]["name"];
    }

    return name;
}

var minDate, maxDate;

// Custom filtering function which will search data in column four between two values
$.fn.dataTable.ext.search.push(
    function (settings, data, dataIndex) {
        var min = minDate.val();
        var max = maxDate.val();
        var date = new Date(data[4]);

        if (
            (min === null && max === null) ||
            (min === null && date <= max) ||
            (min <= date && max === null) ||
            (min <= date && date <= max)
        ) {
            return true;
        }
        return false;
    }
);

$(document).ready(function () {

    // Create date inputs
    minDate = new DateTime($('#min'), {
        format: 'MMMM Do YYYY'
    });
    maxDate = new DateTime($('#max'), {
        format: 'MMMM Do YYYY'
    });

    var columnDefs = [
        { "data": "id", "visible": false, "disabled": true },
        {
            "data": "date",
            "title": "Txn Date",
            "datetimepicker": { timepicker: false, format: "Y/m/d" }
        },
        {
            "data": "from_name",
            "type": "select",
            "select2": { width: "100%" },
            "options": account_options[0],
        },
        {
            "data": "to_name",
            "type": "select",
            "select2": { width: "100%" },
            "options": account_options[0],
        },
        {
            "data": "txn_tag",
            "type": "select",
            "select2": { width: "100%" },
            "options": budget_options,
        },
        { "data": "description" },
        { "data": "amount" }
    ];

    var get_txn_url = $('#api-transactions').data("url");
    let dt_txn = new base_dt("#dataTable", columnDefs);
    dt_txn.load_dataTable(get_txn_url);
    dt_txn.load_search();
});

