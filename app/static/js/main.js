$(function() {
   //上传图片
	$('#posterFile').change(function() {
		$('#poster_value').val($('input[id=posterFile]').val());
	});

	$('.btn-upload').click(function() {
		var upload = true;
		$('.btn .fa-upload').attr('data-load', 'false');
		var load = $('.btn .fa-upload').attr('data-load');
		var arry = ['png', 'jpg', 'jpeg', 'gif'];
		if($('#poster_value').val() == '') {
			alert('图片地址不能为空！');
			return;
		}
		for(var i = 0; i < arry.length; i++) {
			if(!$('#poster_value').val().indexOf(arry[i]) <= -1) {
				alert('上传内容不是图片！');
				upload = false;
				break;
			}
		}

		if(upload) {
			var formData = new FormData(); //通过jquery的FormData类获取数据：头像和它的地址
			formData.append("file", $("#posterFile")[0].files[0]);
			$.ajax({
				url: "/main/upload",
				type: 'POST',
				data: formData,
				cache: false,
				contentType: false,
				processData: false,
				success: function(poster_url) {
					alert("上传成功，头像地址为：" + poster_url + "，请点击[提交]保存项目信息");
					$('#poster_value').val(poster_url);
					if(load == 'false') {
						$('.btn .fa-upload').attr('data-load', 'true');
					}
				},
				error: function(poster_url) {
					alert("上传出错：" + poster_url);
				}
			});
		}
	});
	//subject下拉菜单
	$('.dropdown-toggle').click(function() {
		$('.dropdown-subjectMenu').toggle();
	});
	$('.dropdown-subjectMenu').mouseleave(function() {
		$('.dropdown-subjectMenu').hide();
	});

	//显示checkbox的勾选值
	$('.dropdown-subjectMenu').delegate('input[type="checkbox"]', 'click', function() {
		var arry = [];
		$('.dropdown-subjectMenu input[type="checkbox"]').each(function(index, ele) {
			if($(this).is(':checked')) {
				var val = $(this).parent().text();
				arry.push(val);
			}
		});
		$('#prj_prosubject').val(arry.join(';'));

	});

	//上下三角形
	$('#upAndDown .up').click(function() {
		var temp = $('input[id="prj_protime"]').val();
		var $ele = $('input[id="prj_protime"]');
		if(temp == '') {
			$ele.val('1');
		} else {
			temp = temp - 0 + 1;
			$ele.val(temp);
		}
	});
	$('#upAndDown .down').click(function() {
		var temp = $('input[id="prj_protime"]').val();
		var $ele = $('input[id="prj_protime"]');
		if(temp == '' || temp == 0) {
			$ele.val('0');
		} else {
			temp = temp - 0 - 1;
			$ele.val(temp);
		}
	});

   //单集多集
	$('.modal-body .btn-md').on('click', function(event) {
		var e = event || window.event;
		var $target = $(e.target);
		if(!$target.hasClass('btn-primary')) {
			$target.addClass('btn-primary');
			$target.next() && $target.next().removeClass('btn-primary');
			$target.prev() && $target.prev().removeClass('btn-primary');
		}
		if($target.hasClass('btn-multi') && !$target.hasClass('btn-public')) {
			$('#btn-multiItem') && $('#btn-multiItem').fadeIn();
		} else {
			$('#btn-multiItem') && $('#btn-multiItem').fadeOut();
		}
	});

	//创建一部影视剧
	$('.btn-create').click(function() {
		var obj = {};
		var name = $('input[id=prj_value]').val().trim(); //名称
		var time = $('input[name="prjtime"]').val(); //时长
		var num = $('input[name="prjnum"]').val(); //集数
		var isMulti = 0; //是否为单集，默认为单集
		var subject = $('input[name="prjsubject"]').val(); //题材

		$('input[name="isMulti"]').each(function(index, ele) {
			if($(this).hasClass('btn-primary')) {
				$(this).val() == '单集' ? isMulti = 0 : isMulti = 1;
			}
		});
		obj.isMulti = isMulti;
		if(isMulti) {
			if(name == '' || time == '' || num == '' || subject == '') {
				alert("请填写影视剧完整信息！");

			}
		} else {
			if(name == '' || time == '' || subject == '') {
				alert("请填写影视剧完整信息！");

			}
		}
		obj.name = name;
		time = parseInt(time);
		obj.time = time;
		num == '' ? num = 1 : num = parseInt(num);
		obj.num = num;
		obj.subject = subject;

        //是否已发表
		var isPublic = 1;
		$('input[name="isPublic"]').each(function(index, ele) {
			if($(this).hasClass('btn-primary')) {
				$(this).val().indexOf('已发表') >= 0 ? isPublic = 1 : isPublic = 0;
			}
		});
		obj.isPublic = isPublic;

        //获取标签
		var arry_label = [];
		$('input[name="prjlabel"]').each(function(index, ele) {
			if($(this).val() !== '') {
				arry_label.push($(this).val());
			}
		});
		obj.label = arry_label.join(';');

		function upload() {
			$.post("/main/", {
				action: 'create',
				prjdata: JSON.stringify(obj),
				async: false,
				cache: false,
				contentType: 'application/json',
				processData: false
			}, function(data) {}).done(function(data) {
				location.reload(true);
			}).fail(function(data, textStatus, xhr) {
				alert("error", data.status + ", " + xhr);
			});
			$('span[id=prj-plus]').hide();
			$('div[id=prj-loading]').show();
		}
        console.log($('.btn .fa-upload').attr('data-load'))
		if($('.btn .fa-upload').attr('data-load') == 'false') {
			if(confirm("尚未上传图片！确定要提交信息吗？")) {
				upload();
			}
		} else {
			upload();
		}
	});

	 //删除一个影视剧
	var prj_id = -1;
    var prj_no = 0;
    $('.btn-warning').click(function() {
         prj_id = $(this).attr('data-id');
         var prjNo = $(this).attr('data-no');
         pri_no = prjNo.split('No')[1];
    });
	$('.btn-delete').click(function() {
	    console.log('1',prj_id,pri_no);
		if(prj_id <= 0) {
			return;
		}
		$.post("/main/", {
			action: 'delete',
			idAndno: JSON.stringify({
				pri_id: prj_id,
				pri_no: pri_no
			}),
			async: false,
			cache: false,
			contentType: 'application/json',
			processData: false
		}, function(data) {}).done(function(data) {
			location.reload(true);
		}).fail(function(data, textStatus, xhr) {
			alert("error", data.status + ", " + xhr);
		});
		prj_id = -1;
	});
});