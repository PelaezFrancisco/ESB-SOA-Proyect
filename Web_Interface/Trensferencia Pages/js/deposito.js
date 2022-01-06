function depositar() {
    var numeroCuenta = document.getElementById("numCuenta").value;
    var montoCuenta = document.getElementById("monto").value;
    var entidadBancaria = document.getElementById("seleccion").value;

    console.log(numeroCuenta)

    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location='index.html';
        }
    };
    /*
    maux=parseFloat(montoCuenta);
    maux=maux/2;
    montoCuenta=maux.toString();
    */
    var mimeType = "text/plain";
    xmlhttp.open("PUT", "http://ec2-3-83-158-24.compute-1.amazonaws.com:9568/deposito/"+numeroCuenta+"/"+montoCuenta, true);
    xmlhttp.setRequestHeader('Content-Type', mimeType);
    xmlhttp.send();

    return false;
}


