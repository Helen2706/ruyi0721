$(function(){
    var oldLen=$('.scene tbody').find('tr').length;
    var oldVal=[];
    $('.scene tbody input').each(function(i,item){
        var item=$(item);
        oldVal[i]=item.val();
    });
//回车增加一行,delete删除
    $('.row').undelegate('.projectSceneID','keydown').delegate('.projectSceneID','keydown',function(event){
       var e=event || window.event;
       var $target=$(e.target);
       var $parentsEle=$target.parents('tr');
       if(e && e.keyCode==13){
           var $appendEle=$parentsEle.clone(true);
           $appendEle.find('.isAdd').val('1');
           $parentsEle.after($appendEle);
           $target.blur();
           $parentsEle.next().find('.projectSceneID').focus();
       }
       if(e && e.keyCode==46){
          if($parentsEle.find('.isAdd').val()=='0'){
               $parentsEle.find('.isDel').val('true');
               $parentsEle.hide();
               $('form[name=formUpdate]').submit();
          }else{
                $parentsEle.empty();
              }
         }
    });

//提交表单（默认回车触发，已经阻止）
    $('#save').on('click',function(){
           var res=true;
           var newLen=$('.scene tbody').find('tr').length;
           if(oldLen==newLen){
               var newVal=[];
               $('.scene tbody input').each(function(i,item){
                   var item=$(item);
                   newVal[i]=item.val();
               });
              if(oldVal.toString()!=newVal.toString()){
                 res=false;
              }
           }
           if((oldLen!=newLen) || (!res)){
               $('form[name=formUpdate]').submit();
           }

    });

//场景创建
     $('#create').on('click',function(){
            $('form[name=formCreate]').submit();
    });
});
