function init_comment_forms() {
  $(".comment-form").submit(function (event) {

    // Get data
    const comment = $(this).find("textarea").val()
    const info = $(this).find("input[name=info]").val();
    const page = JSON.parse(info).page
    const data = JSON.stringify({
      "page": page,
      "comment": comment,
    })

    // Get feedback container
    const responseContainer = $(this).find(".response");

    // Send comment to backend
    sendAjax("POST", { url: `/comments`, data: data })
      .then(function (data, textStatus, jqXHR) {
        responseContainer.html("Thank you for your feedback.").addClass("success");
      })
      .catch(function (jqXHR, textStatus, errorThrown) {
        responseContainer.html("Something went wrong.").addClass("error");
      });

    // Prevent default    
    event.preventDefault();
    event.stopImmediatePropagation();
  });
}

function when_time_passed(date) {
  return new Promise((resolve) => {
    let timer = setInterval(function () {
      if (date < new Date().toLocaleString()) {
        clearInterval(timer);
        resolve(true);
      }
    }, 60 * 1000 * 5); // check every 5 min
  });
}