function changePage(src) {
    window.location.href = src
}

//微信公众号appid
var appid = "wx8ca1ef28740b0106";
var key_customer_id = appid + "_customer_id";
var key_token = appid + "_token";

//封装http请求头
sendAuthentication = function(xhr) {
    var user = localStorage.getItem(key_token); // your actual username
    var pass = "mypassword"; // your actual password
    var token = user.concat(":", pass);
    xhr.setRequestHeader('Authorization', ("Basic ".concat(btoa(token))));
}

//js 深度拷贝
function deepCopy(obj) {
    var cloneObject = {};
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            cloneObject[key] = obj[key];
        }
    }
    return cloneObject;
}

// 计算 yyyy-MM-dd n个月后 
function addmulMonth(dtstr, n) {
    var d = new Date(dtstr)
    d.setMonth(d.getMonth() + n);
    return d.Format("yyyy-MM-dd");
}

//GMT时间转普通时间
function GMTToStr(time) {
    let date = new Date(time)
    var m = date.getMonth();
    if (m + 1 < 10) {
        m = "0" + (m + 1);
    }
    var d = date.getDate();
    if (d < 10) {
        d = "0" + d;
    }
    let Str = date.getFullYear() + '-' +
        (m) + '-' +
        d // +
        //date.getHours() + ':' +
        //date.getMinutes() + ':' +
        //date.getSeconds()
    return Str
}

//js Date 扩展
Date.prototype.Format = function(fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}