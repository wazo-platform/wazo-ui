/*
  https://github.com/select2/select2/issues/195#issuecomment-240130634
  Define the adapter so that it's reusable
*/
$.fn.select2.amd.define('select2/selectAllAdapter', [
  'select2/utils',
  'select2/dropdown',
  'select2/dropdown/attachBody'
], function (Utils, Dropdown, AttachBody) {

  function SelectAll() {
  }

  SelectAll.prototype.render = function (decorated) {
    var self = this,
      $rendered = decorated.call(this),
      $selectAll = $(
        '<button class="btn btn-xs btn-default" type="button" style="margin-left:6px;"><i class="fa fa-check-square-o"></i> Select All</button>'
      ),
      $unselectAll = $(
        '<button class="btn btn-xs btn-default" type="button" style="margin-left:6px;"><i class="fa fa-square-o"></i> Unselect All</button>'
      ),
      $btnContainer = $('<div style="margin-top:3px;">').append($selectAll).append($unselectAll);
    if (!this.$element.prop("multiple")) {
      // this isn't a multi-select -> don't add the buttons!
      return $rendered;
    }
    $rendered.find('.select2-dropdown').prepend($btnContainer);
    $selectAll.on('click', function (e) {
      var $results = $rendered.find('.select2-results__option[aria-selected=false]');
      $results.each(function () {
        self.trigger('select', {
          data: $(this).data('data')
        });
      });
      self.trigger('close');
    });
    $unselectAll.on('click', function (e) {
      var $results = $rendered.find('.select2-results__option[aria-selected=true]');
      $results.each(function () {
        self.trigger('unselect', {
          data: $(this).data('data')
        });
      });
      self.trigger('close');
    });
    return $rendered;
  };

  return Utils.Decorate(
    Utils.Decorate(
      Dropdown,
      AttachBody
    ),
    SelectAll
  );

});