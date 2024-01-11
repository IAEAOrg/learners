$(function () {
  $(".PINbutton").click(function () {
    if ($(this).hasClass("clear")) {
      clearForm(this);
    } else if ($(this).hasClass("enter")) {
      submitForm($("#PINbox").val());
    } else {
      addNumber(this);
    }
  });

  function addNumber(e) {
    //document.getElementById('PINbox').value = document.getElementById('PINbox').value+element.value;
    var v = $("#PINbox").val();
    $("#PINbox").val(v + e.value);
  }
  function clearForm(e) {
    //document.getElementById('PINbox').value = "";
    $("#PINbox").val("");
  }
  function submitForm(enteredpin) {
    if (enteredpin == "") {
      alert("Enter a PIN");
    } else {
      alert("Your PIN has been sent! - " + enteredpin);
      data = {
        pin: enteredpin,
      };
      /*		
            apiCall( data, function( r ) {
                $( "#logo" ).attr( "src", r.site_logo );
                $( ".title-msg" ).text( r.site_msg );
                accent = r.accent;
                $( ".accent-bg" ).css( "background-color", accent );
            });
            */

      //document.getElementById('PINbox').value = "";
      $("#PINbox").val("");
    }
  }

  /*
    function apiCall( post, callback ) {	
        $.ajax({
            type: "POST",
            contentType: "application/json",
            url: "admin/api.php",
            data: JSON.stringify( post ),
            dataType: "json",
            success: function ( r ) {
                callback( r );
            },
            error: function ( response ) {
                console.log( response )
            },
        });
    }
    */

  initDroppable();

  $("#dvSource a").click(function (e) {
    e.preventDefault();
    alert("Gregor is the best");
  });

  function initDroppable() {
    var img_list = $("#dvSource").find("img");
    var sourceContainer = $("#dvSource");
    sourceContainer.html(img_list);
    sourceContainer.append(
      "<a href='test.html' target='_blank'>add own picture</a>"
    );
    sourceContainer.find("img").removeClass("dropped");
    sourceContainer.find("img").css("left", "");
    sourceContainer.find("img").css("top", "");

    $("#dvSource img").draggable({
      revert: "invalid",
      refreshPositions: true,
      drag: function (event, ui) {
        console.log("drag");
        ui.helper.addClass("draggable");
      },
      stop: function (event, ui) {
        ui.helper.removeClass("draggable");
      },
    });
  }

  $("#pictureUploadArea").droppable({
    drop: function (event, ui) {
      if ($("#pictureUploadArea img").length == 0) {
        $("#pictureUploadArea").html("");
      } else {
        console.log(ui);
        $("#dvSource").append($("#pictureUploadArea").html());
        initDroppable();
      }
      ui.draggable.addClass("dropped");
      $("#pictureUploadArea").html(ui.draggable);
    },
  });

  // ################################################
  // UPLOAD local image
  // ################################################

  // function markDragover(e) {
  //     e.preventDefault();
  //     $("#PINform").addClass("is-dragover");
  // }
  // function unmarkDragover(e) {
  //     e.preventDefault();
  //     $("#PINform").removeClass("is-dragover");
  // }

  // $("#pictureUploadArea").on({
  //     'dragover': function (e) { markDragover(e) },
  //     'dragenter': function (e) { markDragover(e) }
  // });

  // $("#pictureUploadArea").on({
  //     'dragleave': function (e) { unmarkDragover(e) },
  //     'drop': function (e) { unmarkDragover(e) },
  //     'dragend': function (e) { unmarkDragover(e) }
  // });

  // $("#pictureUploadArea").on({
  //     'drop': function (e) {
  //         unmarkDragover(e)
  //         var image = e.originalEvent.dataTransfer.files;
  //         createFormData(image);
  //     },

  // });

  // function createFormData(image) {
  //     var formImage = new FormData();
  //     formImage.append('userImage', image[0]);
  //     uploadFormData(formImage);
  // }

  // function uploadFormData(formData) {

  //     console.log("upload image")
  //     console.log(formData)
  //     // $.ajax({
  //     //     url: "upload.php",
  //     //     type: "POST",
  //     //     data: formData,
  //     //     contentType: false,
  //     //     cache: false,
  //     //     processData: false,
  //     //     success: function (data) {
  //     //         $('#pictureUploadArea').append(data);
  //     //     }
  //     // });

  // }
});
