function passCheck(){

    var password=document.getElementById('psw');
    var vpassword=document.getElementById('pswrepeat');

    if (password.value != vpassword.value)
    {
        document.getElementById('registerbtn').disable = true;
    }
    else
    {
        document.getElementById("registerbtn").disable = false;
    }

}