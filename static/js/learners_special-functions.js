// Risk Calculation

function calcRiskValue(element) {
  let risk_id = element.id.split("_")[1]
  let likelihood_value = $(`#likelihood_${risk_id}`)[0].value;
  let impact_value = $(`#impact_${risk_id}`)[0].value;
  $(`#risk_${risk_id}`)[0].value =
    parseInt(likelihood_value.slice(0, 1)) * parseInt(impact_value.slice(0, 1));
}


function editDrawIO(event, button_element) {
  event.preventDefault();
  const drawio_obj = $(button_element).closest(".drawio-previewer").find(".drawio-object")[0];
  DiagramEditor.editElement(drawio_obj)
}

function resetDrawIO(event, button_element, original_data) {
  const drawio_obj = $(button_element).closest(".drawio-previewer").find(".drawio-object")[0];
  $(drawio_obj).attr('data', original_data);
  event.preventDefault();
}