//HTTP通信用共通関数
/* Get XmlHttpRequest */
var errmsg = "";
var isUser = false;
var urlAddEdit = "/dev/ajax/XRAddEdit.jsp";
var urlNewAddEdit = "/dev/ajax/XRNewAddEdit.jsp";
var urlDel = "/dev/ajax/XRDel.jsp";
var urlControl = "/dev/ajax/XRControl.jsp";
var urlRunSearch = "/dev/ajax/XRRunSearch.jsp";
var XRRunScript = "/dev/ajax/XRRunScript.jsp";
var XRRunJson = "/dev/ajax/XRRunJson.jsp";

var wsProtocal = location.protocol == 'http:'? 'ws://' : 'wss://';
var wsViewlogfile=wsProtocal+location.host+'/w/viewlogfile?tag=';
var wsCreate=wsProtocal+location.host+'/w/progress?tag=FuncProgress.func';
var wsImportData=wsProtocal+location.host+'/w/importdata?tag=';
var wsCompareEnvDif=wsProtocal+location.host+'/w/compareenvdif?tag=';
var urlUserDelete = "/user/ajaxUser/XRDel.jsp";
var urlUserEdit = "/user/ajaxUser/XRAddEdit.jsp";
var urlUserSearch = "/user/ajaxUser/XRRunSearch.jsp";
var urlUserScript = "/user/ajaxUser/XRRunScript.jsp";
var urlUserScriptFixUser = "/user/ajaxUser/XRRunScriptFixUser.jsp";
var urlUserChart = "/s/Chart";

var urlAdminAddEdit = "/admin/XRAdminAddEdit.jsp";
ua=navigator.userAgent.toLowerCase();
var is_MSIE = (ua.indexOf('msie') > -1) && (ua.indexOf('opera') == -1);
var is_IE11 = (ua.indexOf('trident/7') > -1);
var is_IE = is_MSIE || is_IE11;
var is_Edge = (ua.indexOf('edge') > -1);
//Google Chrome
var is_Chrome = (ua.indexOf('chrome') > -1) && (ua.indexOf('edge') == -1);
// Firefox
var is_Firefox = (ua.indexOf('firefox') > -1);
// Safari
var is_safari = (ua.indexOf('safari') > -1) && (ua.indexOf('chrome') == -1);
// Opera
var is_Opera = (ua.indexOf('opera') > -1);
//iPhone
var is_iPhone = (ua.indexOf('iphone') > -1);
// iPad
var is_iPad = (ua.indexOf('ipad') > -1);
// Android
var is_Android = (ua.indexOf('android') > -1) && (ua.indexOf('mobile') > -1);
// Android Tablet
var is_AndroidTablet = (ua.indexOf('android') > -1) && (ua.indexOf('mobile') == -1);
var isSplit = new RegExp(/\#{12}\r\n/);
function createXmlHttpRequestObj() {
	var XMLhttpObject = null;
	try {
		XMLhttpObject = new XMLHttpRequest();
	} catch (e) {
		try {
			XMLhttpObject = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e) {
			try {
				XMLhttpObject = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (e) {
				return null;
			}
		}
	}
	return XMLhttpObject;
}

function createXMLHttpRequest(cbFunc) {
	var XMLhttpObject = createXmlHttpRequestObj();
	if (XMLhttpObject) {
		XMLhttpObject.onreadystatechange = cbFunc;
	}
	return XMLhttpObject;
}

/* Error Dealing */
function dealError() {
	if (httpObj.readyState == 4) {
		if (httpObj.status == 404) {
			return jQuery.i18n.prop("common.err00005");
		} else if (httpObj.status == 401) {
			return jQuery.i18n.prop("common.err00006");
		} else if (httpObj.status == 403) {
			return jQuery.i18n.prop("common.err00007");
		} else if (httpObj.status == 500) {
			return jQuery.i18n.prop("common.err00008");
		}
		return jQuery.i18n.prop("common.err00009");
	}
}
/* get all items in level 0 and items in selected grid row */
function setSendDataWithSelectedGridRow(frm) {
	var txt = new String();
	var radiomNoVal = new Map();
	var radiomWithVal = new Map();
	var tp = '', item;
	if (frm=="")
		return "";
	var properties = "";
	$("form[name=form1] input,form[name=form1] select").not("table.datagrid input,table.datagrid select").each(function() {
		var element = $(this).get(0);
		if (element.name != "" && element.name != undefined) {
			var saasforceAttributes = SF.makeItemAttributesForSendData(element);
			if (saasforceAttributes != "") {
				properties += element.name;
				properties += "=";
				properties += saasforceAttributes;
				properties += ",";
			}
		}
		if (element.type == "checkbox" && (element.checked == false)) {
			txt += "&";
			txt += element.name;
			txt += "=0";
		} else if (element.type == "radio"
						&& (element.checked == false
					|| element.value == ""
					|| element.value == null)) {
			radiomNoVal.set(element.name, "1");
		} else if (element.tagName == "SELECT") {
			var selectValue = element.value;
			selectValue = $.trim(selectValue);
			if (selectValue == null || selectValue == "") {
				if ($("#s2id_" + element.id).length > 0) {
					selectValue = $.trim($("span.select2-chosen", $("#s2id_" + element.id)).text());
					if (!selectValue) {
						selectValue = "";
					}
					txt += "&";
					txt += element.name + "_new_flg";
					txt += "=1";
				}
			}
			txt += "&";
			txt += element.name;
			txt += "=";
			txt += encodeURIComponent(selectValue);
		} else {
			if (element.name == ""||element.name==undefined) {
			} else {
				txt += "&";
				item = element.name;
				txt += item;
				txt += "=";
				txt += encodeURIComponent(element.value);
				if (element.type == "radio") {
					radiomWithVal.set(item, "1");
				}
			}
		}
	});
	$("form[name=form1] table.datagrid input[type=hidden][id^=Grid][id*=flg][value!='']").closest("tr").find("select,input[type=text],input[type=checkbox],input[type=radio],input[type=hidden]").each(function() {
		var element = $(this).get(0);
		if (element.name != "" && element.name != undefined) {
			var saasforceAttributes = SF.makeItemAttributesForSendData(element);
			if (saasforceAttributes != "") {
				properties += element.name;
				properties += "=";
				properties += saasforceAttributes;
				properties += ",";
			}
		}
		if (element.type == "checkbox" && (element.checked == false)) {
			txt += "&";
			txt += element.name;
			txt += "=0";
		} else if (element.type == "radio"
						&& (element.checked == false
					|| element.value == ""
					|| element.value == null)) {
			radiomNoVal.set(element.name, "1");
		} else if (element.tagName == "SELECT") {
			var selectValue = element.value;
			selectValue = $.trim(selectValue);
			if (selectValue == null || selectValue == "") {
				if ($("#s2id_" + element.id).length > 0) {
					selectValue = $.trim($("span.select2-chosen", $("#s2id_" + element.id)).text());
					if (!selectValue) {
						selectValue = "";
					}
					txt += "&";
					txt += element.name + "_new_flg";
					txt += "=1";
				}
			}
			txt += "&";
			txt += element.name;
			txt += "=";
			txt += encodeURIComponent(selectValue);
		} else {
			if (element.name == ""||element.name==undefined) {
			} else {
				txt += "&";
				item = element.name;
				txt += item;
				txt += "=";
				txt += encodeURIComponent(element.value);
				if (element.type == "radio") {
					radiomWithVal.set(item, "1");
				}
			}
		}
	});
	for (let sp of radiomNoVal) {
		if (!radiomWithVal.get(sp[0])) {
			txt += "&";
			txt += sp[0];
			txt += "=";
			txt += "";
		}
	}
	var dialogIDs = "";
	// ダイアログの中のinput項目値を取得
	$("div.dialogDiv").each(function () {
		dialogIDs += $(this).attr("id") + ",";
	});

	if (dialogIDs != "") {
		// 最後のコンマを切り捨てる
		dialogIDs = dialogIDs.substring(0, dialogIDs.length - 1);
		txt += "&" + setSendDivData(dialogIDs);
	}

	txt += "&saasforceProperties=";

	txt += encodeURIComponent(properties);
	if (txt.length > 0) {
		txt = txt.substring(1);
	}
	return txt;
}
/* Get Send Data from Form */
function setSendData(frm) {
	var txt = new String();
	var tp = '', item;
	var radiomNoVal = new Map();
	var radiomWithVal = new Map();
	if (frm=="")
		return "";
	var properties = "";
	for ( var i = 0; i < frm.elements.length; i++) {
		if (frm.elements[i].name != "" && frm.elements[i].name != undefined) {
			var saasforceAttributes = SF.makeItemAttributesForSendData(frm.elements[i]);
			if (saasforceAttributes != "") {
				properties += frm.elements[i].name;
				properties += "=";
				properties += saasforceAttributes;
				properties += ",";
			}
		}
		if (frm.elements[i].type == "checkbox" && (frm.elements[i].checked == false)) {
			txt += "&";
			txt += frm.elements[i].name;
			txt += "=0";
		} else if (frm.elements[i].type == "radio"
						&& (frm.elements[i].checked == false
					|| frm.elements[i].value == ""
					|| frm.elements[i].value == null)) {
			radiomNoVal.set(frm.elements[i].name, "1");
		} else if (frm.elements[i].tagName == "SELECT") {
			var selectValue = frm.elements[i].value;
			selectValue = $.trim(selectValue);
			if (selectValue == null || selectValue == "") {
				if ($("#s2id_" + frm.elements[i].id).length > 0) {
					selectValue = $.trim($("span.select2-chosen", $("#s2id_" + frm.elements[i].id)).text());
					if (!selectValue) {
						selectValue = "";
					}
					txt += "&";
					txt += frm.elements[i].name + "_new_flg";
					txt += "=1";
				}
			}
			txt += "&";
			txt += frm.elements[i].name;
			txt += "=";
			txt += encodeURIComponent(selectValue);
		} else {
			if (frm.elements[i].name == ""||frm.elements[i].name==undefined) {
			} else {
				txt += "&";
				item = frm.elements[i].name;
				if (item.indexOf("_") > -1) {
					var oriitem = item.split("_")[0];
					var line = Number(item.split("_")[1]) -1;
				}
				txt += item;
				txt += "=";
				txt += encodeURIComponent(frm.elements[i].value);
				if (frm.elements[i].type == "radio") {
					radiomWithVal.set(item, "1");
				}
			}
		}
	}
	for (let sp of radiomNoVal) {
		if (!radiomWithVal.get(sp[0])) {
			txt += "&";
			txt += sp[0];
			txt += "=";
			txt += "";
		}
	}

	var dialogIDs = "";
	// ダイアログの中のinput項目値を取得
	$("div.dialogDiv").each(function () {
		dialogIDs += $(this).attr("id") + ",";
	});

	if (dialogIDs != "") {
		// 最後のコンマを切り捨てる
		dialogIDs = dialogIDs.substring(0, dialogIDs.length - 1);
		txt += "&" + setSendDivData(dialogIDs);
	}

	txt += "&saasforceProperties=";

	txt += encodeURIComponent(properties);
	if (txt.length > 0) {
		txt = txt.substring(1);
	}
	return txt;
}
/* Get Send Data from Form */
function setSendJsonData(frm) {
	var json = {};
	var txt = new String();
	var tp = '';
	if (frm=="")
		return json;
	for ( var i = 0; i < frm.elements.length; i++) {
		if (frm.elements[i].name != "" && frm.elements[i].name != undefined) {
			var saasforceAttributes = SF.makeItemAttributesForSendData(frm.elements[i]);
			if (saasforceAttributes != "") {
				json['wfpage_' + frm.elements[i].name] = saasforceAttributes;
			}
		}
		if (frm.elements[i].type == "checkbox" && (frm.elements[i].checked == false)) {
			json['wfpage_' + frm.elements[i].name] = "0";
		} else if (frm.elements[i].type == "radio"
						&& (frm.elements[i].checked == false
					|| frm.elements[i].value == ""
					|| frm.elements[i].value == null)) {
		} else if (frm.elements[i].tagName == "SELECT") {
			var selectValue = frm.elements[i].value;
			selectValue = $.trim(selectValue);
			if (selectValue == null || selectValue == "") {
				if ($("#s2id_" + frm.elements[i].id).length > 0) {
					selectValue = $.trim($("span.select2-chosen", $("#s2id_" + frm.elements[i].id)).text());
					if (!selectValue) {
						selectValue = "";
					}
					json['wfpage_' + frm.elements[i].name + "_new_flg"] = "1";
				}
			}
			json['wfpage_' + frm.elements[i].name] = (selectValue);
		} else {
			if (frm.elements[i].name == ""||frm.elements[i].name==undefined) {
			} else {
				json['wfpage_' + frm.elements[i].name] = (frm.elements[i].value);
			}
		}
	}

	return json;
}
function getObjValueWithDiv(itemid, div) {
	div = "#"+div;
	if ($("#"+itemid,$(div)).get(0).type.toLowerCase() == "checkbox"
			&& $("#"+itemid,$(div)).get(0).checked == false) {
		return "0";
	} else if ($("#"+itemid,$(div)).get(0).type.toLowerCase() == "radio") {
		return encodeURIComponent(getRadioValueWithDiv(itemid, $(div)));
	} else {
		return encodeURIComponent($("#"+itemid, $(div)).val());
	}

}
function getObjValue(itemid) {
	if ($("#"+itemid).get(0).type.toLowerCase() == "checkbox"
			&& $("#"+itemid).get(0).checked == false) {
		return "0";
	} else if ($("#"+itemid).get(0).type.toLowerCase() == "radio") {
		return encodeURIComponent(getRadioValueWithDiv(itemid));
	} else {
		return encodeURIComponent(encodeURIComponent($("#"+itemid).val()));
	}

}
/* Get Send Data from Div for filter */
function setSendDataForFilter(divid) {
	var txt = new String();
	var tp = '';
	if (divid=="")
		return "";
	var list;
	if (divid.indexOf(",")>-1) {
		list = divid.split(",");
	} else {
		list = new Array(1);
		list[0] = divid;
	}
	for( var i = 0 ;i<list.length;i++){
		var currentDivObj = $(list[i]);
		$('input, select', currentDivObj).each(function() {
			if ($(this).get(0).type.toLowerCase() == "checkbox"
					&& $(this).get(0).checked == false) {
				txt += "&";
				txt += $(this).get(0).name;
				txt += "=0";
			} else if ($(this).get(0).type.toLowerCase() == "radio"
							&& ($(this).get(0).checked == false
						|| $(this).get(0).value == ""
						|| $(this).get(0).value == null)) {
			} else {
				if ($(this).get(0).name == ""||$(this).get(0).name==undefined) {
				} else {
					txt += "&";
					txt += $(this).get(0).name;
					txt += "=";
					if (is_safari) {
						txt += encodeURIComponent($(this).get(0).value);
					} else {
						txt += encodeURIComponent($(this).get(0).value);
					}
				}
			}

			$('textarea', currentDivObj).each(function () {
				txt += "&" + $(this).attr("name") + "=" + encodeURIComponent($(this).val());
			});
		});
	}
	txt += getFixValues();
	if (txt.length > 0) {
		txt = txt.substring(1);
	}

	return txt;
}
/* Get Send Data from Div */
function setSendDivData(divid) {
	var txt = new String();
	var tp = '';
	if (divid=="")
		return "";
	var list;
	if (divid.indexOf(",")>-1) {
		list = divid.split(",");
	} else {
		list = new Array(1);
		list[0] = divid;
	}
	for( var i = 0 ;i<list.length;i++){

		var currentDivObj = $('#'+list[i]);
		$('input, select', currentDivObj).each(function() {
			if ($(this).get(0).type.toLowerCase() == "checkbox"
					&& $(this).get(0).checked == false) {
				txt += "&";
				txt += $(this).get(0).name;
				txt += "=0";
			} else if ($(this).get(0).type.toLowerCase() == "radio"
							&& ($(this).get(0).checked == false
						|| $(this).get(0).value == ""
						|| $(this).get(0).value == null)) {
			} else {
				if ($(this).get(0).name == ""||$(this).get(0).name==undefined) {
				} else {
					txt += "&";
					txt += $(this).get(0).name;
					txt += "=";
					if (is_safari) {
						txt += encodeURIComponent($(this).get(0).value);
					} else {
						txt += encodeURIComponent($(this).get(0).value);
					}
				}
			}

			$('textarea', currentDivObj).each(function () {
				txt += "&" + $(this).attr("name") + "=" + encodeURIComponent($(this).val());
			});
		});
	}
	if (txt.length > 0) {
		txt = txt.substring(1);
	}

	return txt;
}
/* Get Send Data from Div */
function setSendDivDataForSearch(divid) {
	var txt = new String();
	var tp = '';
	if (divid=="")
		return "";
	var list;
	if (divid.indexOf(",") > -1) {
		list = divid.split(",");
	} else {
		list = new Array(1);
		list[0] = divid;
	}
	for( var i = 0 ;i<list.length;i++){

		var currentDivObj = $('#'+list[i]);
		$('input, select', currentDivObj).each(function() {
			if ($(this).get(0).type.toLowerCase() == "checkbox"
					&& $(this).get(0).checked == false) {
			} else if ($(this).get(0).type.toLowerCase() == "radio"
							&& ($(this).get(0).checked == false
						|| $(this).get(0).value == ""
						|| $(this).get(0).value == null)) {
			} else {
				if ($(this).get(0).name == ""||$(this).get(0).name==undefined) {
				} else {
					txt += "&";
					txt += $(this).get(0).name;
					txt += "=";
					if (is_safari) {
						txt += encodeURIComponent($(this).get(0).value);
					} else {
						txt += encodeURIComponent($(this).get(0).value);
					}
				}
			}
		});

		$('textarea', currentDivObj).each(function () {
			txt += "&" + $(this).attr("name") + "=" + encodeURIComponent($(this).val());
		});
	}
	if (txt.length > 0) {
		txt = txt.substring(1);
	}

	return txt;
}
/* Get Send Data from Div of Grid*/
function setSendDivGridData(griddivid, chgFlg) {
	var txt = new String();
	var tp = '';
	if (griddivid=="")
		return "";
	var  list =griddivid.split(",");
	for( var i = 0 ;i<list.length;i++){

		$('input, select', $('#'+list[i]))
		  .filter(function (index) {
              return $("input[name^='"+chgFlg+"']", $(this).parent().parent()).val()=='1';
          })
		  .each(function() {
			if ($(this).get(0).type.toLowerCase() == "checkbox"
					&& $(this).get(0).checked == false) {
				txt += "&";
				txt += $(this).get(0).name;
				txt += "=0";
			} else if ($(this).get(0).type.toLowerCase() == "radio"
							&& ($(this).get(0).checked == false
						|| $(this).get(0).value == ""
						|| $(this).get(0).value == null)) {
			} else {
				if ($(this).get(0).name == ""||$(this).get(0).name==undefined) {
				} else {
					//alert(divid.elements[i].value + " : " + encodeURIComponent(divid.elements[i].value));
					txt += "&";
					txt += $(this).get(0).name;
					txt += "=";
					if (is_safari) {
						txt += encodeURIComponent($(this).get(0).value);
					} else {
						txt += encodeURIComponent($(this).get(0).value);
					}
				}
			}
		});
	}
	if (txt.length > 0) {
		txt = txt.substring(1);
	}
	return txt;
}

/* Get Send Data from Form */
function setSendDataNotDis(frm) {
	var txt = new String();
	if (frm=="")
		return "";

	for ( var i = 0; i < frm.elements.length; i++) {
		if (!frm.elements[i].disabled) {

			if (frm.elements[i].type == "checkbox"
					&& frm.elements[i].checked == false) {
				txt += "&";
				txt += frm.elements[i].name;
				txt += "=0";
			} else if (frm.elements[i].type == "radio"
					&& frm.elements[i].checked == false) {

			} else {
				txt += "&";
				txt += frm.elements[i].name;
				txt += "=";
				txt += encodeURIComponent(frm.elements[i].value);
			}
		}
	}
	if (txt.length > 0) {
		txt = txt.substring(1);
	}
	return txt;
}

/* Get Send Data from Form */
function setSearchSendData(frm) {

	var txt = new String();
	for ( var i = 0; i < frm.elements.length; i++) {
		//if (!frm.elements[i].disabled) {

			if (frm.elements[i].type == "checkbox"
					&& frm.elements[i].checked == false) {

			} else if (frm.elements[i].type == "radio"
					&& frm.elements[i].checked == false) {

			} else {
				txt += "&";
				txt += frm.elements[i].name;
				txt += "=";

				if (is_safari) {
					txt += encodeURIComponent(frm.elements[i].value);
				} else {
					txt += encodeURIComponent(frm.elements[i].value);
				}
			}
		//}
	}
	if (txt.length > 0) {
		txt = txt.substring(1);
	}
	return txt;
}
function getFixValues() {
	var txt = "";
	var fixo = ["ServerScriptID",
	            "ServerScriptFlg",
	            "ServerScriptResult",
	            "WF_PRINTFILEID",
	            "WF_PRINTFILEENCODE",
	            "pringFlg","PageID",
	            "SubID",
	            "pageRcds",
	            "currentpage",
	            "div",
	            "actid",
	            "actflg",
	            "mode",
	            "TargetObj",
	            "filterID",
	            "filterRow",
	            "filterError",
	            "recognID",
	            "srecognID","initSearch","sinitSearch","dataControlFlg","uniqueId","importFilePath","popflg",
	            "unloadCheck","isAfter","WF_RUNRESULT","WF_PREVLOC","WF_CURRLOC","WF_ADDLOC","WF_CUSTOMIZE-CHARTID","WF_CACHEABLE","pageFlg","triggerID"];
	if (fixo!=undefined && fixo.length >0) {
		for (i=0;i<fixo.length;i++) {
			v = fixo[i];
			if (getObj(v)) {
				txt += "&" +  v + "=" + encodeURIComponent(getObj(v).value);
			}
		}
	}
	return txt;
}
function setSpecData(o,g,gd){
	var v,txt,gv;
	var i,k,j,properties="";
	txt = "";
	if (o!=undefined && o.length >0) {
		for (i=0;i<o.length;i++) {
			v = o[i];
			if (getObj(v) && getObj(v) != undefined) {
				if (getObj(v).type == "checkbox"
						&& getObj(v).checked == false) {
					txt += "&" + v + "=0";
				} else if (getObj(v).type == "radio") {
					txt += "&" +  v + "=" + encodeURIComponent(getRadioValue(v));
				} else {
					txt += "&" +  v + "=" + encodeURIComponent(getObj(v).value);
				}
			} else {
				var saasforceAttributes = SF.makeItemAttributesForSpecData(v);
				if (saasforceAttributes != "") {
					properties += saasforceAttributes;
					properties += ",";
				}
			}
		}
	}

	if (g!=undefined && g.length >0) {
		var rows,gf;
		for ( i=0;i<g.length;i++) {
			rows = getObj(g[i]).rows.length;
			gf =  gd[i][0];
			for ( j=1;j<=rows;j++) {
				if (getObj(gf + j)!=undefined && getObj(gf + j).value !="") {
					gv = gd[i];
					for (k = 0; k < gv.length; k++) {
						v = gv[k] +j;
						if (getObj(v)) {
							if (getObj(v).type == "checkbox"
								&& getObj(v).checked == false) {
								txt += "&" + v + "=0";
							} else if (getObj(v).type == "radio") {
								txt += "&" +  v + "=" + encodeURIComponent(getRadioValue(v));

							} else {

								txt += "&" +  v + "=" + encodeURIComponent(getObj(v).value);
							}
						}
					}
				}
			}
		}
	}
	txt += getFixValues();
	txt += "&saasforceProperties=";
	txt += encodeURIComponent(properties);
	if (txt.length > 0) {
		txt = txt.substring(1);
	}
	return txt;
}


/*-----------------------------------------------------------------------------
============================================================
getAjaxRunData( httpObj, oneFieldId, doNextFlg,messageFlg,changeFlg,changeObjID,changeType )
============================================================
引数: doNextFlg - 次の動作(true or false)
	: messageFlg (true or false)
	: changeFlg メッセージ用文字列
	　changeFlg　- 1 （uniqueId）キーの値を更新,Script実行後返されたｽｸﾘﾌﾟﾄの実行
	  changeFlg　- 2 JSPから値（resultText変更しない）
	　changeFlg　- 3 失敗のみ、メッセージを表示
	  changeFlg　- 5 PopWinAjax戻り値を項目設定
    : changeObjID 設定対象
    : changeType  設定タイプ

機能:
-----------------------------------------------------------------------------*/
function getAjaxRunData(httpObject, oneFieldId, doNextFlg, messageFlg, changeFlg, changeObjID, changeType) {
	var Sharppos;
	var sUniqueId;
	var sMsg;
	var errResuld = null;
	createDiv(oneFieldId);
	setPosToCenter(oneFieldId);
	if ((httpObject.readyState == 4) && (httpObject.status == 200)||(httpObject.status == 0)) {

		resultText = httpObject.responseText;
		resultText=jQuery.trim(resultText);
		hidemsg(oneFieldId);

		if (resultText.length > 0) {
			if (changeFlg =="4") {
				Sharppos = resultText.indexOf("#");
				sUniqueId = resultText.substring(0,Sharppos);
				sMsg = resultText.substring(Sharppos+1);

				prestr = sMsg.substring(0, 1);
				msgstr = sMsg.substring(1);

				if (prestr == "0") {
					if (messageFlg) alert(msgstr);
				}

				if (prestr == "1") {// OK
					if (sUniqueId.length > 0) {
						if (messageFlg) alert(sUniqueId);
					}
					if (msgstr.length > 0)
						if (changeType =="div"){
							if (getObj(changeObjID))
								$("#"+changeObjID).html(msgstr);
						}
					if (doNextFlg) afterajax();
				}

			} else if (changeFlg =="3") {
				Sharppos = resultText.indexOf("#");
				sMsg = resultText.substring(Sharppos+1);

				prestr = sMsg.substring(0, 1);
				msgstr = sMsg.substring(1);
				//var strs = resultText.split("#");
				//prestr = strs[1].substring(0, 1);
				//msgstr = strs[1].substring(1);

				if (prestr == "1") {
					// OK
					if (doNextFlg) afterajax();
				} else {
					alert(msgstr);
				}

			} else if (changeFlg =="2") {
				if  (changeType =="text"){
					if (getObj(changeObjID)) {
						getObj(changeObjID).value = resultText;
					}
				} else if (changeType =="image"){
					if (getObj(changeObjID)) {
						var opName = new Array();
						opName = resultText.split(",");

						getObj(changeObjID).src = opName[0];
						getObj(changeObjID).alt = opName[1];
					}
				} else if (changeType =="div"){
					if (messageFlg) {
						Sharppos = resultText.indexOf("#");
						sMsg = resultText.substring(Sharppos+1);

						prestr = sMsg.substring(0, 1);
						msgstr = sMsg.substring(1);
						//var strs = resultText.split("#");
						//prestr = strs[1].substring(0, 1);
						//msgstr = strs[1].substring(1);

						if (prestr == "1") {
							// OK
							if (getObj(changeObjID)) {
								$("#"+changeObjID).html(msgstr);
							}
						} else if (prestr == "0"){
							alert(msgstr);
						}
					} else {
						$tbl = jQuery(resultText);
						$("#"+changeObjID).html($tbl);
					}
				} else if (changeType =="divRow"){
					if ($("#"+changeObjID)) {
						$("#"+changeObjID).html(resultText);
					}

				} else if (changeType =="table"){
					$("#"+changeObjID).append(resultText);
				} else if (changeType =="thickbox"){
					if (getObj(changeObjID)){
						getObj(changeObjID).value = resultText.replace(/(^\s*)|(\s*$)/g,"");
						setInnerHtml();
					}
				} else if (changeType =="select") {
					//SELECT
					hidemsg(oneFieldId);
					if (resultText !="") {
						if (getObj(changeObjID)){
							var opName = new Array();
							opName = resultText.split(",");
							getObj(changeObjID).innerHTML ="";
							for (i = 0; i < opName.length-1; i++) {
								var op =  opName[i].split("#");
								getObj(changeObjID).options.add(new Option(op[1], op[0]));
							}
						}
					}
				}  else if (changeType =="checkbox"){
					//SELECT
					hidemsg(oneFieldId);
					if (getObj(changeObjID)){
						var opName = new Array();
						opName = resultText.split(",");
						getObj(changeObjID).innerHTML ="";
						var inHtml = "";
						for (i = 0; i < opName.length-1; i++) {
							var op =  opName[i].split("#");
							//getObj(changeObjID).options.add(new Option(op[1], op[0]));
							inHtml +=  "<input type='checkbox' id='"+ op[0]+"' name='"+ op[0]+"'  value='"+ op[0]+"' onclick=\"javascript:setCheckBoxVal('"+ op[0]+"','"+ op[0]+"')\"> "+op[1];
						}
						getObj(changeObjID).innerHTML = inHtml;
					}
				} else if (changeType =="radio"){
					if (getObj(changeObjID)){
						setRadioValue(resultText, changeObjID);
					}
				} else if (changeType =="radioHtml"){
					//setRadioValue(resultText, changeObjID);
					var obj = changeObjID.split("#");
          //span-0;radio-1
					var opName = new Array();
					opName = resultText.split(",");
					var html = "";
					for (i = 0; i < opName.length-1; i++) {
						var op =  opName[i].split("#");
						html += "<input type='radio' name='"+ obj[1] + "' id='"+ obj[1] + "' value='"+ op[0]+"' >" +op[1] + "&nbsp;";
					}
					var spanID =  "#" + obj[0];
					if ($(spanID))
						$(spanID).html(html);
				} else {
					Sharppos = resultText.lastIndexOf("#");
					sUniqueId = resultText.substring(0,Sharppos);
					sMsg = resultText.substring(Sharppos+1);

					prestr = sMsg.substring(0, 1);
					msgstr = sMsg.substring(1);
					if (prestr == "0") {
						if (messageFlg) alert(msgstr);
					}
					//SELECT
					hidemsg(oneFieldId);
					if (getObj(changeObjID)) {
						if (getObj(changeObjID).type=="hidden"
							|| getObj(changeObjID).type=="text"
							|| getObj(changeObjID).type=="button") {
							$("#"+changeObjID).val("");
						} else {
							var opName = new Array();
							opName = resultText.split(",");
							getObj(changeObjID).innerHTML ="";
							getObj(changeObjID).options.add(new Option());
							for (i = 0; i < opName.length-1; i++) {
								var op =  opName[i].split("#");
								getObj(changeObjID).options.add(new Option(op[1], op[0]));
							}
						}
					}
				}
				if (doNextFlg) afterajax();
			} else if (changeFlg =="5") {
				var opName = new Array();
				if (isSplit.test(resultText)) {
					opName = resultText.split(/\#{12}\r\n/);
					setJS("pop",opName[0]);
					getObj(changeObjID).innerHTML = opName[1];
					if (doNextFlg) afterajax();
				}
			} else if (changeFlg =="6") {
				var opName = new Array();
				if (isSplit.test(resultText)) {
					opName = resultText.split(/\#{12}\r\n/);
					setJS("pop1",opName[0]);
					getObj(changeObjID).innerHTML = opName[1];
					setJS("pop2",opName[2]);
					if (doNextFlg) afterajax();
				}
			} else {
				Sharppos = resultText.lastIndexOf("#");
				sUniqueId = resultText.substring(0,Sharppos);
				sMsg = resultText.substring(Sharppos+1);

				prestr = sMsg.substring(0, 1);
				msgstr = sMsg.substring(1);

				if (prestr == "0") {
					if (messageFlg) alert(msgstr);
				}

				if (prestr == "1") {
					// OK
					if (changeFlg =="1") {
						if (getObj(changeObjID))
							getObj(changeObjID).value = sUniqueId;
					}

					if (msgstr.length > 0)
						if (messageFlg) alert(msgstr);

					if (doNextFlg) afterajax();
				}

				if (prestr == "2") {
          // CONTROL
					if (msgstr.length > 0) setJS(msgstr);
					if (doNextFlg) afterajax();
				}

				if (prestr == "3") {
					// Script

					if (changeFlg =="1") {
						if (getObj(changeObjID))
							getObj(changeObjID).value = sUniqueId;
					}

					if (msgstr.length > 0)
						if (messageFlg) alert(msgstr);

					if (doNextFlg) afterajax();
				}
			}
		} else {
			/* 正常に処理した場合 */
			if (doNextFlg) afterajax();
		}
	} else {
		errResuld = dealError();
		if (errResuld) {
			hidemsg(oneFieldId);
			alert(errResuld);
		} else {
			displaymsg(oneFieldId, jQuery.i18n.prop("com.msg_0010100"));
		}
	}
}
//廃棄予定
function getRstRunData(httpObject, oneFieldId, doFunc) {
	var errResuld = null;
	createDiv(oneFieldId);
	setPosToCenter(oneFieldId);
	if ((httpObject.readyState == 4) && (httpObject.status == 200)) {
		resultText = httpObject.responseText;

		if (resultText.length > 0) {
			var strs = resultText.split("#");
			var sUniqueId = strs[0];
			prestr = strs[1].substring(0, 1);
			msgstr = strs[1].substring(1);

			if (prestr == "0") {
				// NG
				hidemsg(oneFieldId);
				alert(msgstr);
			}

			if (prestr == "1") {
				// OK
				hidemsg(oneFieldId);
				if (msgstr.length > 0)
					alert(msgstr);

				if (getObj("actflg").value == "1")
					getObj("uniqueId").value = sUniqueId;

				if (doFunc)
					afterajax();
			}

			if (prestr == "2") {
        // CONTROL
				hidemsg(oneFieldId);
				if (msgstr.length > 0)
					setJS(msgstr);
				if (doFunc)
					afterajax();

			}
		} else {
			/* 正常に処理した場合 */
			hidemsg(oneFieldId);
			if (doFunc)
				afterajax();
		}
	} else {
		errResuld = dealError();
		if (errResuld) {
			hidemsg(oneFieldId);
			alert(errResuld);
		} else {
			displaymsg(oneFieldId, jQuery.i18n.prop("com.msg_0010100"));
		}
	}
}

// 2009/07/03 葉コンテンツ権限のみ、関数を追加
function getContAuthRstRunData(httpObject, oneFieldId, messageFlg) {
	var errResuld = null;
	createDiv(oneFieldId);
	setPosToCenter(oneFieldId);
	if ((httpObject.readyState == 4) && (httpObject.status == 200)) {
		resultText = httpObject.responseText;

		if (resultText.length > 0) {

			var strs = resultText.split("#");
			var sUniqueId = strs[0];
			prestr = strs[1].substring(0, 1);
			msgstr = strs[1].substring(1);
			var k = 0;
			if (prestr == "0") {
				// NG
				hidemsg(oneFieldId);
				if (messageFlg) alert(msgstr);
				form = getObj("rightFrm");
				for (k = 0; k < form.elements.length; k++) {
					element = form.elements[k];
					if (element.type == 'checkbox'){
						element.checked = false;
						element.disabled = false;
					}
				}
			}

			if (prestr == "1") {// OK
				hidemsg(oneFieldId);

				var auth = sUniqueId;
				var arr = auth.split(":");
				var form;
				var element;

				// 取得したデータをド画面にセットする
				if (auth.length > 0) {
					// 初期化
					form = getObj("rightFrm");
					for (k = 0; k < form.elements.length; k++) {
						element = form.elements[k];
						//if (element.name == "id" && element.type == 'checkbox')
						if (element.type == 'checkbox')	 {
							element.checked = false;
							element.disabled = false;
						}
					}

					var arrOpt = new Array();
					// 設置権限
					for ( var i = 0; i < arr.length; i++) {

						arrOpt = arr[i].split(",");

						var NodeId = arrOpt[0];
						var inhertFlg = arrOpt[1];
						var insertFlg = arrOpt[2];
						var updateFlg = arrOpt[3];
						var deleteFlg = arrOpt[4];
						var displayFlg = arrOpt[5];

						if (insertFlg =="1") {
							getObj(NodeId+"_insert").value = "1";
							getObj(NodeId+"_insert").checked = true;
						}

						if (updateFlg =="1"){
							getObj(NodeId+"_update").value = "1";
							getObj(NodeId+"_update").checked = true;
						}

						if (deleteFlg =="1"){
							getObj(NodeId+"_delete").value = "1";
							getObj(NodeId+"_delete").checked = true;
						}

						if (displayFlg =="1"){
							getObj(NodeId+"_display").value = "1";
							getObj(NodeId+"_display").checked = true;
						}

						if (inhertFlg =="1") {
							getObj(NodeId+"_noright").value = "1";
							getObj(NodeId+"_noright").checked = true;

							getObj(NodeId+"_insert").checked = false;
							getObj(NodeId+"_insert").value = "0";
							getObj(NodeId+"_insert").disabled = true;

							getObj(NodeId+"_update").checked = false;
							getObj(NodeId+"_update").value = "0";
							getObj(NodeId+"_update").disabled = true;

							getObj(NodeId+"_delete").checked = false;
							getObj(NodeId+"_delete").value = "0";
							getObj(NodeId+"_delete").disabled = true;

							getObj(NodeId+"_display").checked = false;
							getObj(NodeId+"_display").value = "0";
							getObj(NodeId+"_display").disabled = true;
						}
					}
				}
				if (messageFlg) alert(msgstr);
			}


		} else {
			/* 正常に処理した場合 */
			hidemsg(oneFieldId);
		}
	} else {
		errResuld = dealError();
		if (errResuld) {
			hidemsg(oneFieldId);
			alert(errResuld);
		} else {
			displaymsg(oneFieldId, jQuery.i18n.prop("com.msg_0010100"));
		}
	}
}

function ajaxDoSend(url,method,frm,comFlg) {
	if (httpObj) {

		var parameters;
		if (frm==undefined || frm=="") {
			parameters = "";
		} else {
			parameters = frm;
		}
		if (comFlg==undefined || comFlg=="") {
			httpObj.open(method, url, true);
			httpObj.timeout = 0;
			httpObj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
		} else {
			httpObj.open(method, url, comFlg);
			httpObj.timeout = 0;
			httpObj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
		}

		if (frm==undefined || frm=="") {
			httpObj.send();
		} else {
			httpObj.send(frm);
		}
	}
}

function ajaxSend(url,method,frm,spcdata,comFlg) {
	var p;
	httpObj = createXMLHttpRequest(initdisplayData);

	ajaxDoSend(url,method,resetSendData(frm,"",spcdata),comFlg);
}
function ajaxSendById(url,method,frm,spcid,comFlg) {
	var p;
	httpObj = createXMLHttpRequest(initdisplayData);

	ajaxDoSend(url,method,resetSendData(frm,spcid),comFlg);
}
function resetSendData(frm,spcid,spcdata) {
	var p;
	if (frm==undefined || frm=="") {
		p="";
	} else {
		p=setSendData(frm);
	}

	if (spcid != undefined) {
		if (p==""){
			p=setSpecData(spcid);
		} else {
			p=p+"&"+setSpecData(spcid);
		}
	}

	if (spcdata != undefined && spcdata!="") {
		if (p==""){
			p=spcdata;
		} else {
			p=p+"&"+spcdata;
		}
	}
	return p;
}
function ajaxSearchDoSend(url,method,frm) {
	if (httpObj) {
		httpObj.open(method, url, true);
		httpObj.timeout = 0;
		httpObj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
		var parameters = setSearchSendData(frm);
		httpObj.send(parameters);
	}
}
function ajaxSearchSend(url,method,frm) {
	httpObj = createXMLHttpRequest(initdisplayData);
	ajaxSearchDoSend(url,method,frm);
}
function ajaxSearchSendPop(url,method,frm) {
	httpObj = createXMLHttpRequest(initdisplayDataPop);
	ajaxSearchDoSend(url,method,frm);
}

function ajaxdel(frm,spcdata) {
	f = "d";
	ajaxSend(urlDel,"POST",frm,spcdata);
}

function ajaxUserDelete(frm,spcdata) {
	f = "d";
	ajaxSend(urlUserDelete,"POST",frm,spcdata);
}

function escapeSqlTag(input) {
	var ch, chr = "";
	for ( var i = 0; i < input.length; i++) {
		ch = input.charAt(i);
		if (ch == "\\")
			chr = chr + "\\\\";
		else if (ch == "'")
			chr = chr + "''";
		else
			chr = chr + ch;
	}
	return chr;
}
function createDiv(id) {
	if (getObj(id) == null) {
		myDiv = document.createElement("div");
		if (id) myDiv.setAttribute("id", id);
		if (id) myDiv.setAttribute("name", id);
		var objBody = getBody();
		objBody.appendChild(myDiv);
	}
}
function setPosToCenter(idSpan) {
	var cWidth,cHeight;
	var oWidth;
  //  = getObj(idSpan).offsetWidth;
	oWidth = 208;
	var oHeight = 30;
	var left,top;
	cWidth  = $(window).width();
	cHeight = $(window).height();
	getObj(idSpan).style.position  = "absolute";
	left = (cWidth  - oWidth)  * 0.5;
	top  = (cHeight - oHeight) * 0.5;

	$("#"+idSpan).css(
		{left: Math.max(left, 0)+"px",
		 top: Math.max(top,  0)+"px",
		 zIndex: '2000'});
}
function displaymsg(idSpan,msg){
	getObj(idSpan).innerHTML="<div align=center valign=middle><img src='/images/loadingAnimation.gif'/><br>"+msg+"</div>";
//	getObj(idSpan).style.backgroundColor='#CCCCCC';
	getObj(idSpan).style.backgroundColor='transparent';
	getObj(idSpan).style.color='#000000';
	$("#"+idSpan).show();
}
function hidemsg(idSpan){
	getObj(idSpan).innerHTML="";
	$("#"+idSpan).hide();
}
function createDivForFrm(id, frmid) {
	if (getObj(id)==null) {
		myDiv=document.createElement("div");
		if (id) myDiv.setAttribute("id", id);
		if (id) myDiv.setAttribute("name", id);
		var objFrm = getForm(frmid);
		objFrm.appendChild(myDiv);
	}
}

function getBody() {
	return document.getElementsByTagName("body").item(0);
}

function getForm(id) {
	return getObj(id);
}

function setControlObjId(s) {
	getObj("cid").value = s;
}

function setJS(s) {
	// script 要素作成
	nd = document.createElement("script");
	nd.setAttribute("type", "text/javascript");
	// head 要素の子どもに script 要素を追加する
	ndNew = document.getElementsByTagName("head").item(0).appendChild(nd);
	// script 要素のテキストに読みこんだファイルを入れる
	ndNew.text = s;
}
function setJS(id, s) {
	// script 要素作成
	nd = document.createElement("script");
	nd.setAttribute("id", id);
	nd.setAttribute("type", "text/javascript");
	// head 要素の子どもに script 要素を追加する
	ndNew = document.getElementsByTagName("head").item(0).appendChild(nd);
	// script 要素のテキストに読みこんだファイルを入れる
	ndNew.text = s;
}
function getAjaxRunDataJson(httpObject,d,doNextFlg,msgFlg,changeFlg,changeObjID,changeType,infomsgid,errmsgid) {
	var errResuld = null;
	createDiv(d);
	setPosToCenter(d);
	if ((httpObject.readyState == 4) && (httpObject.status == 200)) {

		resultText = httpObject.responseText;
		resultText=jQuery.trim(resultText);
		hidemsg(d);

		if (resultText.length > 0) {
			if (changeFlg =="2") {
        //searchpage
				var myJsonObj = jsonParse(resultText);
				if (changeType =="div"){
					$("#"+changeObjID).html(jQuery(myJsonObj.b));
				}
				if (msgFlg) {
					if (myJsonObj.i!= undefined && myJsonObj.i!="") {
						alert(myJsonObj.i);
					}
					if (myJsonObj.e!= undefined && myJsonObj.e!="") {
						alert(myJsonObj.e);
					}
				} else {
					$("#"+infomsgid).html(myJsonObj.i);
					$("#"+errmsgid).html(myJsonObj.e);
				}
			} else if (changeFlg =="3") { //mainpage
				var myJsonObj = jsonParse(resultText);
				if (changeType =="div"){
					$("#"+changeObjID).html(jQuery(myJsonObj.b));
				} else if (changeType =="text"){
					$("#"+changeObjID).val(myJsonObj.b);
				}
				if (msgFlg) {
					if (myJsonObj.i!= undefined && myJsonObj.i!="") {
						alert(myJsonObj.i);
					}
					if (myJsonObj.e!= undefined && myJsonObj.e!="") {
						alert(myJsonObj.e);
					}
				} else {
					$("#"+infomsgid).html(myJsonObj.i);
					$("#"+errmsgid).html(myJsonObj.e);
				}
			}
			if (doNextFlg) afterajax();
		} else {
			/* 正常に処理した場合 */
			if (doNextFlg) afterajax();
		}
	} else {
		errResuld = dealError();
		if (errResuld) {
			hidemsg(d);
			alert(errResuld);
		} else {
			displaymsg(d, "Loading ...");
		}
	}
}
/*-----------------------------------------------------------------------------
============================================================
getAjaxRunJsonData( httpObject, oneFieldId, doNextFlg,messageFlg,bodyFlg,bodyID,msgCntlFlg )
============================================================
引数: doNextFlg - 次の動作(true or false)
	: messageFlg (true or false)
	: bodyFlg (true or false)
    : bodyID 設定対象
    : msgCntlFlg メッセージ制御フラグ
    	0-無条件/次の動作
    	1-エラーなし/次の動作
    	2-confirmして/次の動作
機能:
-----------------------------------------------------------------------------*/
function getAjaxRunJsonData(httpObject, oneFieldId, doNextFlg,messageFlg,bodyFlg,bodyID,msgCntlFlg,popflg) {
	var errResuld = null;
	createDiv(oneFieldId);
	setPosToCenter(oneFieldId);
	if ((httpObject.readyState == 4) && (httpObject.status == 200)) {

		hidemsg(oneFieldId);

		var resultText = httpObject.responseText;

		getJAjaxRunJsonData(resultText,doNextFlg,messageFlg,bodyFlg,bodyID,msgCntlFlg,popflg);

	} else {
		errResuld = dealError();
		if (errResuld) {
			hidemsg(oneFieldId);
			alert(errResuld);
		} else {
			displaymsg(oneFieldId, "Loading ...");
		}
	}
}
/*-----------------------------------------------------------------------------
============================================================
getJAjaxRunJsonData( data,doNextFlg,messageFlg,bodyFlg,bodyID,msgCntlFlg )
============================================================
引数: doNextFlg - 次の動作(true or false)
	: messageFlg (true or false)
	: bodyFlg (true or false)
    : bodyID 設定対象
    : msgCntlFlg メッセージ制御フラグ
    	0-無条件/次の動作
    	1-エラーなし/次の動作
    	2-confirmして/次の動作
機能:
-----------------------------------------------------------------------------*/
function getJAjaxRunJsonData(data, doNextFlg,messageFlg,bodyFlg,bodyID,msgCntlFlg,popflg) {
	var resultText = data;
	resultText=jQuery.trim(resultText);

	if (resultText.length > 0) {
		var myJsonObj = jsonParse(resultText);
		var flg = true;
		if (messageFlg) {

			if (msgCntlFlg==undefined
					|| msgCntlFlg == ""
					|| msgCntlFlg == "0") {
				if (myJsonObj.e!=undefined) {
					alert(myJsonObj.e);
					flg = false;
				} else if (myJsonObj.i!=undefined) {
					alert(myJsonObj.i);
					flg = true;
				}
			} else if (msgCntlFlg == "1") {
				if (myJsonObj.e!=undefined) {
					alert(myJsonObj.e);
					flg = false;
				} else {
					if (myJsonObj.i!=undefined) {
						alert(myJsonObj.i);
						flg = true;
					}
				}
			} else if (msgCntlFlg == "2"){
				if (myJsonObj.i!=undefined) {
					var flg = confirm(myJsonObj.i);
					if (flg == true) {
						if (doNextFlg) {
							if (popflg==undefined
									||popflg==""
									||popflg=="0"){
								afterajax();
							} else {
								afterajaxpop();
							}
						}
						flg = true;
					} else {
						flg = false;
					}
				}
			}
		} else {
			if (msgCntlFlg == "1") {
				 if (myJsonObj.e!=undefined) {
					 alert(myJsonObj.e);
					flg = false;
				}
			 }
		}
		if (bodyFlg) {
			if ($("#"+bodyID)) {
				if (myJsonObj.b!=undefined) {
					$("#"+bodyID).html(jQuery(myJsonObj.b));
				} else {
					$("#"+bodyID).html(resultText);
				}
			}
		} else {
			var key,id;
			var jid;
			if (myJsonObj.v !== undefined) {
				for (let key in myJsonObj.v) {
					let id = myJsonObj.v[key];           // 例: "username"
					let value = myJsonObj[id];           // myJsonObj["username"]

					if (getObj(id)) {
						if (getObj(id).type === "radio") {
							setRadioValue(value, id);
						} else {
							$("#" + id).val(value);
						}
					}
				}
			}
			if (myJsonObj.h !== undefined) {
				for (let key in myJsonObj.h) {
					let id = myJsonObj.h[key];        // e.g. "dragB5"
					let value = myJsonObj[id];        // e.g. "<svg>...</svg><script>...</script>"

					if (getObj(id)) {
					$("#" + id).html(value);        // HTMLを挿入（←ここもscriptなら注意が必要）
					}
				}
			}
			if (myJsonObj.f!=undefined) {
				setJS(myJsonObj.f);
			}
			if (myJsonObj.r!=undefined) {
				eval(myJsonObj.r);
			}
		}

		if (flg) {
			if (doNextFlg) {
				if (popflg==undefined
						||popflg==""
						||popflg=="0"){
					afterajax();
				} else {
					afterajaxpop();
				}
			}
		}
	} else {
		/* 正常に処理した場合 */
		if (doNextFlg) {
			if (popflg==undefined
					||popflg==""
					||popflg=="0"){
				afterajax();
			} else {
				afterajaxpop();
			}
		}
	}

}
/*-----------------------------------------------------------------------------
============================================================
getQAjaxRunJson(oneFieldId,messageFlg,msgCntlFlg,popflg,lasturl,async,paramdata,nextFunc,showLoading )
============================================================
引数:
	: messageFlg (true or false)
    : msgCntlFlg メッセージ制御フラグ
    	0-無条件/次の動作
    	1-エラーなし/次の動作
    	2-confirmして/次の動作
    : popflg POPUP flag
    : lasturl url
    : async: true/false
    : paramdata: extend parameter
    : nextFunc 次FUNC
    : showLoading 処理中を表示
機能:
-----------------------------------------------------------------------------*/
function getQAjaxRunJson(oneFieldId,messageFlg,msgCntlFlg,popflg,lasturl,async,paramdata,nextFunc,showLoading, loadingContent) {
	try {
		$.ajax({
			type: "POST",
			url: lasturl,
			async: async,
			data: paramdata,
			timeout: 0,
			beforeSend: function(xhr) {
				if (showLoading==undefined || showLoading) {
					// SF.loadingOn(loadingContent);
				} else {
					SF.setServerExecute(true);
				}
			},
			success: function(responseText){
				try {
					getQAjaxRunJsonData(responseText,messageFlg,msgCntlFlg,popflg,nextFunc,lasturl);
					SF.setServerExecute(true);
				} catch(e) {
					if (showLoading==undefined || showLoading) {
						SF.loadingOff();
						SF.setServerExecute(true);
					}
					alert('JS Error:'+e.message);
				}
				return true;
			},
			error: function(XMLHttpRequest, textStatus, errorThrown){
				showAjaxErr(textStatus,XMLHttpRequest);
				if (showLoading==undefined || showLoading) {
					SF.loadingOff();
					SF.setServerExecute(true);
				}
				return false;
			}

		 });
	} catch(e) {
		if (showLoading==undefined || showLoading) {
			SF.loadingOff();
			SF.setServerExecute(true);
		}
		alert('JS Error:'+e.message);
		return true;
	}
}
function showAjaxErr(textStatus,XMLHttpRequest) {
	if (textStatus=='error') {
		if (XMLHttpRequest.status == '12029') {
			alert(jQuery.i18n.prop("common.err00010"));
		} else if (XMLHttpRequest.status == '403') {
			alert(jQuery.i18n.prop("common.err00011"));
		} else if (XMLHttpRequest.status == '404') {
			alert(jQuery.i18n.prop("common.err00012"));
		} else if (XMLHttpRequest.status == '500') {
			alert(jQuery.i18n.prop("common.err00013"));
		} else if (XMLHttpRequest.status == '503') {
			alert(jQuery.i18n.prop("common.err00014"));
		} else if (XMLHttpRequest.status == '0') {

		} else {
			alert(jQuery.i18n.prop("common.err00015") + "["+XMLHttpRequest.status+"]");
		}
	} else if (textStatus=='timeout') {
		alert("Can not access network.");
	}
}
/*-----------------------------------------------------------------------------
============================================================
getQAjaxRunJsonData(data,doNextFlg,messageFlg,msgCntlFlg,popflg,nextFunc,lasturl )
============================================================
引数: messageFlg (true or false)
    : msgCntlFlg メッセージ制御フラグ
    	0-無条件/次の動作
    	1-エラーなし/次の動作
    	2-confirmして/次の動作
機能:
-----------------------------------------------------------------------------*/
function getQAjaxRunJsonData(data,messageFlg,msgCntlFlg,popflg,nextFunc,lasturl) {
	var resultText = data;
	resultText=jQuery.trim(resultText);
	var flg = true;

	if (resultText.length > 0) {
		if (resultText.indexOf("@html@") != -1) {
			var areaid = resultText.substring(0, resultText.indexOf("@html@"));
			$("#"+areaid).html(resultText.substring(resultText.indexOf("@html@") + "@html@".length, resultText.length));
			if (nextFunc!=undefined&&nextFunc!="") {
				eval(nextFunc);
			}
			return;
		}
		// var myJsonObj = jsonParse(resultText);
		var myJsonObj = JSON.parse(resultText);
		var id;
		var jid;
		if (myJsonObj.v!=undefined) {
			for (var key in myJsonObj.v) {
				id = myJsonObj.v[key];
				jid = "myJsonObj." + id;
				if (getObj(id)) {
					if (getObj(id).type=="radio") {
						setRadioValue(eval(jid), id);
					} else {
						$("#"+id).val(eval(jid));
						if (eval("myJsonObj.WF_JSON_TYPE") == "excel" && nextFunc) {
							window[nextFunc](eval(jid));
							flg = false;
						}
					}
				}
			}
		}
		if (myJsonObj.status!=undefined) {

			if (nextFunc) {
				window[nextFunc](myJsonObj);
				flg = false;
			}
		}
		if (myJsonObj.h!=undefined) {
			for (var key in myJsonObj.h) {
				id = myJsonObj.h[key];
				jid = "myJsonObj." + id;
				if (getObj(id)) {
					$("#"+id).html(eval(jid));
				}
			}

		}
		if (myJsonObj.f!=undefined) {
			setJS("func",myJsonObj.f);
		}
 		if (myJsonObj.r!=undefined) {
			eval(myJsonObj.r);
		}

		if (messageFlg) {

			if (msgCntlFlg==undefined
					|| msgCntlFlg == ""
					|| msgCntlFlg == "0") {
				if (myJsonObj.e!=undefined) {
					alert(myJsonObj.e);
					if (myJsonObj.eu!=undefined) {
						eval(myJsonObj.eu);
					}
					flg = false;
				} else if (myJsonObj.i!=undefined) {
					alert(myJsonObj.i);
					flg = true;
				} else if (myJsonObj.c!=undefined) {
					success(myJsonObj.c);
					flg = true;
				}
			} else if (msgCntlFlg == "1") {
				if (myJsonObj.e!=undefined) {
					alert(myJsonObj.e);
					if (myJsonObj.eu!=undefined) {
						eval(myJsonObj.eu);
					}
					flg = false;
				} else {
					if (myJsonObj.i!=undefined) {
						alert(myJsonObj.i);
						flg = true;
					} else if (myJsonObj.c!=undefined) {
						success(myJsonObj.c);
						flg = true;
					}
				}

			} else if (msgCntlFlg == "2"){
				if (myJsonObj.i!=undefined) {
					flg = confirm(myJsonObj.i);
					if (flg == true) {
						flg = true;
					} else {
						flg = false;
					}
				}
			}
		} else {
			if (msgCntlFlg == "1") {
				 if (myJsonObj.e!=undefined) {
					 alert(myJsonObj.e);
					if (myJsonObj.eu!=undefined) {
						eval(myJsonObj.eu);
					}
					flg = false;
				} else if (myJsonObj.ei!=undefined) {
					$("#serverInform ul").html(myJsonObj.ei);
					$("div#serverInform").show();
					flg = false;
				} else {
					$("#serverInform ul").html("");
					$("div#serverInform").hide();
				}
			 }
		}

		if (myJsonObj.u!=undefined) {
			var url = myJsonObj.u;
			window.open(url, '_blank');
		}
		if (myJsonObj.filter_result!=undefined && myJsonObj.filter_target!=undefined) {
			var filter_target = myJsonObj.filter_target;
			var filter_result = myJsonObj.filter_result;
			SF.resetDropDownOptionsValue(filter_target, filter_result);
		}
		var nextFlg = true;
		if (myJsonObj.n!=undefined) {
			nextFlg = myJsonObj.n;
		} else {
			nextFlg = true;
		}
		if (flg && nextFlg) {
			if (nextFunc!=undefined&&nextFunc!="") {
				SF.loadingOff();
				eval(nextFunc);
			}
		}

 		if (myJsonObj.a!=undefined) {
 			var funid = myJsonObj.a;
 		    setTimeout(function(){
 	 			getQAjaxRunJson("rstfld",false,1,"",urlUserScript, true,"ServerScriptFlg=1&ServerScriptID="+funid,"");
 	 			SF.loadingOff();
 		    },3000);

		} else {
	 		if (myJsonObj.p!=undefined) {
	 			var reportid = myJsonObj.p;
	 		    setTimeout(function(){
	 		    	getQAjaxRunJson("rstfld",false,1,"",urlUserSearch,true,setSendData(document.form1),"printAjax");
	 		    	SF.loadingOff();
	 		    },3000);
	 		} else {
				SF.loadingOff();
				if (lasturl.indexOf("linkID") == -1) {
					SF.setServerExecute(true);
				}
	 		}
		}
	} else {
		SF.loadingOff();

		/* 正常に処理した場合 */
		if (nextFunc!=undefined && nextFunc!="") {
			eval(nextFunc);
		}

		if (lasturl.indexOf("linkID") == -1) {
			SF.setServerExecute(true);
		}

	}

}
//var mySetInteral = setTimeout;
//window.setTimeout = function(callback, interval) {
//	var args = Array.prototype.slice.call(arguments, 2);
//	function callFn(){callback.apply(null, args);}
//	return mySetInteral(callFn, interval);
//}

/*-----------------------------------------------------------------------------
============================================================
getQAjaxRun(data,oneFieldId,messageFlg,msgCntlFlg,popflg,lasturl,nextFunc )
============================================================
引数:
	: messageFlg (true or false)
    : msgCntlFlg メッセージ制御フラグ
    	0-無条件/次の動作
    	1-エラーなし/次の動作
    	2-confirmして/次の動作
    : popflg POPUP flag
    : lasturl url
    : async: true/false
    : paramdata: extend parameter
    : nextFunc 次FUNC
機能:
-----------------------------------------------------------------------------*/
function getQAjaxRun(oneFieldId,messageFlg,lasturl,async,paramdata,nextFunc, changeFlg, changeObjID, changeType) {
	createDiv(oneFieldId);
	setPosToCenter(oneFieldId);
	displaymsg(oneFieldId, "Loading ...");
	try {
		$.ajax({
			type: "POST",
			url: lasturl,
			async: async,
			data: paramdata,
			timeout: 0,
			beforeSend: function (xhr) {
			},
			success: function(responseText){
				hidemsg(oneFieldId);
				getQAjaxRunData(responseText,messageFlg,nextFunc, changeFlg, changeObjID, changeType);

			},
			error: function(XMLHttpRequest, textStatus, errorThrown){
				hidemsg(oneFieldId);
				showAjaxErr(textStatus,XMLHttpRequest);
			}

		 });
	} catch(e) {
		hidemsg(oneFieldId);
		alert('JS Error:'+e.message);
	}
}
/*-----------------------------------------------------------------------------
============================================================
getQAjaxRunData( data,messageFlg,nextFunc changeFlg, changeObjID, changeType )
============================================================
引数: nextFunc - 次の動作JS
	: messageFlg (true or false)
	: changeFlg メッセージ用文字列
	　changeFlg　- 1 （uniqueId）キーの値を更新,Script実行後返されたｽｸﾘﾌﾟﾄの実行
	  changeFlg　- 2 JSPから値（resultText変更しない）
	　changeFlg　- 3 失敗のみ、メッセージを表示
	  changeFlg　- 5 PopWinAjax戻り値を項目設定
    : changeObjID 設定対象
    : changeType  設定タイプ

機能:
-----------------------------------------------------------------------------*/
function getQAjaxRunData(data,messageFlg,nextFunc, changeFlg, changeObjID, changeType) {
	var Sharppos;
	var sUniqueId;
	var sMsg;
	var errResuld = null;
	var resultText = data;
	resultText=jQuery.trim(resultText);

	if (resultText.length > 0) {
		if (changeFlg =="4") {
			Sharppos = resultText.indexOf("#");
			sUniqueId = resultText.substring(0,Sharppos);
			sMsg = resultText.substring(Sharppos+1);

			prestr = sMsg.substring(0, 1);
			msgstr = sMsg.substring(1);

			if (prestr == "0") {
				if (messageFlg) alert(msgstr);
			}

			if (prestr == "1") {
        // OK
				if (sUniqueId.length > 0) {
					if (messageFlg) alert(sUniqueId);
				}
				if (msgstr.length > 0)
					if (changeType =="div"){
						if (getObj(changeObjID))
							$("#"+changeObjID).html(msgstr);
					}
				if (nextFunc!=undefined&&nextFunc!="") {
					eval(nextFunc);
				}
			}

		} else if (changeFlg =="3") {
			Sharppos = resultText.indexOf("#");
			sMsg = resultText.substring(Sharppos+1);

			prestr = sMsg.substring(0, 1);
			msgstr = sMsg.substring(1);

			if (prestr == "1") {
				// OK
				if (nextFunc!=undefined&&nextFunc!="") {
					eval(nextFunc);
				}
			} else {
				alert(msgstr);
			}

		} else if (changeFlg =="2") {
			if  (changeType =="text"){
				if (getObj(changeObjID)) {
					getObj(changeObjID).value = resultText;
				}
			} else if (changeType =="image"){
				if (getObj(changeObjID)) {
					var opName = new Array();
					opName = resultText.split(",");

					getObj(changeObjID).src = opName[0];
					getObj(changeObjID).alt = opName[1];
				}
			} else if (changeType =="div"){
				if (messageFlg) {
					Sharppos = resultText.indexOf("#");
					sMsg = resultText.substring(Sharppos+1);

					prestr = sMsg.substring(0, 1);
					msgstr = sMsg.substring(1);

					if (prestr == "1") {
						// OK
						if (getObj(changeObjID)) {
							$("#"+changeObjID).html(msgstr);
						}
					} else if (prestr == "0"){
						alert(msgstr);
					}
				} else {
					$tbl = jQuery(resultText);
					$("#"+changeObjID).html($tbl);
				}
			} else if (changeType =="divRow"){
				if ($("#"+changeObjID)) {
					$("#"+changeObjID).html(resultText);
				}

			} else if (changeType =="table"){
				$("#"+changeObjID).append(resultText);
			} else if (changeType =="thickbox"){
				if (getObj(changeObjID)){
					getObj(changeObjID).value = resultText.replace(/(^\s*)|(\s*$)/g,"");
					setInnerHtml();
				}
			} else if (changeType =="select") {
				//SELECT
				if (resultText !="") {
					if (getObj(changeObjID)){
						var opName = new Array();
						opName = resultText.split(",");
						getObj(changeObjID).innerHTML ="";
						for (i = 0; i < opName.length-1; i++) {
							var op =  opName[i].split("#");
							getObj(changeObjID).options.add(new Option(op[1], op[0]));
						}
					}
				}
			}  else if (changeType =="checkbox"){
				//SELECT
				if (getObj(changeObjID)){
					var opName = new Array();
					opName = resultText.split(",");
					getObj(changeObjID).innerHTML ="";
					var inHtml = "";
					for (i = 0; i < opName.length-1; i++) {
						var op =  opName[i].split("#");
						//getObj(changeObjID).options.add(new Option(op[1], op[0]));
						inHtml +=  "<input type='checkbox' id='"+ op[0]+"' name='"+ op[0]+"'  value='"+ op[0]+"' onclick=\"javascript:setCheckBoxVal('"+ op[0]+"','"+ op[0]+"')\"> "+op[1];
					}
					getObj(changeObjID).innerHTML = inHtml;
				}
			} else if (changeType =="radio"){
				if (getObj(changeObjID)){
					setRadioValue(resultText, changeObjID);
				}
			} else if (changeType =="radioHtml"){
				//setRadioValue(resultText, changeObjID);
				var obj = changeObjID.split("#");
        //span-0;radio-1
				var opName = new Array();
				opName = resultText.split(",");
				var html = "";
				for (i = 0; i < opName.length-1; i++) {
					var op =  opName[i].split("#");
					html += "<input type='radio' name='"+ obj[1] + "' id='"+ obj[1] + "' value='"+ op[0]+"' >" +op[1] + "&nbsp;";
				}
				var spanID =  "#" + obj[0];
				if ($(spanID))
					$(spanID).html(html);
			} else {
				/*Sharppos = resultText.lastIndexOf("#");
				sUniqueId = resultText.substring(0,Sharppos);
				sMsg = resultText.substring(Sharppos+1);
				prestr = sMsg.substring(0, 1);
				msgstr = sMsg.substring(1);
				if (prestr == "0") {
					if (messageFlg) alert(msgstr);
				}
				//SELECT the logic is unused after go json
				SF.resetDropDownOptionsValue(changeObjID, resultText);*/
			}
			if (nextFunc!=undefined&&nextFunc!="") {
				eval(nextFunc);
			}
		} else if (changeFlg =="5") {
			var opName = new Array();
			if (isSplit.test(resultText)) {//resultText.indexOf("############")!=-1) {
				opName = resultText.split(/\#{12}\r\n/);
				setJS("pop",opName[0]);
				getObj(changeObjID).innerHTML = opName[1];
				if (nextFunc!=undefined&&nextFunc!="") {
					eval(nextFunc);
				}
			} else {
				getObj(changeObjID).innerHTML = resultText;
			}
		} else if (changeFlg =="6") {
			var opName = new Array();
			if (isSplit.test(resultText)) {//resultText.indexOf("############")!=-1) {
				opName = resultText.split(/\#{12}\r\n/);
				setJS("pop1",opName[0]);
				getObj(changeObjID).innerHTML = opName[1];
				setJS("pop2",opName[2]);
				if (nextFunc!=undefined&&nextFunc!="") {
					eval(nextFunc);
				}
			} else {
				getObj(changeObjID).innerHTML = resultText;
			}
		} else {
			Sharppos = resultText.lastIndexOf("#");
			sUniqueId = resultText.substring(0,Sharppos);
			sMsg = resultText.substring(Sharppos+1);

			prestr = sMsg.substring(0, 1);
			msgstr = sMsg.substring(1);

			if (prestr == "0") {
				if (messageFlg) alert(msgstr);
			}

			if (prestr == "1") {// OK
				if (changeFlg =="1") {
					if (getObj(changeObjID))
						getObj(changeObjID).value = sUniqueId;
				}

				if (msgstr.length > 0)
					if (messageFlg) alert(msgstr);

				if (nextFunc!=undefined&&nextFunc!="") {
					eval(nextFunc);
				}
			}

			if (prestr == "2") {// CONTROL
				if (msgstr.length > 0) setJS(msgstr);
				if (nextFunc!=undefined&&nextFunc!="") {
					eval(nextFunc);
				}
			}

			if (prestr == "3") {// Script

				if (changeFlg =="1") {
					if (getObj(changeObjID))
						getObj(changeObjID).value = sUniqueId;
				}

				if (msgstr.length > 0)
					if (messageFlg) alert(msgstr);

				if (nextFunc!=undefined&&nextFunc!="") {
					eval(nextFunc);
				}
			}
		}
	} else {
		/* 正常に処理した場合 */
		if (nextFunc!=undefined&&nextFunc!="") {
			eval(nextFunc);
		}
	}
}
/* open dialog by lgh on 2012/4/30 */
function openFuncDiag(title, url, nextfunc, w, h, type, dialogid, param) {
	SF.setServerExecute(true);
	var dialogObj = $('#'+dialogid );
	if (!dialogObj.dialog("isOpen")) {
		dialogObj
			.dialog( 'option','position',["center","middle"]);

		if (title != undefined && $.trim(title) != "") {
			dialogObj.dialog( 'option','title',title);
		}

		if (w != '') {
			dialogObj.dialog( 'option','width',w);
		} else {
			dialogObj.dialog( 'option','width','auto');
		}

		if (h != '') {
			dialogObj.dialog( 'option','height',h);
		} else {

			dialogObj.dialog( 'option','height','auto');
		}

		dialogObj.unbind( "dialogopen");
		dialogObj.bind( "dialogopen", function(event, ui) {
			getFuncPage(url, nextfunc, type, dialogid, param);
		});
		dialogObj.dialog('open' );
	}
}
function getFuncPage(url,nextfunc,type,dialogid, param){
	if (param==undefined) {
		param = "";
	}
	if (type=='5') {
		//getQAjaxRun(oneFieldId,messageFlg,lasturl,async,paramdata,nextFunc, changeFlg, changeObjID, changeType)
		getQAjaxRun("rstfld1",true,url,true,param,nextfunc,"5",dialogid,"div");
	} else if (type=='6') {
		getQAjaxRun("rstfld1",true,url,true,param,nextfunc,"6",dialogid,"div");
	}
}
function ajaxDoFixUser(v, param, showLoading){
	var url = urlUserScriptFixUser;
	getQAjaxRunJson("rstfld",false,1,"",url, true,param+"&ServerScriptFlg=1&ServerScriptID="+v,"",showLoading);
}