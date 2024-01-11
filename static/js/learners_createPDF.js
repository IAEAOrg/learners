window.jsPDF = window.jspdf.jsPDF

async function downloadPDF(btn) {
    $(btn).addClass("active")
    $(".pdf-loading-indicator").show()
    generatePDF().then(()=> {
      $(".pdf-loading-indicator").hide()
      $(btn).removeClass("active")
    })
}

function generatePDF() {
    return new Promise(resolve => {
        var pdf = new jsPDF("portrait", "px", "a4", true);
        let $source = $("#body-inner").clone();

        var selects = $("#body-inner").find("select");
        $(selects).each(function(i) {
            var select = this;
            $source.find("select").eq(i).val($(select).val());
        });

        var pdf_spacer = document.createElement("div");
        pdf_spacer.id = "pdf-viewpoint-spacer";
        $("#body-inner").append(pdf_spacer);

        var pdf_container = document.createElement("div");
        pdf_container.id = "pdfcontainer";
        $("#body-inner").append(pdf_container);
        
        $("#pdfcontainer").append($source);
        cleanHTML($("#pdfcontainer"));

        source = $("#pdfcontainer")[0];

        // let test = $("#body-inner")[0]

        pdf.html(source, {
          callback: function (doc) {
            doc.setFontSize(7);
            doc.setTextColor("#9a9a9a");
            doc.setFont("helvetica");

            var pageTitle = $(source).find("h1:first").text().trim();

            const pageCount = doc.internal.getNumberOfPages();
            for (let i = 1; i <= pageCount; i++) {
                doc.setPage(i);
                const pageSize = doc.internal.pageSize;
                const pageWidth = pageSize.width ? pageSize.width : pageSize.getWidth();
                const pageHeight = pageSize.height
                ? pageSize.height
                : pageSize.getHeight();
                const header = "Report: " + pageTitle;
                const footer = `Page ${i} of ${pageCount}`;

                // Header
                doc.text(header, 40, 20, { baseline: "top" });

                // Footer
                doc.text(footer, 40, pageHeight - 20, { baseline: "bottom" });
            }
            resolve('resolved');
            doc.save("Report_" + pageTitle + ".pdf");
            $("#pdfcontainer").remove();
            $("#pdf-viewpoint-spacer").remove();
        },
        x: 0,
        y: 0,
        margin: 40,
        autoPaging: "text",
        filename: "test.pdf",
        html2canvas: {
          scale: 0.5
        },
        // image: {},
        // jsPDF: {},
        // width: 460
      })
    });
}

function cleanHTML(source) {
  const exception_list = "table, thead, tbody, tr, td, th"
  $.each($(source).find("*"), function () {
    let element = $(this)[0];
    let tagName = $(element).prop("tagName");
    var k = parseInt($(tagName).css("font-size"));
    // var redSize = (k * 80) / 100;
    // $(element).not(exception_list).css({ "font-size": redSize });
    // $(element).not(exception_list).css({ padding: 0 });
    $(element).addClass("pdf");
  });

  // Adjust Image Sizes
  $.each($(source).find(".input-row"), function () {
    $(this).addClass("wide");
  });

  // Adjust Image Sizes
  $.each($(source).find("img"), function () {
    adjustImgSize(this);
  });

  // Replace hyperlinks
  $.each($(source).find("a"), function () {
    // $(this).replaceWith("<b>" + this.innerHTML + "</b>");
    $(this).replaceWith(this.innerHTML);
  });

  $.each($(source).find("em"), function () {
    $(this).replaceWith(this.innerHTML);
  });
  $.each($(source).find("b"), function () {
    $(this).replaceWith(this.innerHTML);
  });
  $.each($(source).find("strong"), function () {
    $(this).replaceWith(this.innerHTML);
  });
  $.each($(source).find("font"), function () {
    $(this).replaceWith(this.innerHTML);
    // TODO: Keep color
  });

  // Replace labels
  $.each($(source).find("label"), function () {
    // $(this).replaceWith("<b>" + this.innerHTML + "</b>");
    $(this).replaceWith(this.innerHTML);
  });

  // Replace input fields with value
  $.each($(source).find("input[type=text]"), function () {
    let value = $(this).val();
    replaceInputField(value, $(this));
  });

  // Replace input selects with value
  $.each($(source).find("select"), function () {
    let value = $(this).find("option:selected").text();
    replaceInputField(value, $(this));
  });

  // Replace input textarea with value
  $.each($(source).find("textarea"), function () {
    let value = $(this).val();
    replaceInputField(value, $(this));
  });

  // Remove unnecessary elements
  let objects_to_remove = [
    "div.exercise-control",
    ".add-input-row",
    "button",
    "aside",
    ".copy-to-clipboard",
    "#comment-section"
  ];
  $.each(objects_to_remove, function (i) {
    $(source).find(objects_to_remove[i]).remove();
  });

  // Replace special chars
  let map = { "’": "'" };
  $(source).html(
    $(source)
      .html()
      .replace(/’/g, function (m) {
        return map[m];
      })
  );
}

function replaceInputField(value, element) {
  element.replaceWith(
    "<table class='answer pdf'><tr><th>Answer:</th></tr><tr><td>" + value + "</td></tr></table>"
  );
}

function toDataURL(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.onload = function () {
    var reader = new FileReader();
    reader.onloadend = function () {
      callback(reader.result);
    };
    reader.readAsDataURL(xhr.response);
  };
  xhr.open("GET", url);
  xhr.responseType = "blob";
  xhr.send();
}

function adjustImgSize(img) {
  
  const width_constraints = [
    parseInt($(img).width()),
    parseInt(img.style.maxWidth)
  ]
  
  let max_value = 540;

  const max_width = Math.min.apply(Math, width_constraints.filter(Boolean))
  if (max_width) {
    const body_width = $("#body-inner").width()
    const ratio = body_width / max_width
    max_value = max_value / ratio
  }
  
  let orignial_width = $(img).prop("naturalWidth");
  let orignial_height = $(img).prop("naturalHeight");

  if (orignial_width > max_value) {
    $(img).width(max_value);
    if ($(img).height() > max_value) {
      $(img).width("");
      $(img).height(max_value);
    }
  } else if (orignial_height > max_value) {
    $(img).height(max_value);
  }
}
