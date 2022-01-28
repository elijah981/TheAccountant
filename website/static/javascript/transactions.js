
$(document).ready(function () {

    var columnDefs = [
        { "data": "id", "visible": false, "disabled": true },
        { "data": "date" },
        { "data": "from_name" },
        { "data": "to_name" },
        { "data": "txn_tag" },
        { "data": "description" },
        { "data": "amount" },
        // { "data": "project_id", "visible": false, "disabled": true },
        // {
        //     "data": "model_id",
        //     "type": "select",
        //     "select2": { width: "100%" },
        //     "options": model_options,
        // },
        // {
        //     "data": "car_id",
        //     "type": "select",
        //     "select2": { width: "100%" },
        //     "options": car_options,
        // },
        // { "data": "alias" },
        // { "data": "lv_device" }
    ];

    var get_txn_url = $('#api-transactions').data("url");
    let dt_txn = new base_dt("#dataTable", columnDefs);
    dt_txn.load_dataTable(get_txn_url);
    dt_txn.load_search();
});

