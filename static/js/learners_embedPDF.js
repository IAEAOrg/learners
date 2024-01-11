function renderPDF(container_id, file) {
  let pdfDoc = null;
  let numPages = 0;
  
  pdfjsLib.getDocument(file).promise.then((pdfDoc_) => {
    pdfDoc = pdfDoc_;
    numPages = Boolean($(`#${container_id}`).attr("show_all_pages"))
    ? pdfDoc.numPages
    : 1;
    $(`#${container_id}`).attr("num_pages", numPages);
    
    pdfDoc.getPage(1).then((page) => {
      const viewport = page.getViewport({ scale: 1.5 });
      $(`#${container_id}`).attr("ratio_height", viewport.height);
      $(`#${container_id}`).attr("ratio_width", viewport.width);
      resizePDF(container_id);
    });
  });
}

function resizePDF(container_id) {
  numPages = parseInt($(`#${container_id}`).attr("num_pages"));
  if (numPages) {
    ratio_height = $(`#${container_id}`).attr("ratio_height");
    ratio_width = $(`#${container_id}`).attr("ratio_width");
    
    const currWidth = $(`#${container_id}`).width();
    let ratio = Math.floor(((ratio_height * numPages) / ratio_width) * 10) / 10;
    $(`#${container_id}`).css({
      height: currWidth * ratio + "px",
    });
  } else {
    // Fallback
    inner_body_width = $("#body-inner").width();
    $(`#${container_id}`).css({
      height: inner_body_width * 1.2 + "px",
    });

  }

}
