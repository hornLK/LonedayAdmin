$(function(){
    $("#add_CheckedAll2").click(function () {
	if ($(this).is(":checked")) {
	    $("#add_auth_table [name=id]:checkbox").prop("checked", true);
	} else {
	    $("#add_auth_table [name=id]:checkbox").prop("checked", false);
	}
    });
    $("#add_CheckedAll1").click(function () {
	if ($(this).is(":checked")) {
	    $("#outhosts [name=id]:checkbox").each(function(){
		if  ( !$(this).attr("disabled")){
			$(this).prop("checked", true);
		    }
	    })
	} else {
	    $("#outhosts [name=id]:checkbox").each(function(){
		if ( !$(this).attr("disabled")){
			$(this).prop("checked", false)
		    }
	    })
	}
    });
	//--比较两个表，冻结已添加的表
	function lockHoststr(){ //创建一个数组，获取添加的hostid，out表中的host_id与之做比较
	    var hostIdList= new Array()
		$("#add_auth_table tr").each(function(){
		    var host_id=$(this).attr("host_id")
		    hostIdList.push(host_id)
		})
		$("#outhosts tr").each(function(){
		    var out_id=$(this).attr("host_id")
		    if ( $.inArray(out_id,hostIdList) != -1 ){
			$(this).addClass("tr-disabled ").children().first().children().prop("checked",false).iCheck('disable')
			}
		})
	};
    //Enable check and uncheck all functionality
    $("#add_table th .checkbox-toggle").click(function () {
	var clicks = $(this).data('clicks');
	if (clicks) {
	    $("#add_table div[aria-disabled!='true'] input[type='checkbox']").iCheck("uncheck");
	    $(".fa", this).removeClass("fa-check-square-o").addClass('fa-square-o');
	}else{
	    $("#add_table input[type='checkbox']").iCheck("check");
	    $(".fa", this).removeClass("fa-square-o").addClass('fa-check-square-o');
	}
	    $(this).data("clicks", !clicks);		
	});
	//--添加主机按钮_new
	$("#addHostBtn").click(function(){
             var flag = false
	     $("#model_hosts").html("")
             $("#outhosts input[type='checkbox']").each(function(){
                if ($(this).prop('checked')){
	    		var host_id = $(this).parent().parent().attr("host_id")
			var check_tr = $(this).parent().parent().html()
			$("#model_hosts").append("<tr host_id="+host_id+">"+check_tr+"</tr>")
                        flag = true
		}
	    });
	    if ( !flag ){
		$('#addModal').modal('toggle')
	        $("#model_hosts").html("")
	    }
	    
	});	
	//--end 添加主机_new

    //---添加确认授权表
    $("#model_auth").click(function(){
	var selected_role = $("#select_role").val()
	$("#model_hosts tr").each(function(){
	    var host_id = $(this).attr("host_id")
	    var tmp_html=$(this).children().last().text(selected_role).parent().html()	
	    $("#add_auth_table").append("<tr host_id="+host_id+">"+tmp_html+"</tr>")
	    })
	    $("#add_auth_table td div").parent().html("").append("<input  type='checkbox' />")
	    $('#addModal').modal('toggle')
	    lockHoststr()
	})
    //---end 模态里的授权
    //-- 确认授权按钮
    $("#confirmAuth").click(function(){
	var flag=false
	$("#add_auth_table [name=id]:checkbox").each(function(){
	    if ($(this).prop('checked')){
		flag=true
	    }	
	})
	if (flag){
	    swal({
		title: "确定授权",
		text: "用户添加主机授权",
		type: "warning",
		showCancelButton: true,
		confirmButtonColor: "#DD6B55",
		confirmButtonText: "确定",
		closeOnConfirm: false
		},function(){
			var user_id = $("#user_tag").attr("user_id")
			var hostRole = {}
			$("#add_auth_table [name=id]:checkbox").each(function(){
                             if ($(this).is(":checked")){
				var host_id = $(this).parent().parent().attr("host_id")
				var role = $(this).parent().siblings().last().text()
				hostRole[host_id]=role
			     }
			})
			$("#confirmAuth").attr("disabled","disabled")
			//post数据给用户授权
			$.ajax({
				url:"/auths/authorizeuser/ajax/authhostsuser/",
				type:"POST",
				data:{"data":JSON.stringify({"host_role":hostRole,"user_id":user_id})},
				dataType:"json",
				success:function(data){
				    console.log(data)
                                    if (data.status){
					swal({title: "添加", text: "已成功添加", type: "success"}, function () {
					$('#add_table input[type="checkbox"]').prop("checked",false)
                                        window.location.reload();
					})
				    }else{
					 swal("错误", "删除" + "[ " + data.error + " ]" + "遇到错误", "error");
				    }
				}
			    })
			}
		    )
		}
	    }
	);
//-- end确认授权更改数据库
//-----	
});

