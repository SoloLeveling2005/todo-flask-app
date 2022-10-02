function change_task() {
    document.getElementById("info").style.cssText = `
        display:none;
    `;
    document.getElementById("change_info").style.cssText = `
        display:block;
    `;

    document.getElementById("change").style.cssText = `
        display:none;
    `;
    document.getElementById("cancel_change").style.cssText = `
        display:block;
    `;
}

function cancel_change_task() {
    document.getElementById("change_info").style.cssText = `
        display:none;
    `;
    document.getElementById("info").style.cssText = `
        display:block;
    `;

    document.getElementById("change").style.cssText = `
        display:block;
    `;
    document.getElementById("cancel_change").style.cssText = `
        display:none;
    `;
}