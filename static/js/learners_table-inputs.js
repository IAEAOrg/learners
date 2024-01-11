function isEmpty(td) {
  if ($(td).prop("contenteditable") !== "true") return true;
  if (
    td.text == "" ||
    td.text() == " " ||
    td.text() == "\n" ||
    $(td).html() == "<br>" ||
    td.html() == "&nbsp;" ||
    td.html() == undefined ||
    td.is(":empty") ||
    td.is(":not(:visible)")
  ) return true;
  return false;
}

function initTableDetection(td) {
  $(td).focusout(() => {
    detectFullTable($(event.target).closest("table"));
  });
}

function detectFullTable(table_obj) {
  const tds = $(table_obj).find("tr:last td");
  const trs = $(table_obj).find("tr").not("tr:last").not("tr:first");
  let tableBody = $(table_obj).find("tbody").first();

  let empty_row = true;
  let last_row = $(table_obj).find("tr:last")[0];
  let new_row_template = $(last_row).clone();
  $(new_row_template).find("td[contenteditable]").text("");

  $.each(tds, (i, cell) => {
    if (isEmpty($(cell)) === false) empty_row = false;
  });

  // Append new empty row
  if (!empty_row) {
    $(tableBody).append(new_row_template);
    $(tableBody)
      .find("tr:last td")
      .css("height", "0px")
      .wrapInner('<div style="display: none; height: 22px" />')
      .parent()
      .find("td > div")
      .slideDown(700, function () {
        const td_obj = $(this).parent()[0]
        var $set = $(this);
        $set.replaceWith($set.contents());
        $(td_obj).css("height", "40px")
      })
    $(tableBody).slideDown();
    initTableDetection($(tableBody).find("tr:last"));
  }

  // Remove empty rows
  $.each(trs, (i, row) => {
    let trIsEmpty = true;
    let allNonEditable = true;

    $.each($(row).find("td"), (i, cell) => {
      if (isEmpty($(cell)) === false) {
        trIsEmpty = false;
      }
      if ($(cell).prop("contenteditable") == "true") {
        allNonEditable = false;
      }
    });
    if (trIsEmpty && !allNonEditable) {
      $(row)
        .children("td")
        .css("height", "0px")
        .animate({ "padding-top": 0, "padding-bottom": 0 })
        .wrapInner('<div style="height: 22px" />')
        .children()
        .slideUp(function () {
          $(this).closest("tr").remove();
        });
    }
  });
}

$(function () {
  $(".input-table.autoextend tr td[contenteditable]").each(function (index, cell_object) {
    initTableDetection($(cell_object));
  });
});
