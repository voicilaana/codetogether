// $(window).resize(function() {
//     $('#textareaForm').height($(window).height());
// });

// $(window).trigger('resize');

var h = window.innerHeight;
console.log(h);

document.getElementById("textareaForm").style.height = h - 50 + "px";
