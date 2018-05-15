$(function(){
    //验证手机号是否合规
    function checkPhone(str) {
	var re = /^1\d{10}$/
	if (re.test(str)) {
	    } else {
		alert("手机号输入有误");
		}
	}
    //结束验证手机号
    //编辑用户信息
    $("button[btn_action='edituser']").click(function () {
    //更改属性
    $(this).attr("btn_action","saveuser").text("保存")
    //解绑编辑事件,添加保存事件
    $(this).unbind().bind("click",save_useredit)
	$(this).siblings().each(function(){
	if ($(this).children().attr("btn_action")=="authuser"){
	    $(this).hide();
	    }
	if ($(this).attr("btn_action")=="deleteuser"){
	    $(this).attr("btn_action","canceluser").text("取消").bind("click",cancel_useredit)
	    }
	});
	$(this).parent().siblings().each(function(){
	    if( $(this).attr("userinfo") == "weixinnumber" ){
		var text = $(this).text();
		//td标签中添加input标签
		var edit_input = $(this).text("").append("<input type='text' class='useredit' />").children()
		edit_input.val(text);
		edit_input.focusin(function(){
		    $(this).val("")	
		});
	    };
	    if( $(this).attr("userinfo") == "confirmed" ){
		var text = $(this).text();
		//td标签中添加select标签
		edit_input = $(this).text("").append("<select><option value ='True'>True</option><option value ='False'>False</option></select>")
		});
	});
	//end 用户编辑
	//取消用户输入
	function cancel_useredit(){
		location.reload()
	}
	//end 取消用户输入
	//保存用户输入
	function save_useredit(){
	    $("#ajaxModal").modal('toggle')
	    var data_dic={}
	    $(this).parent().siblings().each(function(){
		if( $(this).attr("userinfo") == "username" ){
		    var user_id = $(this).attr("user_id")
		    data_dic["user_id"] = user_id
		}
		if( $(this).attr("userinfo") == "weixinnumber" ){
		    var weixin = $(this).children().val()
		    data_dic["weixinnumber"] = weixin
		    }
		if( $(this).attr("userinfo") == "confirmed" ){
		    var confir = $(this).children().val()
		    data_dic["confirmed"] = confir
		    }
	    });	
	    var data = {
		    data:JSON.stringify(data_dic)
		};
	    $.ajax({
		    url:"/auths/authorizeuser/ajax/edituser/",
		    type:"POST",
		    timeout: 10000,
		    data:data,
		    dataType:'JSON',
		    success:function(data){
			if (data.status){ 
				location.reload()
			}else{
			    location.reload()
			    alert("变更失败，请联系管理员")	
			}
			    }
	    })
	}
	//end  保存用户输入
});
