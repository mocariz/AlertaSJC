$(document).ready(function () {
    $.tablesorter.addParser({
        id: 'brDateTime',
        is: function (s, table, cell, $cell) {

            if (!$cell.attr("data-date")) {
                return false;
            }

            return true;

        },
        format: function(s, table, cell, cellIndex) {
            var date = $(cell).attr("data-date");

            if (date === '-') return -1;
            return moment(date).valueOf() * -1;
        },
        type: 'numeric'
    });

    $.tablesorter.addParser({
        id: 'brNumber',
        is: function (s) {
            return /\d+,\d+/.test(s);
        },
        format: function (s) {
            var value = parseFloat(s.replace(',', '.'));

            return isNaN(value) ? -1 : value;
        },
        type: 'numeric'
    });

    $('table.table-sorter').each(function (i, table) {
        var $table = $(table),
            initialSortColumn = 0,
            initialSortOrder = 0;

        $table.find('thead th').each(function (i, th) {
            var initialSort = $(th).attr('initial-sort');

            if (initialSort) {
                initialSortColumn = i;
                initialSortOrder = initialSort === 'asc' ? 0 : 1;
            }
        });

        $table.tablesorter({
            sortList: [[initialSortColumn, initialSortOrder]]
        });
    });
});
