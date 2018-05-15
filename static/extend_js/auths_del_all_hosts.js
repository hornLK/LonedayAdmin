$(function(){
    $(document).on('click', '.host_all_del', function () {
	    var user_id = $(this).attr("user_id")
	    swal({
		title: "确定删除？",
		text: "删除该用户的主机授权",
		type: "warning",
		showCancelButton: true,
		confirmButtonColor: "#DD6B55",
		confirmButtonText: "确定",
		closeOnConfirm: false
	    }, function () {
                 var data_dict={}
		 $("input[name='id']").prop("checked",function(){
                    if ($(this).prop("checked")){
			data_dict[$(this).attr('value')]=user_id
			} 
		})
		 console.log(data_dict)
                 var data = {
			data:JSON.stringify(data_dict)
		    }
		$.ajax({
		    url: "/auths/authorizeuser/ajax/deluserhost/",
		    type: 'POST',
		    data: data,
		    dataType:"json",
		    success: function (data) {
			if (data.status) {
			    swal({title: "删除", text: "已成功删除", type: "success"}, function () {
				window.location.reload();
			    })
			} else {
			    swal("错误", "删除" + "[ " + obj.error + " ]" + "遇到错误", "error");
			}
		    }
		});
	    });
	});
    });
