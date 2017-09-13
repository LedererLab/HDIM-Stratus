class dropDown {
  constructor( divName ) {
    //
  }

 populateColumnNames( col_name_array ) {
    // var db_select = document.getElementById( drop_down );

    for (var i = 0; i < col_name_array.length; i++) {
      var option = document.createElement("option");
      option.text = col_name_array[i];
      db_select.add(option);
    }
  }

 removeOptions(selectbox) {
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--) {
        selectbox.remove(i);
    }
  }

}
