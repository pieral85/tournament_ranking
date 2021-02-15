
$('#club_matches').bootstrapTable({
  onColumnSwitch: function (field, checked) {
    console.log('onColumnSwitch');
    console.log(field);
    console.log(checked);
  },
  onPostBody: function () {
    console.log('onPostBody');
    /*arguments[1].columns[0].visible = false;*/
  },
  showColumn: function () {
    console.log('showColumn');
  },
  hideColumn: function () {
    console.log('hideColumn');
  }
});
