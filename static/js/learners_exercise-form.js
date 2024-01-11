const validationOptions = {
  ignore: [],
  rules: getValidationRules(),
};

function formExercise(exercise) {
  const exerciseForm = $(`#${exercise.global_exercise_id}`);

  // Initital validation
  exerciseForm.validate(validationOptions);

  // Submit Handler
  exerciseForm.submit(async (event) => {
    event.preventDefault();

    // Upload Handler
    let sucessfulUploadHandler = await uploadHandler(exerciseForm);
    persistForm(exercise.global_exercise_id);

    // Validate Form
    let status = exerciseForm.validate(validationOptions);
    let validForm = !Object.keys(status.invalid).length;

    if (validForm && sucessfulUploadHandler) {
      await submitForm(this, exercise);
      getExecutionHistory(exercise);
    }
  });

  $("#upload_form").submit(function (event) {
    const status = $(this).validate(validationOptions);
    const validForm = !Object.keys(status.invalid).length;

    if (validForm) {
      uploadHandler(exerciseForm);
    }
    event.preventDefault();
    event.stopImmediatePropagation();
  });

  loadForm(exercise);
  initForm(exercise);

  getExecutionHistory(exercise);
}

// ------------------------------------------------------------------------------------------------------------

async function uploadHandler(exerciseForm) {
  var defer = $.Deferred();

  // Determine if fileupload exists in exercise
  const uploadContainerList = exerciseForm.find("#upload-container");

  // If no upload present return
  if (!uploadContainerList.length) defer.resolve(true);

  // Set variables
  let uploadContainer = uploadContainerList[0];
  let fileInput = $($(uploadContainer).find("#file")[0]).val();

  // User feedback
  const msgContainer = $(uploadContainer).find("#msg-detail")[0];

  if (fileInput) {
    await uploadFile(uploadContainer)
      .then((data) => {
        // Add classes
        $(msgContainer).removeClass("error success");
        if (!data.executed) {
          $(msgContainer).addClass("error");
          $(msgContainer).html(data.msg || "File upload failed.");
          $(msgContainer).slideDown();
        } else if (data.executed) {
          $(msgContainer).addClass("success");
          $(msgContainer).html(data.msg || "File uploaded.");
          $(msgContainer).slideDown();
        } else {
          $(msgContainer).removeClass();
          $(msgContainer).html("");
          $(msgContainer).hide();
        }

        defer.resolve(true);
      })
      .catch((error) => {
        $(msgContainer).addClass("error");
        $(msgContainer).html(error);
        $(msgContainer).slideDown();
      });
  }

  let uploadedFilename = $($(uploadContainer).find("#attachment")[0]).val();
  if (uploadedFilename) defer.resolve(true);

  if (!$($(uploadContainer).find("#attachment")[0]).hasClass("required"))
    defer.resolve(true);

  return defer.promise();
}

async function uploadFile(upload_container) {
  const defer = $.Deferred();
  const file_data = $(upload_container).find("#file").prop("files")[0];

  if (!file_data) {
    // Handle the case where no file is selected
    defer.reject("No file selected");
    return defer.promise();
  }

  const form_data = new FormData();
  form_data.append("file", file_data);

  try {
    const response = await $.ajax({
      url: `${apiUrl}/uploads`,
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      type: "post",
      headers: { Authorization: `Bearer ${getCookie("jwt_cookie")}` },
      timeout: 10000,
    });

    if (response) {
      // Set attachment value to hidden field
      const hiddenField = $(upload_container).find("#attachment")[0];
      $(hiddenField).attr("value", response.filename);
      defer.resolve(true);
    } else {
      // Handle the case where the server did not return the expected data
      defer.reject("Unexpected response from the server");
    }
  } catch (error) {
    if (error.statusText === "timeout") {
      // Handle timeout error
      defer.reject("Request timed out");
    } else {
      // Handle other errors
      defer.reject("Upload failed");
    }
  }

  return defer.promise();
}

function appendNewInputRow(fieldset_id, amount = 1) {
  const base = $(`#${fieldset_id} .default-inputs`);
  const container = $(`#${fieldset_id} #extendedInputs`);
  let current_count = $(container).find(".input-group").length;

  for (let i = 0; i < amount; i++) {
    let new_index = current_count + i + 1;
    let new_input_block = base
      .clone()
      .removeClass("default-inputs")
      .css("display", "none");

    // Update input names and labels
    $.each($(new_input_block).find(".input"), (index, input_object) => {
      let current_input_name = $(input_object).attr("name");
      let new_input_name = `${current_input_name} (${new_index})`;

      $(new_input_block)
        .find(`label[for="${current_input_name}"]`)
        .attr("for", new_input_name);

      $(input_object).attr("name", new_input_name);
      $(input_object).val("");
    });

    $(new_input_block).find(".divider").first().val("--divider--");
    $(new_input_block).find(".closer").first().css("display", "block");

    $(container).append(new_input_block);
    $(new_input_block).slideDown();
  }
}

function showGroupDetails(btn_obj) {
  const group = $(btn_obj).siblings(".group-details");
  $(group).toggle();
  event.preventDefault();
}

function disableForm(id) {
  $(`#${id} .btn-submit-form`).prop("disabled", true);
  $(`#${id} .add-input-row`).remove();

  let input_types = ["input", "textarea", "select", "button"];
  $.each(input_types, function () {
    $.each($(`#${id}`).find(String(this)), function () {
      $(this).prop("disabled", "true");
    });
  });
}

function getValidationRules() {
  var rule_dict = {};
  $.each($(".form .required"), function () {
    key = $(this).attr("id");
    rule_dict[key] = "required";
  });
  return rule_dict;
}

function getFormData(exercise) {
  let form_data = {};
  let section = 0;

  $.each($(`#${exercise.global_exercise_id}`).find("fieldset"), function () {
    section++;
    let section_obj = {};
    let section_name =
      $(this).find("h4").first().text() || `Section ${section}`;

    $.each(
      $(this)
        .find(".input, .editable-table")
        .not("[name='minInputs']")
        .not(".uploader-element"),
      function () {
        let input_name = $(this).attr("name");
        let input_value = "";
        if ($(this).hasClass("drawio-object")) {
          if (this.contentDocument) {
            let svgContent = this.contentDocument.documentElement.outerHTML;
            let base64String = btoa(svgContent);
            input_value = "data:image/svg+xml;base64," + base64String;
          } else {
            input_value = this.data;
          }
        } else if (
          $(this).hasClass("input") &&
          ($(this).hasClass("radio") || $(this).hasClass("checkboxes"))
        ) {
          let selected_values = [];
          $.each($(this).find("input:checked"), (index, checked_element) => {
            selected_values.push($(checked_element).val());
          });
          input_value = selected_values;
        } else if ($(this).hasClass("input")) {
          input_value = $(this).val();
        } else if ($(this).hasClass("editable-table")) {
          input_value = $(this)
            .prop("outerHTML")
            .replaceAll('contenteditable="true"', "");
        }
        section_obj[input_name] = input_value;
      }
    );

    form_data[section_name] = section_obj;
  });

  return form_data;
}

function minimumElements(form) {
  var valid = true;
  let fieldsets = $(form).find("fieldset");
  $.each(fieldsets, function () {
    let hidden_inputs = $(this).find("[name='minInputs']");
    if (hidden_inputs.length > 0) {
      var minInputs = hidden_inputs[0].value;
    }
    var additionalInputs = $(this).find("#additionalInput .input-group").length;
    if (additionalInputs + 1 < minInputs) {
      valid = false;
      $(this).addClass("error");
      $(this)
        .find("#fieldset-error")
        .html(
          `A minimum of ${minInputs} items are required. Only ${
            additionalInputs + 1
          } were given.`
        );
    } else {
      $(this).removeClass("error");
      $(this).find("#fieldset-error").html("");
    }
    let error = $("fieldset.error");
    if (error.length > 0) {
      $("html, body").animate(
        {
          scrollTop: $("fieldset.error").offset().top,
        },
        400
      );
    }
  });
  return valid;
}

function submitForm(form, exercise) {
  var defer = $.Deferred();
  if (minimumElements(form)) {
    formData = getFormData(exercise);
    sendAjax("POST", {
      url: `/submissions/form/${exercise.global_exercise_id}`,
      data: JSON.stringify(formData),
    })
      .then(function (data, textStatus, jqXHR) {
        defer.resolve(data);
      })
      .catch(function (jqXHR, textStatus, errorThrown) {
        defer.reject(jqXHR, textStatus, errorThrown);
      });
  }
  return defer.promise();
}

function initForm(exercise) {
  $(`#${exercise.global_exercise_id}`)
    .find(".add-input-row")
    .click(function () {
      appendNewInputRow($(this).closest("fieldset").attr("id"));
    });

  $(document).on("click", ".closer", function () {
    $(this)
      .parent()
      .slideUp("normal", function () {
        $(this).remove();
      });
    setTimeout(function () {
      persistForm(exercise.global_exercise_id);
    }, 500);
  });

  $(document).on("focusout", ".input-table tr td", function () {
    persistForm(exercise.global_exercise_id);
  });
  $(document).on("change", ".input", function () {
    persistForm(exercise.global_exercise_id);
  });
}

function loadForm(exercise) {
  // Get cache from server
  let storedForm = {};

  sendAjax("GET", { url: `/cache/${exercise.global_exercise_id}` })
    .then(function (data, textStatus, jqXHR) {
      storedForm = JSON.parse(data["form_data"]);

      // if stored form is not empty
      if (storedForm) {
        let inputdata = [];

        let dom_field_sets = $(`#${exercise.global_exercise_id}`).find(
          "fieldset"
        );

        const stored_fieldsets = Object.values(storedForm);
        stored_fieldsets.forEach((stored_fieldset, fieldset_index) => {
          // Expand if needed

          for (let i = 0; i < stored_fieldset.additional; i++) {
            $(dom_field_sets[fieldset_index])
              .find(".add-input-row")
              .trigger("click");
          }

          const stored_inputs = Object.values(stored_fieldset);
          stored_inputs.forEach((stored_input, input_index) => {
            if (Object.keys(stored_fieldset)[input_index] != "additional") {
              inputdata.push(stored_input);
            }
          });
        });

        // Set data
        let _inputs = $(`#${exercise.global_exercise_id}`)
          .find(".input, .editable-table")
          .not(".divider");
        $.each($(_inputs), function (index, _input) {
          if ($(_input).attr("type") != "file") {
            if (inputdata[index].type == "TABLE") {
              $(_input).html(inputdata[index].value);
            } else if (inputdata[index].type == "OBJECT") {
              $(_input).attr("data", inputdata[index].value);
            } else if (inputdata[index].type == "DIV") {
              $.each($(_input).find("input"), (_index, option) => {
                if (inputdata[index].value.includes($(option).val())) {
                  $(option).prop("checked", true);
                }
              });
            } else {
              $(_input).val(inputdata[index].value);
            }
          }
        });
        $(".editable-table tr td").focusout(() => {
          detectFullTable($(event.target).closest("table"));
        });
      }
    })
    .catch(function (jqXHR, textStatus, errorThrown) {
      console.error(jqXHR, textStatus, errorThrown);
    });
}

function persistForm(global_exercise_id) {
  let form_data_to_store = {};
  let parent = null;

  $.each(
    $(`#${global_exercise_id}`).find(".input, .editable-table").not(".divider"),

    // callback
    function (index, _input) {
      // get current fieldset
      const current_fieldset = $(_input).closest("fieldset")[0];

      // Determine if case
      const is_case_object = Boolean(
        $(current_fieldset).parents().find("#cases").length
      );

      // init parent fieldset
      if (parent != current_fieldset) {
        parent = current_fieldset;
        parentindex = index;
      }

      // if in the same fieldset
      if (parent == current_fieldset) {
        form_data_to_store[parentindex] = form_data_to_store[parentindex] || {};

        const field_type = $(_input).prop("nodeName");

        // Get amount of additionals
        let additional_count = 0;
        if (is_case_object) {
          additional_count = $(parent)
            .closest("#cases")
            .find(".case-container").length;
        } else {
          additional_count = $(parent).find(".closer").length;
        }

        // Get input value
        let input_value = null;
        if (["INPUT", "SELECT", "TEXTAREA"].includes(field_type)) {
          input_value = $(_input).val();
        } else if (["TABLE"].includes(field_type)) {
          input_value = $(_input).html();
        } else if (["OBJECT"].includes(field_type)) {
          input_value = $(_input).attr("data");
        } else if (
          ["DIV"].includes(field_type) &&
          ($(_input).hasClass("radio") || $(_input).hasClass("checkboxes"))
        ) {
          let selected_values = [];
          $.each($(_input).find("input:checked"), (index, checked_element) => {
            selected_values.push($(checked_element).val());
          });
          input_value = selected_values;
        }

        form_data_to_store[parentindex][index] = {
          value: input_value || "",
          type: field_type || "default",
        };
        form_data_to_store[parentindex]["additional"] = additional_count - 1;
      }
    }
  );

  // Set cache on server
  sendAjax("PUT", {
    url: `/cache`,
    data: JSON.stringify({
      global_exercise_id: global_exercise_id,
      form_data: form_data_to_store,
    }),
  }).catch(function (jqXHR, textStatus, errorThrown) {
    console.error(jqXHR, textStatus, errorThrown);
  });
}

function setSectionValues(element, section) {
  if (section) {
    $.each(
      $(element)
        .find(".input")
        .not("[name='minInputs']")
        .not(".uploader-element"),
      function () {
        $(this).val(section[$(this).attr("name")]);
      }
    );
  }
}

function getSectionValues(element) {
  let input_group_obj = {};
  $.each(
    $(element)
      .find(".input")
      .not("[name='minInputs']")
      .not(".uploader-element"),
    function () {
      let input_name = $(this).attr("name");
      let input_value = $(this).val();
      input_group_obj[input_name] = input_value;
    }
  );
  return input_group_obj;
}

$.extend(jQuery.validator.messages, {
  required: "",
});
