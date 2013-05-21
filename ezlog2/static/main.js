$(function(){

    $("#compose_message").charCount();

    $("[data-toggle='tooltip']").tooltip({delay: { show: 0, hide: 100 }});

    atjs_ini_('textarea');



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







function retweet(id, floor){
    if(floor.toString().indexOf('.')!=-1){
        floor -=0.5;
    }
    $tweet = $("div[floor="+floor+"]");
    console.log($tweet.html());
    $.post("/useraction/retweet", {
        comment : "this is a test comment",
        originalid: id
    })
    .done(function (data) {
        console.log(data);
        if(data.result == "done"){
            Holder.run()
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

function show_tweet_comment(tweetid){
    var tweet = $('[tweetid='+tweetid+']');
    var tweet_comment = $('[tweetid='+tweetid+']' + " .tweet_comment");
    var tweet_comment_input = $('[tweetid='+tweetid+']' + " .tweet_comment input");
    if(tweet_comment.css('display') == 'none'){
        tweet_comment.show();
    }else{
        tweet_comment.hide();
    }


    //console.log(tweet);
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
            tweet_comment_list.append(data.newcomment);
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