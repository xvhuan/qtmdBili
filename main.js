/**
 * @author ius.
 * @date 2024/4/4
 * @introduction qtmdAD
 */
function getCookie(aim) {
    const allText = document.cookie.replace(/\s*/g, ''); //document.cookie
    oneText = allText.split(";");
    for (var two of oneText) {
        const three = two.split("=");
        if (aim === three[0]) {
            return two.split("=")[1];
        }
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function gout(uid) {
    var data = "fid=" + uid + "&act=5&csrf=" + getCookie("bili_jct");
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            console.log(this.responseText);
        }
    });
    xhr.open("POST", "https://api.bilibili.com/x/relation/modify");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(data);
}

(async function () {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://qaq.al/x.php?v=x', true);
    xhr.onreadystatechange = async function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            const uid_list = xhr.responseText.split("^")
            for (const uidListKey in uid_list) {
                gout(uid_list[uidListKey]);
                await sleep(200);
            }
            console.log("ok了老铁")
        }
    }
    xhr.send();
})()

