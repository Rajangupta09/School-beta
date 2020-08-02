
    let tmp = document.getElementById("class-btn");
    tmp.onclick = function(e){
        e.preventDefault();
        RI();
    }
    
function RI() {
    let str = document.getElementById("class-input").value;
    let str_section = document.getElementById("section-input").value;
    str1 = str.toUpperCase();
    let num = char_to_int(str1.charAt(0));
    if(str.length < 1){
        const invalid = document.getElementsByClassName("invalid-feedback");
        for(i=0;i<invalid.length;i++)
            invalid[i].style.display = "block";
        console.log("document.getElementsByClassName('invalid-feedback')");
    }
    else{
    let pre, curr;
    for(let i = 1; i < str1.length; i++){
    curr = char_to_int(str1.charAt(i));
    pre = char_to_int(str1.charAt(i-1));
    if(curr <= pre){
    num += curr;
    } else {
    num = num - pre*2 + curr;
    }
    }
    document.getElementById("class-input").value = num;
    section = str_section.toUpperCase();
    document.getElementById("section-input").value = section;
    document.getElementById("class-form").submit();
    }
};



function char_to_int(c){
switch (c){
case 'I': return 1;
case 'V': return 5;
case 'X': return 10;
case 'L': return 50;
case 'C': return 100;
case 'D': return 500;
case 'M': return 1000;
default: return 0;
}
}
