$(document).ready(function () {
    $('[chart-table]').each(function (i, table) {
        var values = [],
            $table = $(table),
            xAxis = 0,
            hideColumns = [],
            campos = [];

        $table.find('thead th').each(function (i, cell) {
            var value = $(cell).text().trim();

            if ($(cell).attr('chart-hide') !== undefined) {
                hideColumns.push(i);
                return true;
            }

            if (value) {
                values.push([value]);
                campos.push(value);
            }
        });

        $table.find('tbody tr').each(function (i, line) {
            var aux = 0;

            $(line).find('td').each(function (i, cell) {
                if (hideColumns.indexOf(i) != -1) {
                    aux += 1;
                    return true;
                }

                i -= aux;

                var $cell = $(cell),
                    value = $cell.attr('data-value');

                if (!value) value = $cell.text().trim();
                if (i != 0 && value == '-') value = null;

                if (value) {
                    values[i].push(value);
                } else {
                    values[i].push(null);
                }
            });
        });

        var $chart = $($table.attr('chart-table'));
        $chart.show();

        c3.generate({
            bindto: $chart.get(0),
            data: {
                x: values[xAxis][0],
                columns: values,
                xFormat: '%d/%m/%Y %H:%M'
            },
            point: {
                show: false
            },
            grid: {
                x: {
                    show: true
                },
                y: {
                    show: true
                }
            },
            axis: {
                x: {
                  type: 'timeseries',
                  tick: {
                      count: 32,
                      format: '%d/%m/%Y %H:%M'
                  }
                },
                y: {
                    tick: {
                        format: d3.format('.2f')
                    }
                }
            }
        });
    });
});
