$(function(){
    $('#userHosts td input[type="checkbox"]').iCheck({
	checkboxClass: 'icheckbox_flat-blue'
	});

    $("#userHosts th .checkbox-toggle").click(function () {
	var clicks = $(this).data('clicks');
	if (clicks) {
	    $("#userHosts input[type='checkbox']").iCheck("uncheck");
	    $(".fa", this).removeClass("fa-check-square-o").addClass('fa-square-o');
	}else{
	    $("#userHosts input[type='checkbox']").iCheck("check");
	    $(".fa", this).removeClass("fa-square-o").addClass('fa-check-square-o');
	}
	    $(this).data("clicks", !clicks);
    });
	
    $("#del_auth").click(function(){
	$("#ajaxModal").modal('toggle')
	var data_dict={}
	var user_id = $("#user_tag").attr("user_id")
	$("tbody tr td .checked").each(function(){
	    var tmp_id = $(this).parent().parent().attr("host_id")
	    data_dict[tmp_id]=user_id
	});
	var data = {
	    data:JSON.stringify(data_dict)
	}

	$.ajax({
	    url:"/auths/authorizeuser/ajax/deluserhost/",
	    type:"POST",
	    data:data,
	    dataType:"json",
	    success:function(data){
	    location.reload()
	    }
	})
    });

    //变更用户角色按钮事件
    $("td button[btn_action='edituserRole']").bind('click',function(){
	$(this).text("保存变更");
	$(this).unbind().bind("click",saveuserRole);
	$(this).next().removeClass("hide").text("取消变更").bind("click",canceleditRole)
	// ajax
	var mythis = $(this)
	$.ajax({
	    url:"/auths/authorizeuser/ajax/getroles/",
	    type:"get",
	    dataType:"json",
	    success:function(data){
	    var tmp_option = ""
	    for (role in data){
		var tmp_html = "<option value ='"+data[role]["role_id"]+"'>"+data[role]["role_name"]+"</option>"	
		var tmp_option = tmp_option+tmp_html
	    }
		var select_html = "<select>"+tmp_option+"</select>"
		mythis.parent().prev().prev().text("").append(select_html)
	    }
	});//--end ajax
    });
    // end get roles
    function canceleditRole(){
	location.reload()
    }
    function saveuserRole(){
	var data_dic={}
	data_dic["host_id"]=$(this).parent().prev().prev().attr("host_id")
	data_dic["role_id"]=$(this).parent().prev().prev().children().val()
	data_dic["user_id"]=$("#user_tag").attr("user_id")
	var data = {
		data:JSON.stringify(data_dic)
	    }
	$.ajax({
		url:"/auths/authorizeuser/ajax/editrole/",
		type:"POST",
		timeout:10000,
		data:data,
		dataType:"JSON",
		success:function(){
		    location.reload()
		}
	});
    }
});
