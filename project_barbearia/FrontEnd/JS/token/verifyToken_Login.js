let tokenChecked = false;
async function checkTokenValidityLogin() {
    const token = localStorage.getItem("token"); 
    if (tokenChecked) {
        return; // Se a função já foi chamada, retorna sem fazer nada
    }
    const options = {
    method: 'GET',
    url: 'http://localhost:8000/verificar-token/',
    params: {token: token},
    headers: {'User-Agent': 'insomnia/9.1.0'}
    };
    tokenChecked = true;
    axios.request(options).then(function (response) {
    console.log(response.data);
    if(response.data.status == "Token válido"){
        alert("LOGIN FEITO COM SUCESSO!");
    }else{
        alert("ERRO NA AUTENTICAÇÂO TENTE NOVAMENTE")
        window.location.href("http:/FrontEnd/HTML/pagina_cliente.html")
    }
    }).catch(function (error) {
    console.error(error);
    });
}

function decodeJWT(token) {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(atob(base64).split("").map(function(c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(""));

    return JSON.parse(jsonPayload);
}

