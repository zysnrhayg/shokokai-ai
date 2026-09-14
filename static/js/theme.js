function loadTheme() {
  let theme = localStorage.getItem("theme") || "light"
  if (theme == "light") {
    const elm = document.getElementById("css_drak")
    if (elm) elm.remove()
  } else {
    let style = document.createElement("style")
    style.id = "css_drak"
    style.rel = "stylesheet"
    style.type = "text/css"
    style.innerHTML  = ":root { transition: filter .3s; filter: invert(0.9); } video, img, svg { filter: invert(1); }"
    document.head.appendChild(style)
  }
}
loadTheme()