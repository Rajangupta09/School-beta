/* 
  Dyynamically creates form in formset
  requirments:
    The formset must be wrapped in a div and a button with class 'add-new-form'
    should be only one level deep

    The div should contain an attribute called 'prefix' that has value for formset
    prefix 

    Form fields must be wrapped in div with class 'fieldset' that works as a handler
    that is cloned by jquery

*/

$(document).ready(function () {
  $('.add-new-form').click(function (event) {
    event.stopPropagation();
    event.preventDefault();
    let $formsetContainer = $(event.target).parent();
    prefix = $formsetContainer.attr('prefix');
    let totalForms = $formsetContainer.find(`#id_${prefix}-TOTAL_FORMS`);
    let currentForms = parseInt(totalForms.attr('value'));
    totalForms.attr('value', currentForms + 1);

    let fieldset = $formsetContainer.find('.fieldset').last();
    let newForm = fieldset.clone();

    $(newForm).insertAfter(fieldset);

    $.each(newForm.find('input.form-control'), function (
      indexInArray,
      element
    ) {
      $(element).val('');
      let id = $(element).attr('id');
      let name = $(element).attr('name');
      console.log(id);
      $(element).attr('id', updateAttr(id, currentForms));
      $(element).attr('name', updateAttr(name, currentForms));
    });

    $.each(newForm.find('select.form-control'), function (
      indexInArray,
      element
    ) {
      $(element).val('');
      let id = $(element).attr('id');
      let name = $(element).attr('name');
      console.log(id);
      $(element).attr('id', updateAttr(id, currentForms));
      $(element).attr('name', updateAttr(name, currentForms));
    });

    $.each(newForm.find('label'), function (indexInArray, element) {
      let attrFor = $(element).attr('for');
      $(element).attr('for', updateAttr(attrFor, currentForms));
    });

    $.each(newForm.find('.form-group'), function (indexInArray, element) {
      let id = $(element).attr('id');
      $(element).attr('id', updateAttr(id, currentForms));
    });
  });
});

let updateAttr = function (oldString, newValue) {
  let oldStringList = oldString.split('-');
  oldStringList[1] = newValue.toString();
  // console.log(oldStringList.join('-'));
  return oldStringList.join('-');
};
