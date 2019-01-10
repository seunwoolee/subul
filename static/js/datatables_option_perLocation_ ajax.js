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
var gubun = ".gubun1";
var product;

function addRow()
{
	row =  '<tr class="animated fadeIn">'
	row += '<td><select class="form-control gubun'+counter+'">'
	row += '<option value=""></option>'
	row += ' <optgroup label="생산절차">'
	row += ' <option value="할란">할란</option>'
	row += ' <option value="할란사용">할란사용</option>'
	row += ' <option value="공정품투입">공정품투입</option>'
	row += ' <option value="공정품발생">공정품발생</option>'
	row += ' <option value="제품생산">제품생산</option>'
	row += ' </optgroup>'
	row += ' </select></td>'
	row += ' <td><select class="form-control product'+counter+'" >'
	row += ' <option value=""></option>'
	row += ' <optgroup label="제품명">'
	row += ' </optgroup>'
	row += ' </select></td>'		 
	row += '                      <td>'                        
	row += '						<div class="input-group">'
	row += '                          <span class="input-group-prepend">'
	row += '                            <span class="input-group-text">'
	row += '                              <i class="fa fa-phone"></i>'
	row += '                            </span>'
	row += '                          </span>'
	row += '                          <input class="form-control" id="phone" type="text">'
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
	
	gubun = '.gubun'+counter;
	product = '.product'+counter;
	
	

	$('#result').append(row); // Row 생성
	$(gubun).select2({placeholder: '공정 구분'}); //select2 기능활성화
	$(product).select2({  placeholder: '제품명을 선택해주세요'}); //select2 기능활성화	
	
	counter++; //class 고유번호를 위한 counter ++
	$(gubun).focus(); // 편의기능(신규 생성된곳 focus)
	
	
counterM = counter-1; 
gubun = ".gubun"+counterM;
tesss = gubun+" option:selected";

$( gubun ).change(function () {
	var str;
    $( tesss ).each(function() {
      str = $( this ).text();
	  gubunStep(str,product);
    });
  }).change();	
}

function gubunStep(str,product)
{
	if(str == '공정품투입' || str == '공정품발생')
	{
		fetch('ajax/공정품.html').then(function(response){
			return response.text();
		}).then(function(j){
			$(product+" option").remove();
			$(product).append(j);
		});
	}
	else if(str == '제품생산')
	{
		fetch('ajax/제품생산.html').then(function(response){
			return response.text();
		}).then(function(j){
			$(product+" option").remove();
			$(product).append(j);
		});
	}
	else if(str == '할란' || str == '할란사용')
	{
		fetch('ajax/할란.html').then(function(response){
			return response.text();
		}).then(function(j){		
			$(product+" option").remove();
			$(product).append(j);
		});
	}
}

// $('#select2-3').select2({
  // theme: 'bootstrap',
  // placeholder: 'Your Favorite Football Team',
  // allowClear: true
// });
//# sourceMappingURL=datatables.js.map