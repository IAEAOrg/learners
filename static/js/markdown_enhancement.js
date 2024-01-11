$(function () {

    // ################################################
    // Autofit Fontsize in Table
    // ################################################
    
    let tables = $("table")
    
    $(tables).hide() // hide tables to allow resizing table by table
    $(tables).each(function (index, table_object) {
        $(table_object).show() // insert respective table
        let max_width = $("#body-inner").width()
        let fontSize = 100;
        while ($(table_object).width() > max_width && fontSize > 0) {
            fontSize -= 5;
            $(table_object).css("font-size", fontSize + '%')
        }
    });

    // ################################################
    // Table Cell Colors
    // ################################################

    let cell_objects = $(".cell-color")
    
    $(cell_objects).each(function (index, cell_object) {
        let color = $(cell_object).attr("color")
        let textcolor = $(cell_object).attr("textcolor")
        let cell = $(cell_object).parent()[0]

        $(cell).css("background-color", color)
        $(cell).css("color", textcolor)
    });


    // ################################################
    // Table Row Colors
    // ################################################

    let row_objects = $(".row-color")
    
    $(row_objects).each(function (index, row_object) {
        let color = $(row_object).attr("color")
        let textcolor = $(row_object).attr("textcolor")
        let row = $(row_object).closest("tr")[0]

        $(row).css("background-color", color)
        $(row).css("color", textcolor)
    });


    // ################################################
    // Table Column Colors
    // ################################################

    let col_objects = $(".col-color")
    
    $(col_objects).each(function (index, col_object) {
        let color = $(col_object).attr("color")
        let textcolor = $(col_object).attr("textcolor")
        let colindex = $(col_object).parent().index();

        let cells = []
        $(col_object).closest('table').find('tr').each(function(){
            cells.push($(this).children('td').eq(colindex)[0]);
        });

        $(cells).each(function (index, cell_object) {
            if (!$(cell_object).find(".cell-color")[0]) {
                $(cell_object).css("background-color", color)
                $(cell_object).css("color", textcolor)
            }
        });
    });
    
    // ################################################
    // Table Cell Span
    // ################################################

    let cellspan_cell_objects = $(".cell-span")
    
    $(cellspan_cell_objects).each(function (index, cell_object) {

        // get td
        let cell = $(cell_object).parent()[0]

        // apply colspan
        let cols = parseInt($(cell_object).attr("cols"))
        $(cell).attr("colspan", cols)
        let colindex = $(cell_object).parent().index();
        
        // apply rowspan
        let rows = parseInt($(cell_object).attr("rows"))
        $(cell).attr("rowspan", rows)
        let rowindex = $(cell_object).closest("tr").index();

        let colcount = $($(cell_object).closest("table tr")[0]).find("td").length - 1

        let cols_to_remove = []
        let rows_to_remove = []

        let table_object = $(cell_object).closest("table")
        $(table_object).find("tr").each(function(index, tr) {
            if (index > rowindex && index <= (rowindex + rows)) {
                rows_to_remove.push(tr)
            }
        });

        $(rows_to_remove).each(function(index, row) {
            if (index > 0) {
                for (let i = 0; i < cols; i++) {
                    let col_to_remove = $(row).children('td').eq(colcount - i)[0];
                    cols_to_remove.push (col_to_remove)
                } 
            } else if (cols > 1) {
                let col_to_remove = $(row).children('td').eq(colcount)[0];
                cols_to_remove.push (col_to_remove)
            }
        });

        $(cols_to_remove).each(function (index, cell_object) {
            $(cell_object).remove();
        });

    });

    // ################################################
    // Layout Table
    // ################################################

    let layout_table_objects = $(".layout-table-marker").closest("table")

    $(layout_table_objects).each(function (index, table_object) {
        $(table_object).addClass("layout-table")
    });
    
    $(".layout-table-marker").each(function (index, marker) {
        let table_object = $(marker).closest("table")
        
        // Format input string
        let formated_padding = $(marker).attr("padding").split(" ").map(padding_element => {
            if (padding_element.includes("px")) return padding_element
            return (`${padding_element}px`)            
        }).join(" ");
        
        let ratio = $(marker).attr("ratio").split(" ").map(ratio_element => {
            if (ratio_element.includes("%")) return ratio_element
            return (`${ratio_element}%`)            
        })
        
        if ($(marker).attr("divider") == "true") $(table_object).addClass("divider")
        if ($(marker).attr("striped") == "true") $(table_object).addClass("striped")

        // Apply CSS
        $(table_object).find("tr td").each(function (index, td_object) {
            $(td_object).css("padding", formated_padding);
            if (!$(table_object).hasClass("autowidth")) {
                $(td_object).css("width", ratio[index % ratio.length]);
            }
        });
    });

    // ################################################
    // No Table Headers
    // ################################################

    let no_header_table_objects = $(".no-table-header").closest("table")
    
    $(no_header_table_objects).each(function (index, table_object) {
        $(table_object).addClass("no-table-header")
    });

});