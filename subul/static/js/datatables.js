/**
 * --------------------------------------------------------------------------
 * CoreUI Pro Boostrap Admin Template (2.1.1): datatables.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */
var t = $('.datatable').DataTable({
        "language": {
            "lengthMenu": "_MENU_ 페이지당 개수",
            "zeroRecords": "결과 없음",
            "info": "page _PAGE_ of _PAGES_",
            "infoEmpty": "No records available",
            "infoFiltered": "(검색된결과 from _MAX_ total records)"
        }
    });

	
hotkeys('f2', function(event, handler) {
  // Prevent the default refresh event under WINDOWS system
  event.preventDefault();
  addRow();
});

$('.gubun1').select2({placeholder: '공정 구분'});
$('.product1').select2({  placeholder: '제품명을 선택해주세요'});

 
var counter = 1;
var product;

function addRow()
{
	row =  '<tr class="animated fadeIn">'
	row += '<td>'+counter+'</td>'
	row += ' <td><select class="form-control product'+counter+'" >'
	row += ' <option value=""></option>'
	row += ' <optgroup label="제품명">'
	row += ' <option value="00152">오랩 요리란 500g 전란</option>'
	row += ' <option value="00151">오랩 요리란 500g 난백</option>'
	row += ' <option value="00150">오랩 요리란 200g 전란</option>'
	row += ' <option value="00149">오랩 요리란 200g 난백</option>'
	row += ' </optgroup>'
	row += ' </select></td>'		 
	row += '                      <td>'                        
	row += '						<div class="input-group">'
	row += '                          <span class="input-group-prepend">'
	row += '                            <span class="input-group-text">'
	row += '                              <i class="fa fa-phone"></i>'
	row += '                            </span>'
	row += '                          </span>'
	row += '                          <input class="form-control" name="asdf1" id="phone" type="text">'
	row += '						</div>'
	row += '					  </td>'
	row += '                      <td>'
	row += '						<div class="input-group">'
	row += '                          <span class="input-group-prepend">'
	row += '                            <span class="input-group-text">'
	row += '                              <i class="fa fa-phone"></i>'
	row += '                            </span>'
	row += '                          </span>'
	row += '                          <input class="form-control" id="phone" type="text">'
	row += '						</div>'
	row += '                      </td>'
	row += '                      <td>'
	row += '						<div class="input-group">'
	row += '                          <span class="input-group-prepend">'
	row += '                            <span class="input-group-text">'
	row += '                              <i class="fa fa-edit"></i>'
	row += '                            </span>'
	row += '                          </span>'
	row += '                          <textarea class="form-control" rows="2" id="memo" name="memo">'
	row += '						  </textarea>'
	row += '						</div>'
	row += '                      </td>'
	row += '                      <td>'
	row += '                        <a class="btn btn-success" href="#">'
	row += '                          <i class="fa fa-search-plus"></i>'
	row += '                        </a>'
	row += '                        <a class="btn btn-info" href="#">'
	row += '                          <i class="fa fa-edit"></i>'
	row += '                        </a>'
	row += '                        <a class="btn btn-danger" href="#">'
	row += '                          <i class="fa fa-trash-o"></i>'
	row += '                        </a>'
	row += '                      </td>'
	row += '                    </tr>'
	
	product = '.product'+counter;
	
	

	$('#result').append(row); // Row 생성
	$(product).select2({  placeholder: '제품명을 선택해주세요'}); //select2 기능활성화	
	
	counter++; //class 고유번호를 위한 counter ++
	$(product).focus(); // 편의기능(신규 생성된곳 focus)

}




function cloneMore(selector, prefix) {
    $(selector).find('select').select2("destroy");

    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name')

        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.forms-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('-');

    $('.django-select2').djangoSelect2();
    return false;
}

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.forms-row').remove();
        var forms = $('.forms-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0; i<forms.length; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.forms-row:last', 'form');
    return false;
});

$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    console.log($(this))
    deleteForm('form', $(this));
    return false;
});

// $('#select2-3').select2({
  // theme: 'bootstrap',
  // placeholder: 'Your Favorite Football Team',
  // allowClear: true
// });
//# sourceMappingURL=datatables.js.map