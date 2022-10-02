function go_to_auth() {
    document.getElementById("login").style.cssText = `
        display:none;
    `;
    document.getElementById("auth").style.cssText = `
        display:flex;
    `;
}

function go_to_login() {
    document.getElementById("auth").style.cssText = `
        display:none;
    `;
    document.getElementById("login").style.cssText = `
        display:flex;
    `;
}

