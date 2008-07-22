
function translationbrowser_openBrowser(path, at_url, type) {
    atrefpopup = window.open(path+'/translationbrowser_popup?at_type='+type+'&at_url='+at_url, 'translationbrowser_popup', 'toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=500,height=550');
}

function translationbrowser_setReference(uid, label) {
    element=document.getElementById('link_content')
    element_label=document.getElementById('link_content_label')
    element.value=uid
    element_label.value=label
}
