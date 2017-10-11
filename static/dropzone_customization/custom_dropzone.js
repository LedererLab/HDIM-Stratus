function CustomDZaddedfile ( file ) {

  switch(file.type) {
    case 'application/vnd.ms-excel':
    case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
      console.log( parseExcel( file ) );
    break;
    case 'text/csv':
      Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        complete: function(results) {
          var data_names = Object.keys(results.data[0]);
          removeOptions( "response_var" );
          populateColumnNames( data_names, "response_var" );
          selectFirstOption( "response_var" );
        }
      });
      break;
    default:
      alert('Please enter correct file format.');
    break;
  }

  // Default functionality provided by DropZone
  var j, k, l, len, len1, len2, node, ref, ref1, ref2, removeFileEvent, removeLink, results;
  if (this.element === this.previewsContainer) {
    this.element.classList.add("dz-started");
  }
  if (this.previewsContainer) {
    file.previewElement = Dropzone.createElement(this.options.previewTemplate.trim());
    file.previewTemplate = file.previewElement;
    this.previewsContainer.appendChild(file.previewElement);
    ref = file.previewElement.querySelectorAll("[data-dz-name]");
    for (j = 0, len = ref.length; j < len; j++) {
      node = ref[j];
      node.textContent = file.name;
    }
    ref1 = file.previewElement.querySelectorAll("[data-dz-size]");
    for (k = 0, len1 = ref1.length; k < len1; k++) {
      node = ref1[k];
      node.innerHTML = this.filesize(file.size);
    }
    if (this.options.addRemoveLinks) {
      file._removeLink = Dropzone.createElement("<a class=\"dz-remove\" href=\"javascript:undefined;\" data-dz-remove>" + this.options.dictRemoveFile + "</a>");
      file.previewElement.appendChild(file._removeLink);
    }
    removeFileEvent = (function(_this) {
      return function(e) {
        e.preventDefault();
        e.stopPropagation();
        if (file.status === Dropzone.UPLOADING) {
          return Dropzone.confirm(_this.options.dictCancelUploadConfirmation, function() {
            return _this.removeFile(file);
          });
        } else {
          if (_this.options.dictRemoveFileConfirmation) {
            return Dropzone.confirm(_this.options.dictRemoveFileConfirmation, function() {
              return _this.removeFile(file);
            });
          } else {
            return _this.removeFile(file);
          }
        }
      };
    })(this);
    ref2 = file.previewElement.querySelectorAll("[data-dz-remove]");
    results = [];
    for (l = 0, len2 = ref2.length; l < len2; l++) {
      removeLink = ref2[l];
      results.push(removeLink.addEventListener("click", removeFileEvent));
    }
    return results;
  }

}

function CustomDZSend( file, xhr, data ) {

  if( document.getElementById("lasso_av_button").checked ) {
    data.append("regression_type","av");
  } else if ( document.getElementById("lasso_cv_button").checked ) {
    data.append("regression_type","cv");
  } else if ( document.getElementById("fos_button").checked ) {
    data.append("regression_type","fos");
  } else {
    alert( "Please select a valid regression method!" );
  }

  switch(file.type) {
    case 'application/vnd.ms-excel':
    case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
      data.append("data_type","xlsx");
    break;
    case 'text/csv':
      data.append("data_type","csv");
      break;
    default:
      alert('Please enter correct file format.');
    break;
  }

  var regression_var_index = $('#response_var').index();
  alert( "Regression Index",regression_var_index);
  data.append( "regression_index", regression_var_index );

}

function CustomDZSuccess( file, response ) {
  barChart.updateChart( response );
  file.status = Dropzone.QUEUED; // Re-que file so that it can be resubmitted
}
