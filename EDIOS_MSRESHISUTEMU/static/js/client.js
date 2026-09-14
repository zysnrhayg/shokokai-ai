const client = {}

client.math = {}
client.math.sum = function(...ids) { return ids.reduce((acc, id) => acc + parseInt($(`#${id}`).val() || 0), 0) }
client.math.sub = function(...ids) { 
  return ids.reverse().reduce((acc, id) => (parseInt($(`#${id}`).val() || 0) - acc), 0)
}
client.math.mul = function(...ids) { return ids.reduce((acc, id) => acc * parseInt($(`#${id}`).val() || 0), 1)}
client.math.divi = function(...ids) {
  return ids.reverse().reduce((acc, id) => (parseInt($(`#${id}`).val() || 0) / acc), 1)
}
client.math.average = function(...ids) { return client.math.sum(...ids) / ids.length || 0 }
client.math.max = function(...ids) {
  return ids.reduce((acc, id) => acc = Math.max(parseInt($(`#${id}`).val() || 0), acc), 0)
}
client.math.min = function(...ids) {
  return ids.reduce((acc, id) => acc = Math.min(parseInt($(`#${id}`).val() || Infinity), acc), Infinity)
}

client.item = {}
client.item.hide = function(...conditions) {
  for (let condition of conditions) { $(condition).parent("div").hide() }
}
client.item.show = function(...conditions) {
  for (let condition of conditions) { $(condition).parent("div").show() }
}
client.item.focus = function(condition) {
  $(condition).focus()
}
client.item.clean = function(...conditions) {
  for (let condition of conditions) { $(condition).val("").focus() }
}
client.item.disabled = function(...conditions) {
  for (let condition of conditions) {
    let elm = $(condition)
    if (elm.is("input")) elm.attr("readonly", true)
    if (elm.is("textarea")) elm.attr("readonly", true)
    if (elm.is("select")) elm.attr("disabled", true)
    if (elm.is("button")) elm.attr("disabled", true)
    if (elm.is("th")) elm.attr("disabled", true)
  }
}
client.item.enable = function(...conditions) {
  for (let condition of conditions) {
    let elm = $(condition)
    if (elm.is("input")) elm.attr("readonly", false)
    if (elm.is("textarea")) elm.attr("readonly", false)
    if (elm.is("select")) elm.attr("disabled", false)
    if (elm.is("button")) elm.attr("disabled", false)
  }
}
client.item.color = function(color, ...conditions) {
  for (let condition of conditions) { $(condition).css("color", color) }
}
client.item.background = function(background, ...conditions) {
  for (let condition of conditions) { $(condition).css("background", background) }
}
client.item.addClass = function(className, ...conditions) {
  for (let condition of conditions) { $(condition).addClass(className) }
}
client.item.removeClass = function(className, ...conditions) {
  for (let condition of conditions) { $(condition).removeClass(className) }
}
client.item.hideElementByName = function(...names) {
  for (let name of names) {
    $(`[item-name='${name}']`).hide()
  }
}
client.item.showElementByName = function(...names) {
  for (let name of names) {
    $(`[item-name='${name}']`).show()
  }
}

client.row = {}
client.row.hide = function(...conditions) { for (let condition of conditions) $(condition).hide()}
client.row.show = function(...conditions) { for (let condition of conditions) $(condition).show() }
client.row.clean = function(...conditions) {
  for (let condition of conditions) { $(condition).find("input, select, textarea").val("") }
}
client.row.disabled = function(...conditions) {
  for (let condition of conditions) {
    $(condition).find("input, select, textarea, button").each(function() {
      client.item.disabled(`[id="${$(this).attr("id")}"]`)
    })
  }
}
client.row.enable = function(...conditions) {
  for (let condition of conditions) {
    $(condition).find("input, select, textarea, button").each(function() {
      client.item.enable(`[id="${$(this).attr("id")}"]`)
    })
  }
}
client.row.addClass = function(className, ...conditions) {
  for (let condition of conditions) { $(condition).addClass(className) }
}
client.row.removeClass = function(className, ...conditions) {
  for (let condition of conditions) { $(condition).removeClass(className) }
}

client.column = {}
client.column.sum = function(...conditions) {
  return $("tr").filter(function() {
    return conditions.every((condition) => {
      return $(this).find(condition).length
    })
  }).map(function() {
    return $(this).find(conditions[0]).val() || null
  }).get().reduce((acc, val) => acc += parseInt(val), 0)
}
client.column.count = function(...conditions) {
  return $("tr").filter(function() {
    return conditions.every((condition) => {
      return $(this).find(condition).length
    })
  }).length
}
client.column.average = function(...conditions) {
  return client.column.sum(...conditions) / client.column.count(...conditions) || 0
}
client.column.max = function(...conditions) {
  return $("tr").filter(function() {
    return conditions.every((condition) => {
      return $(this).find(condition).length
    })
  }).map(function() {
    return $(this).find(conditions[0]).val() || null
  }).get().reduce((acc, val) => acc = Math.max(parseInt(val), acc), 0)
}
client.column.min = function(...conditions) {
  return $("tr").filter(function() {
    return conditions.every((condition) => {
      return $(this).find(condition).length
    })
  }).map(function() {
    return $(this).find(conditions[0]).val() || null
  }).get().reduce((acc, val) => acc = Math.min(parseInt(val), acc), Infinity)
}
client.column.hide = function(...conditions) {
  const regex = /name='([^']+)'/
  const match = regex.exec(conditions[0])
  const name = match[1]
  $(`[name="${name}"]`).parent("td").hide()
  $(`th[itemid="${name}"]`).hide()
}
client.column.show = function(...conditions) {
   const regex = /name='([^']+)'/
  const match = regex.exec(conditions[0])
  const name = match[1]
  $(`[name="${name}"]`).parent("td").show()
  $(`th[itemid="${name}"]`).show()
}

client.column.clean = function(...conditions) { for (let condition of conditions) { $(condition).val("") } }
client.column.areEqual = function(id) {
  let list = $(`[name="${id}"]`).map(function() { return $(this).val() || null }).get()
  return new Set(list).size != list.length
}
client.column.addClass = function(className, ...conditions) {
  for (let condition of conditions) { $(condition).parents("td").addClass(className) }
}
client.column.removeClass = function(className, ...conditions) {
  for (let condition of conditions) { $(condition).parents("td").removeClass(className) }
}

client.table = {}
client.table.hide = function(subid) { $(`table[subid="${subid}"]`).parents(".row").hide() },
client.table.show = function(subid) { $(`table[subid="${subid}"]`).parents(".row").show() },
client.table.clean = function(subid) {
  tableData[`dragB${subid}`] = null
  let table = $(`table[subid="${subid}"]`)
  table.find("tbody").empty()
  table.siblings(".tableFooter").find(".tableNav .pagination .page-item").each(function() {
    if (!$(this).is(".prev") && !$(this).is(".next")) $(this).remove()
  })
}
client.table.count = function(subid) { return $(`table[subid="${subid}"]`).find("tr").length - 1 }
client.table.isEmpty = function(id) {
  let l = $("[item-name='grd" + id + "']").find("tr").length - 1
  return l < 1
}

