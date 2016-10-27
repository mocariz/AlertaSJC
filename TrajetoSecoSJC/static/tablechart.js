$(document).ready(function () {

    function createCookie(name, value) {
        document.cookie = name + "=" + value + "; path=/";
    }

    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
        }
        return "";
    }

    function mostrar(chart, id){
        if (getCookie(id) == ''){
            createCookie(id, 'true');
        }
        else if (getCookie(id) == 'false'){
            chart.hide(id);
        } else {
            chart.show(id);
        }
    }

    $('[chart-table]').each(function (i, table) {
        var values = [],
            $table = $(table),
            chartType = $table.attr('chart-type'),
            xAxis = parseInt($table.attr('chart-x-axis')),
            hideColumns = [],
            campos = [];

        if (!xAxis) xAxis = 0;

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

        var $chart = $($table.attr('chart-table')),
            xAxisType = $table.attr('chart-x-axis-type'),
            timeFormat = $table.attr('chart-timeseries-format');

        $chart.show();

        if (!xAxisType) xAxisType = 'timeseries';
        if (!timeFormat) timeFormat = '%d/%m/%Y %H:%M';

        var data = {
            x: values[xAxis][0],
            columns: values,
            type: chartType
        };

        var xAxisConfig = {};

        xAxisConfig.type = xAxisType;

        if (xAxisType == 'timeseries') {
            data.xFormat = timeFormat;
            xAxisConfig.tick = {
                count: 32,
                format: timeFormat
            };
        }

        if (xAxisType == 'category') {
            xAxisConfig.height = 90;
            xAxisConfig.tick = {
                rotate: -35,
                fit: true,
                multiline: false
            }
        }

        var chart = c3.generate({
            bindto: $chart.get(0),
            data: data,
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
                x: xAxisConfig,
                y: {
                    tick: {
                        format: d3.format('.2f')
                    }
                }
            },
            legend: {
                item: {
                    onclick: function (id) {
                        if (getCookie(id) == 'true'){
                            createCookie(id, 'false');
                            chart.hide(id);
                        } else {
                            createCookie(id, 'true');
                            chart.show(id);
                        }
                    }
                }
            }
        });

        for (i in campos) {
            mostrar(chart, campos[i]);
        }
    });
});
