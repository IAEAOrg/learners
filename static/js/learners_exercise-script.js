function scriptExercise(exercise) {

  getExecutionHistory(exercise);

  $(`#${exercise.global_exercise_id} .btn-run-exercise`).click(function () {
    executeScript(exercise)
  });
};

function checkScriptExecution(button_id, script) {
  const button = $(`#${button_id}`)
  const stat_indicator = $(button).parent().find(".stat_indicator")[0]
  const stat_message = $(button).parent().find(".stat_message")[0]

  // deactivate button and show loading
  $(button).prop('disabled', true)
  displayLoading(stat_indicator, stat_message)

  const url = `/executions/active/${script}`
  waitForExecutionResponse(url, stat_indicator, stat_message, button)
  
}

function executeScript(button, script) {
  const stat_indicator = $(button).parent().find(".stat_indicator")[0]
  const stat_message = $(button).parent().find(".stat_message")[0]

  // deactivate button and show loading
  $(button).prop('disabled', true)
  displayLoading(stat_indicator, stat_message)

  sendAjax("POST", { url: `/executions/${script}` })
    .then(function (data, textStatus, jqXHR) {
      const url = `/executions/${data.uuid}`
      waitForExecutionResponse(url, stat_indicator, stat_message, button)
    })
    .catch(function (xhr, status, error) {
      displayError(stat_indicator, stat_message, "Failed to execute.")
    })
}

// helper functions
function waitForExecutionResponse(url, stat_indicator, stat_message, button) {
  const defer = $.Deferred();
  sendAjax("GET", { url: url })
  .then(function (data, textStatus, jqXHR) {
    if (data) {
      if (data.connection_failed) {
        displayError(stat_indicator, stat_message, data.msg || "Connection failed.")
      } else if (!data.executed) {
        displayError(stat_indicator, stat_message, data.msg || "Execution failed.")
      } else if (data.partial) {
        displayPartialSuccess(stat_indicator, stat_message, data.msg || "")
      } else {
        displaySuccess(stat_indicator, stat_message, data.msg || "Executed.")
      }
    } else {
      hideLoading(stat_indicator, stat_message)
    }
    defer.resolve(data);
  })
  .catch(function (jqXHR, textStatus, errorThrown) {
    console.error(jqXHR, textStatus, errorThrown)
    setTimeout(function() {
      displayError(stat_indicator, stat_message, "Failed to execute.")
    }, 500);
    defer.reject(jqXHR, textStatus, errorThrown);
  })
  .finally(() => {
    $(button).prop('disabled', false)
  });
}

const displayLoading = (stat_indicator, stat_message) => {
  $(stat_indicator)
    .stop(true, true)
    .removeClass("failed success none partial")
    .addClass("loading")
    .show();
    $(stat_message).removeClass().addClass("stat_message")
    $(stat_message).html("Running ...")
}
const hideLoading = (stat_indicator, stat_message) => {
  $(stat_indicator)
    .stop(true, true)
    .removeClass("failed success none partial loading")
    .show();
    $(stat_message).removeClass().addClass("stat_message")
    $(stat_message).html("")
}
const displaySuccess = (stat_indicator, stat_message, msg) => {
  $(stat_indicator)
  .stop(true, true)
  .delay(200)
  .queue(function (next) {
    $(this)
      .removeClass("loading failed none partial")
      .addClass("success")
      .show();
    next();
  });
  $(stat_message).removeClass().addClass("stat_message success")
  $(stat_message).html(msg)
}
const displayError = (stat_indicator, stat_message, error_msg) => {
  $(stat_indicator)
  .stop(true, true)
  .delay(200)
  .queue(function (next) {
    $(this)
      .removeClass("loading success none partial")
      .addClass("failed")
      .show();
    next();
  });
  $(stat_message).removeClass().addClass("stat_message error")
  $(stat_message).html(`Error: ${error_msg}`)
}
const displayPartialSuccess = (stat_indicator, stat_message, msg) => {
  $(stat_indicator)
  .stop(true, true)
  .delay(200)
  .queue(function (next) {
    $(this)
      .removeClass("loading success none failed")
      .addClass("partial")
      .show();
    next();
  });
  $(stat_message).removeClass().addClass("stat_message partial")
  $(stat_message).html(`Partial success: ${msg}`)
}
