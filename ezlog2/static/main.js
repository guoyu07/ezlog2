$(function(){

    $("#compose_message").charCount();

    $("[data-toggle='tooltip']").tooltip({delay: { show: 0, hide: 100 }});

    atjs_ini_('textarea');
    atjs_ini_('input');



});


function atjs_ini_(node){
    var at_template = "<li data-value='${nickname}'><img src='${avatar}' height='20' width='20'/> ${nickname} <small>(${id})</small> </li>";

    $(node).atwho({
        at:"@",
        data : "/api/account/username",
        search_key : "nickname",
        callbacks : {
            data_refactor : function (data) {
                return data.users;
            },
            remote_filter: function(query, callback){
                $.post("/api/account/username", {
                    startwith : query,
                })
                .done(function (data) {
                    callback(data.users);
                });
            },

        },
        tpl : at_template
    });
}


function read_notify(notifyid){

  $.post("/useraction/read_notify_message", {
      messageid : notifyid
  })
  .done(function (data) {
      if(data.rcode == 200){
        $('[notifyid='+notifyid+']').hide();
      
      }
  });
}

function pm_invoke(receiverid){
  var $pm_input     = $("#_private_message_input");
  var $content      = $("#_pm_content",$pm_input);
  var $sender_btn   = $("#_pm_sender",$pm_input);
  $sender_btn.off().on("click" ,function(e){
    pm_send(receiverid,$content.val());
  });
  $content.val("");
}

function pm_send(receiverid,content){
    $.post("/useraction/private_message", {
        content : content,
        receiverid: receiverid
    })
    .done(function (data) {
        console.log(data);
        if(data.rcode == 200){
          $('#_private_message_input').modal('hide');
        }
    });
}

function read_pm(pmid,nickname,content){
  var $view   = $("#_private_message_view");
  var $title  = $("#_pm_title",$view);
  var $content= $("#_pm_content",$view);
  $title.html("来自"+nickname+"的私信");
  $content.html(content);
  
  $.post("/useraction/read_private_message", {
      pmid : pmid
  })
  .done(function (data) {
      if(data.rcode == 200){
      
      }
  });
}

function delete_pm(pmid){
  $.post("/useraction/delete_private_message", {
      pmid : pmid
  })
  .done(function (data) {
      if(data.rcode == 200){
        $('[private_messageid='+pmid+']').hide();
      }
  });
}

function retweeet_trigger(tweetid){
  var tweet = $('[tweetid='+tweetid+']');

  var retweet_input = $("#_retweet_input");
  var sender_btn    = $("#_retweet_sender",retweet_input);
  var $content      = $("#_retweet_content",retweet_input);
  if(tweet.parent().hasClass("retweet")){
    var $comment    = $(".retweet_comment",tweet);
    var $poster     = $(".retweet_poster",tweet);
    $content.val("//"+$poster.html().trim()+": "+$comment.html().trim());
  }else{
    $content.val("");
  }
  
  sender_btn.off().on("click",function(e){
    retweet(tweetid,$content.val());
  });
}


function retweet(id, comment){
    $.post("/useraction/retweet", {
        comment : comment,
        originalid: id
    })
    .done(function (data) {
        console.log(data);
        if(data.result == "done"){
            $('#_retweet_input').modal('hide');
            $('#weibo_list').prepend(data.newtweet);
            var notify = $('#sender_notify');
            notify.addClass('label-success');
            notify.html("转发成功");
            notify.show();
            notify.fadeOut(3000);
            Holder.run();
        }
    });

}


function toggle_follow(followeduserid, node){
     $.post("/useraction/toggle_follow", {
        followeduserid : followeduserid
    }).done(function (data) {
        console.log(data);
        if(data.result == "done"){
            var content = $(node).html();
            if(content == "关注一下"){
                $(node).html("取消关注");
            }else{
                $(node).html("关注一下");
            }
        }

    });

}


function tweet_send_acion(){
    var button = $("#tweet_send_button");
    if(button.hasClass('disabled')){
        alert('已经超出字数, 不能发送');
        return ;
    }

    if($('#compose_message').val() == ""){
        alert('不能发送空内容');
        return ;
    }

    $.post("/useraction/tweet", {
        content : $('#compose_message').val()
    })
    .done(function (data) {
        if(data.result == "done"){
            var notify = $('#sender_notify');
            notify.addClass('label-success');
            notify.html("发送成功");
            notify.show();
            notify.fadeOut(3000);
            $('#weibo_list').prepend(data.newtweet);
            $('#compose_message').val("");
            $('.counter').html("剩余字数 140");
            localStorage.removeItem('publisherTop_word');
            Holder.run()
        }
    });
}

var show_tweet_comment = (function(tweetid){
    var displayed = false;
    return function(tweetid){
      var tweet = $('[tweetid='+tweetid+']');
      var tweet_comment = $(".tweet_comment",tweet);
      if(!displayed){
          tweet_comment.show();
      }else{
          tweet_comment.hide();
      }
      displayed =!displayed;
    }
})();


function comment_comment(node,nickname){
  var $this     = $(node);
  var $comment  = $this.parent().parent().parent().parent();
  var $input    = $("input",$comment);
  $input.val("@"+nickname+" ");

}

function send_tweet_comment(tweetid){
    var tweet_comment_input = $('[tweetid='+tweetid+']' + " .tweet_comment input");
    var tweet_comment_list = $('[tweetid='+tweetid+']' + " .tweet_comment");

    if(tweet_comment_input.val() == ""){
        alert('不能发送空内容');
        return ;
    }

    $.post("/useraction/comment", {
        content : tweet_comment_input.val(),
        tweetid: tweetid
    })
    .done(function (data) {
        console.log(data);
        tweet_comment_input.val("");
        if(data.result == "done"){
            $(".tweet_comment_list",tweet_comment_list).prepend(data.newcomment);
            Holder.run()
        }
    });

}


function getStringLength(str){
    return Math.floor(str.replace(/[^\x00-\xff]/g,"**").length / 2);
}




//helper class


//http://stackoverflow.com/a/2855946
function is_valid_email_address(emailAddress) {
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
};

(function($){
    $.mlp = {x:0,y:0}; // Mouse Last Position
    function documentHandler(){
        var $current = this === document ? $(this) : $(this).contents();
        $current.mousemove(function(e){jQuery.mlp = {x:e.pageX,y:e.pageY}});
        $current.find("iframe").load(documentHandler);
    }
    $(documentHandler);
    $.fn.ismouseover = function(overThis) {
        var result = false;
        this.eq(0).each(function() {
                var $current = $(this).is("iframe") ? $(this).contents().find("body") : $(this);
                var offset = $current.offset();
                result =    offset.left<=$.mlp.x && offset.left + $current.outerWidth() > $.mlp.x &&
                            offset.top<=$.mlp.y && offset.top + $current.outerHeight() > $.mlp.y;
        });
        return result;
    };
})(jQuery);

function refresh(){

}