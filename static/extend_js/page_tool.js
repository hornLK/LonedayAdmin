	//-- 分页获取主机
	$("a[ajax_href]").click(function(){
	    $("#add_table th .checkbox-toggle").children().removeClass("fa-check-square-o").addClass("fa-square-o")
	    $("#auth_table th .checkbox-toggle").children().removeClass("fa-check-square-o").addClass("fa-square-o")
	    if ( $(this).attr("ajax_href") != "null" ){
		var page_url = $(this).attr("ajax_href")
		if ($(this).attr("a_tag")=="true"){
		    $(this).parent().siblings().removeClass("active")
		    $(this).parent().addClass("active")
		}
		var mythis = $(this)
		$.ajax({
			type:"GET",
			url:page_url,
			dataType:"json",
			success:function(data){
			$("#outhosts").html("")
			var tmp_html=""
			for (host in data.hosts){
			    var tmp_html = "<tr host_id="+data.hosts[host]["id"]+"><td><input type='checkbox' /></td><td>"+data.hosts[host]["hostName"]+"</td><td>"+data.hosts[host]["hostIP"]+"</td><td>"+data.hosts[host]["hostGroup"]+"</td></tr>"	
			    $("#outhosts").append(tmp_html)
			}
					//锁定已经选中主机
					lockHoststr()
					$('.hostbox-messages input[type="checkbox"]').iCheck({
					    checkboxClass: 'icheckbox_flat-blue',
							radioClass: 'iradio_flat-blue'
					  });
					//上一页下一页样式
					//上一页样式
					if (data.prev != null){
						$("#outhosts_previous").removeClass("disabled")
					}else{
						$("#outhosts_previous").addClass("disabled").children().attr("ajax_href","null")
					}
					var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
					var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
					$("#outhosts_previous").children().attr("ajax_href",prev_url)
					$("#outhosts_next").children().attr("ajax_href",next_url)
					if (mythis.parent().attr("id") == "outhosts_previous"){
						if ($("#outhosts_paginate ul .active").prev().attr("id") == "outhosts_previous"){
							$("#outhosts_paginate ul .active").prev().addClass("disabled").children().attr("ajax_href","null")
						}else{
							$("#outhosts_paginate ul .active").removeClass("active").prev().addClass("active")
							var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
							var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
							$("#outhosts_previous").children().attr("ajax_href",prev_url)
							$("#outhosts_next").children().attr("ajax_href",next_url)
						}
					}
					//--下一页样式
					if (data.next != null){
						$("#outhosts_next").removeClass("disabled")
					}else{
						$("#outhosts_next").addClass("disabled").children().attr("ajax_href","null")
					}
					var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
					var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
					$("#outhosts_next").children().attr("ajax_href",next_url)
					$("#outhosts_previous").children().attr("ajax_href",prev_url)
					if (mythis.parent().attr("id") == "outhosts_next"){
						if ($("#outhosts_paginate ul .active").next().attr("id") == "outhosts_next"){
							$("#outhosts_paginate ul .active").next().addClass("disabled").children().attr("ajax_href","null")
						}else{
							$("#outhosts_paginate ul .active").removeClass("active").next().addClass("active")
							var next_url=$("#outhosts_paginate ul .active").next().children().attr("ajax_href")
							var prev_url=$("#outhosts_paginate ul .active").prev().children().attr("ajax_href")
							$("#outhosts_previous").children().attr("ajax_href",prev_url)
							$("#outhosts_next").children().attr("ajax_href",next_url)
						}
					}
				}
			})
		}
	});
//-------end
