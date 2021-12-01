function transferir() {

    var bancoEmisor = document.getElementById("bancoEmisor").value;
    var cuentaEmisor = document.getElementById("cuentaEmisor").value;
    var monto = document.getElementById("monto").value;
    var bancoReceptor = document.getElementById("bancoReceptor").value;
    var cuentaReceptor = document.getElementById("cuentaReceptor").value;

    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location='confirmacion.html';
        }
    };
    var mimeType = "text/plain";
    /*
    maux=parseFloat(monto);
    maux=maux/2;
    monto=maux.toString();
    */
    xmlhttp.open("PUT", "http://localhost:8099/esb_proyect/transferencia/" + cuentaEmisor + "/" + bancoEmisor + "/" + monto + "/" + cuentaReceptor + "/" + bancoReceptor, true);
    xmlhttp.setRequestHeader('Content-Type', mimeType);
    xmlhttp.send();

    return false;
}