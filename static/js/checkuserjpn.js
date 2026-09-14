var wftranferurl = "";
var alertMsg = "";
$.fn.tabIndex = function () {
    return $(this).parent().find(this).index() - 1;
};
$.fn.selectTabByID = function (tabID) {
    $(this).tabs("option", "active", $('#' + tabID).tabIndex());
};
$.fn.selectTabByIndex = function (tabIndex) {
    $(this).tabs("option", "active", tabIndex);
};
function getRandnum() {
	return Math.floor( Math.random() * 100000 );
}
function getRandParam() {
	return "&rand="+getRandnum();
}
function nullOrBlank(o) {
	if (o==null || o=='') {
		return true;
	} else {
		return false;
	}
}
function skipCheck(obj) {
	if ($(obj).attr("readonly")) {
		return true;
	}
	return false;
}
/*-----------------------------------------------------------------------------
============================================================
setItemFocus(field)
============================================================
引数	: field - チェックするフィールド
戻り値	:
機能	: 焦点設定
-----------------------------------------------------------------------------*/
function setItemFocus(field) {
	var id = $(field).attr("id");
	if ($("#O-" +id).get(0)) {
		setTimeout(function() {
			$("#O-" +id).focus();
			$("#O-"+id).select();
		},1);
	} else {
		setTimeout(function() {
			$("#"+id).focus();
			$("#"+id).select();
		},1);
	}
}

/*-----------------------------------------------------------------------------
============================================================
checkRequired( field, label, focus )
============================================================
引数	: field - チェックするフィールド
	: focus (true or false)
	: label メッセージ用文字列
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: 引数で渡された文字列が全て半角英字かどうかを判断する。
// 各関数の最後の引数はエラーが発生した時にそのフィールドにフォーカスをあてるかどうかを
// 指定するものです．
// true : フォーカスをあてる．false : フォーカスをあてない
// またJavaScriptのオーバーロードにそって，最終引数をしていせずに関数を呼び出した場合は
// trueを指定した場合と同じ動作をします．
// 例）
// フォーカスが当たる呼び出し方 checkRequired( field, "ラベル" )
//                              checkRequired( field, "ラベル", true )
// フォーカスが当たらない呼び出し方 checkRequired( field, "ラベル", false )
//
// 必須項目が入力済みかどうかチェックします。
-----------------------------------------------------------------------------*/
function checkRequired( field, label, focus, msg, hideMessage ) {
	var strMsg;
	var tvalue;
	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);
	if(field.type=="radio"){
		tvalue = getRadioValue(field.name);
		if ( tvalue ==""||tvalue==null||tvalue==undefined) {
			strMsg = msg.replace("@@",label);
			if (!hideMessage) {
				alert(strMsg);
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$(field).parent().addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		} else{
			return true;
		}
	}else if(field.type=="checkbox"){
		tvalue = $(field).is(":checked")
		if (!tvalue) {
			strMsg = msg.replace("@@",label);
			if (!hideMessage) {
				alert(strMsg);
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$(field).parent().addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		} else{
			return true;
		}
	} else {
		tvalue = field.value.replace(/^\s+|\s+$/g, "");
		field.value = tvalue;
		if ( tvalue ==""||tvalue==null) {
			strMsg = msg.replace("@@",label);
			if (!hideMessage) {
				alert(strMsg);
			}
			if (field.tagName.toLowerCase() == "select" && $field.hasClass("select2-offscreen")) {
				var displayObj = SF.getSelect2DisplayObj($field);
				displayObj.addClass("ErrStyle");
			} else {
				if( focus != false ){
					//field.focus();
					setItemFocus(field);
				}
				$(field).addClass("ErrStyle");
			}
			SF.setServerExecute(true);
			return false;
		} else {
			//if ($(field).hasClass("ErrStyle"))
			//	$(field).removeClass("ErrStyle");
			if (field.tagName.toLowerCase() == "select" && $field.hasClass("select2-offscreen")) {
				var displayObj = SF.getSelect2DisplayObj($field);
				displayObj.removeClass("ErrStyle");
			}
			return true;
		}
	}

}
/*-----------------------------------------------------------------------------
============================================================
isProperByteSize( field, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: focus 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: value 項目値
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 空文字列を受け付けるかどうか判定します。
-----------------------------------------------------------------------------*/
function acceptEmptyString( field, required, label, focus, value, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var s = field.value.replace(/^\s+|\s+$/g, "");
	field.value = s;
	if (value && value !=null) {
		s = value;
	}
	if ( s.length == 0 ) {
		if ( required ) {
			if (!hideMessage) {
				alert( "" + label + jQuery.i18n.prop("checkuserjpn.msg_00001"));
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		} else {
			//if ($(field).hasClass("ErrStyle"))
			//	$(field).removeClass("ErrStyle");
			return true;
		}
	} else {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}
}
/*-----------------------------------------------------------------------------
============================================================
isLenCheck( field, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 半角英数字のみの入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isLenCheck(field, length, label, focus, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var o = $("#"+field.id);
	var val=o.val();
	if (o.attr("_ire")) {
		var ire =o.attr("_ire");
		if ("###,###,##0" == ire) {
			val = o.val();
			while (val.indexOf(",") != -1) {
				val = val.replace(",", "");
			}
		}
	}

	var regex = o.attr("regex")
	if (regex && regex.indexOf("$1-$2") != -1) val = val.replaceAll("-", "")
	if (regex && regex.indexOf("#,#") != -1) val = val.replaceAll(",", "")

	var s = val.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	if (s.length >length) {
		if (!hideMessage) {
			alert("["+ label+ jQuery.i18n.prop("checkuserjpn.lbl_00001") + length + jQuery.i18n.prop("checkuserjpn.lbl_00002"));
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		SF.setServerExecute(true);
		return false;
	} else {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}
}
/*-----------------------------------------------------------------------------
============================================================
isLenMaxCheck( field, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 半角英数字のみの入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isLenMaxCheck(field, length, label, focus, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var val="";
	var o = $("#"+field.id);
	val = o.val();
	while (val.indexOf(",") != -1) {
		val = val.replace(",", "");
	}

	var s = val.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	if (s.length >length) {
		if (!hideMessage) {
			alert("["+ label+ jQuery.i18n.prop("checkuserjpn.lbl_00001") + length + jQuery.i18n.prop("checkuserjpn.lbl_00002"));
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		SF.setServerExecute(true);
		return false;
	} else {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}
}
/*-----------------------------------------------------------------------------
============================================================
isLenMinCheck( field, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 半角英数字のみの入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isLenMinCheck(field, length, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	if (s.length <length) {
		if (!hideMessage) {
			alert("["+ label+ jQuery.i18n.prop("checkuserjpn.lbl_00001")+length+jQuery.i18n.prop("checkuserjpn.lbl_00003") );
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		SF.setServerExecute(true);
		return false;
	} else {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}
}
/*-----------------------------------------------------------------------------
============================================================
isInputRegexCheck( field, inputRegexCheck, label, focus )
============================================================
引数	: field - チェックするフィールド
			: inputRegexCheck 正規表現式
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 正規表現に従った内容
		: false : 正しくない内容
機能	: // 正規表現で入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isInputRegexCheck(field,required,inputRegexCheck,label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s
	s = field.value.replace(/(^\s*)|(\s*$)/g,"");

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var inputRegex = "";
	var returnVal = acceptEmptyString( field, required, label, focus, null, hideMessage);
	if (returnVal) {
		if (!required && s == "") {
			returnVal = true;
		} else {
			var re = new RegExp("^" + inputRegexCheck + "$");
			if (s.match(re)){
				returnVal = true;
			}else{
				if (!hideMessage) {
					alert("["+ label+ jQuery.i18n.prop("checkuserjpn.lbl_00004") );
				}
				if( focus != false ){
					//field.focus();
					setItemFocus(field);
				}
				returnVal = false;
			}
		}
	}
	if (returnVal) {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
	} else {
		if (!$field.hasClass("ErrStyle")) {
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
		}
	}
	SF.setServerExecute(true);
	return returnVal;
}
/*-----------------------------------------------------------------------------
============================================================
isInputRegexCheck( field, inputRegexCheck, label, focus )
============================================================
引数	: field - チェックするフィールド
			: inputRegexCheck 正規表現式
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 正規表現に従った内容
		: false : 正しくない内容
機能	: // 正規表現で入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isInputPartRegexCheck(field,value,required,inputRegexCheck,label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var s = value;
	var inputRegex = "";
	var returnVal = acceptEmptyString( field, required, label, focus, null, hideMessage);

	if (returnVal) {
		var re = new RegExp("^" + inputRegexCheck + "$");
		if (s.match(re)){
			//if ($(field).hasClass("ErrStyle"))
			//	$(field).removeClass("ErrStyle");
			returnVal = true;
		}else{
			if (!hideMessage) {
				alert("["+ label+ jQuery.i18n.prop("checkuserjpn.lbl_00004") );
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			returnVal = false;
		}
	}
	SF.setServerExecute(true);
	return returnVal;
}
/*-----------------------------------------------------------------------------
============================================================
isDateCheck( field, required, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true / false
機能	: 有効な日付かどうかチェックします。
-----------------------------------------------------------------------------*/
function isDateCheck ( field, required, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}

	var inputRegexCheck = "(?!([02468][1235679]|[13579][01345789])000229)(([0-9]{4}(01|03|05|07|08|10|12)(0[1-9]|[12][0-9]|3[01]))|([0-9]{4}(04|06|09|11)(0[1-9]|[12][0-9]|30))|([0-9]{4}02(0[1-9]|1[0-9]|2[0-8]))|([0-9]{2}(([02468])[048]|[13579][26])0229))";
	var	returnVal = isInputRegexCheck(field,required,inputRegexCheck,label, focus, hideMessage);
	SF.setServerExecute(true);
	return returnVal;
}
/*-----------------------------------------------------------------------------
============================================================
isFixingLength(field,required,fixingLength,label)
============================================================
引数	: field - チェックするフィールド
		: required 必須or任意(true or false)
		: fixingLength 固定長
		: label メッセージ用文字列
戻り値	: true : 文字列が固定長になっている。
		: false : 文字列が固定長ではない。
機能	: 引数で渡された文字列が固定長であるかどうかを判断する。
-----------------------------------------------------------------------------*/
function isFixingLength(field, required, fixingLength, label, hideMessage){

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}
	if ( (s.length < fixingLength) || (s.length > fixingLength	) ) {
		if (!hideMessage) {
			alert( label + jQuery.i18n.prop("checkuserjpn.lbl_00005") +fixingLength+ jQuery.i18n.prop("checkuserjpn.lbl_00006"));
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		//field.focus();
		setItemFocus(field);
		SF.setServerExecute(true);
		return false;
	}
	//f ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
textareaMaxLimit( field, maxLimimit )
============================================================
引数	: field - チェックするフィールド
			: maxLimimit 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
機能	: // textarea最大長さチェックします。
-----------------------------------------------------------------------------*/
function textareaMaxLimit( field, maxLimimit ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;
	var strLen = 0;
	var i;
	for (i = 0; i < s.length && s != ""; i++) {
		var c = s.charCodeAt(i);
		if ( ( c >= 0x0 && c < 0x81 ) ||
			( c == 0xf8f0 ) ||
			( c >= 0xff61 && c < 0xffa0 ) ||
			( c >= 0xf8f1 && c < 0xf8f4 ) ) {
			strLen += 1;
		} else {
			strLen += 2;
			maxLimimit -=1;
		}
	}
	if (strLen>maxLimimit){
		field.value = field.value.substring(0,maxLimimit);
	}
}
/*-----------------------------------------------------------------------------
============================================================
isProperByteSize( field, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: value 項目値
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // CHECK文字列のバイト数を返します
-----------------------------------------------------------------------------*/
function isProperByteSize( field, length, label, focus, value, hideMessage ) {

	if (skipCheck(field) || length == -1) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;
	if (value && value !=null) {
		s = value;
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var strLen = 0;
	var i;
	for (i = 0; i < s.length && s != ""; i++) {
		var c = s.charCodeAt(i);
		if ( ( c >= 0x0 && c < 0x81 ) ||
			( c == 0xf8f0 ) ||
			( c >= 0xff61 && c < 0xffa0 ) ||
			( c >= 0xf8f1 && c < 0xf8f4 ) ) {
			strLen += 1;
		} else {
			strLen += 2;
		}
	}
	if (strLen > length) {
		var gap = strLen - length;
		var doubleByteLength = length / 2;
		if (!hideMessage) {
			alert( label + jQuery.i18n.prop("checkuserjpn.lbl_00007") + doubleByteLength + jQuery.i18n.prop("checkuserjpn.lbl_00008") + length + jQuery.i18n.prop("checkuserjpn.lbl_00009") + gap + jQuery.i18n.prop("checkuserjpn.lbl_00010") );
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		SF.setServerExecute(true);
		return false;
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isAlphabet(field, required, length, label)
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
戻り値	: true : 文字列は半角英字である。
				: false : 文字列は半角英字ではない。
機能	: 引数で渡された文字列が全て半角英字かどうかを判断する。
-----------------------------------------------------------------------------*/
// 半角英字のみの入力チェックに使用します。
function isAlphabet( field, required, label, length, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, true, null, hideMessage) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var alphabetChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( alphabetChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00012") + label + jQuery.i18n.prop("checkuserjpn.lbl_00013") );
			}
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isSingleBytesKana(field, required, length, label)
============================================================
引数	: field - チェックするフィールド
		: required 必須or任意(true or false)
		: length 最大長
		: label メッセージ用文字列
戻り値	: true : 文字列は全角カナ文字である。
		: false : 文字列は全角カナではない。
機能	: 引数で渡された文字列が全て全角カナ文字かどうかを判断する。
-----------------------------------------------------------------------------*/
function isSingleBytesKana(field, required, length, label, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var csZenKanaData1 = jQuery.i18n.prop("checkuserjpn.lbl_00014");
	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	for (i=0; i<s.length ; i++) {
		if (csZenKanaData1.indexOf(s.charAt(i)) == -1) {
			if (!hideMessage) {
				alert(jQuery.i18n.prop("checkuserjpn.lbl_00011")+s.charAt(i)+jQuery.i18n.prop("checkuserjpn.lbl_00012")+label+jQuery.i18n.prop("checkuserjpn.lbl_00015"));
			}
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isSingleByte( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 半角文字だけかどうかをチェックします
-----------------------------------------------------------------------------*/
function isSingleByte( field, required, label, length,focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var i;
	for ( i = 0; i < s.length && s != ""; i++ ) {
		var c = s.charCodeAt( i );
		if ( !( ( c >= 0x0 && c < 0x81 ) ||
			( c == 0xf8f0 ) ||
			( c >= 0xff61 && c < 0xffa0 ) ||
			( c >= 0xf8f1 && c < 0xf8f4 ) ) ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00012") + label + jQuery.i18n.prop("checkuserjpn.lbl_00016") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isAlphanumeric( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 半角英数字のみの入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isAlphanumeric( field, required, length, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var alphaNumericChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( alphaNumericChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00012") + label + jQuery.i18n.prop("checkuserjpn.lbl_00013") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isAlphabetOrSpace(field, required, length, label)
============================================================
引数	: field - チェックするフィールド
		: required 必須or任意(true or false)
		: length 最大長
		: label メッセージ用文字列
戻り値	: true : 文字列は半角英字もしくは半角ブランクである。
		: false : 文字列は半角英字もしくは半角ブランクではない。
機能	: 引数で渡された文字列が全て半角英字もしくは半角ブランクかどうかを判断する。
-----------------------------------------------------------------------------*/
// 半角英字もしくは半角ブランクのみの入力チェックに使用します。
function isAlphabetOrSpace( field, required, length, label, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, true, null, hideMessage ) ) {
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var alphabetOrSpaceChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( alphabetOrSpaceChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00012") + label + jQuery.i18n.prop("checkuserjpn.lbl_00013") );
			}
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isDoubleBytesKana(field, required, length, label)
============================================================
引数	: field - チェックするフィールド
		: required 必須or任意(true or false)
		: length 最大長
		: label メッセージ用文字列
戻り値	: true : 文字列は全角カナ文字である。
		: false : 文字列は全角カナではない。
機能	: 引数で渡された文字列が全て全角カナ文字かどうかを判断する。
-----------------------------------------------------------------------------*/
function isDoubleBytesKana(field, required, length, label, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	var csZenKanaData1 = jQuery.i18n.prop("checkuserjpn.lbl_00017");
	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	for (i=0; i<s.length ; i++) {
		if (csZenKanaData1.indexOf(s.charAt(i)) == -1) {
			if (!hideMessage) {
				alert(jQuery.i18n.prop("checkuserjpn.lbl_00011")+s.charAt(i)+jQuery.i18n.prop("checkuserjpn.lbl_00012")+label+jQuery.i18n.prop("checkuserjpn.lbl_00018"));
			}
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isDoubleBytes(field, required, length, label)
============================================================
引数	: field - チェックするフィールド
		: required 必須or任意(true or false)
		: length 最大長
		: label メッセージ用文字列
戻り値	: true : 文字列は全角文字のみである。
		: false : 文字列は全角文字のみではない。
機能	: 引数で渡された文字列が全て全角文字かどうかを判断する。
		  承認する文字
		  全角文字, Null
-----------------------------------------------------------------------------*/
function isDoubleBytes(field, required, label, length, hideMessage){

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, true, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var i;
	for ( i = 0; i < s.length && s != ""; i++ ) {
		var c = s.charCodeAt( i );
		if ( ( ( c >= 0x0 && c < 0x81 ) ||
				( c == 0xf8f0 ) ||
				( c >= 0xff61 && c < 0xffa0 ) ||
				( c >= 0xf8f1 && c < 0xf8f4 ) ) ) {
			if (!hideMessage) {
				alert(jQuery.i18n.prop("checkuserjpn.lbl_00011")+s.charAt(i)+jQuery.i18n.prop("checkuserjpn.lbl_00012")+label+jQuery.i18n.prop("checkuserjpn.lbl_00019"));
			}
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
checkObjNullAndNumber( field, label, focus, flg )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 有効な郵便番号かどうかチェックします。
-----------------------------------------------------------------------------*/
function checkObjNullAndNumber( field, label, focus, strMsg1,strMsg2,strMsg3, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var sss = field.value.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	if( sss.length == 0 ) {
		//alert( "項目'" + label + "'は空白になっております。入力してください。" );
		strMsg1 = strMsg1.replace("@@",label);
		alert(strMsg1);
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	} else {
		if( !checkNumber( field, label, focus,strMsg2,strMsg3) ){
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		} else {
			$field.removeClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "");
			}
			return true;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
checkIntegerType()
引数	: field - チャックされる対象
戻り値	: true : 文字列がInteger型
		: false : 文字列がInteger型ではない
機能	: 引数で渡された文字列がInteger型かどうかを判断する。
-----------------------------------------------------------------------------*/
function checkIntegerType(field, label, focus, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var val = field.value;
	var ss = val.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	while(ss.indexOf(",") > 0) {
		ss = ss.replace(",", "");
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	if(ss == null || ss == "") {
		$field.removeClass("ErrStyle");
		return true;
	}

	var postalCodeChars = "-0123456789";
	var i;

	for ( i = 0; i<ss.length; i++ ) {
		if ( postalCodeChars.indexOf( ss.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00020") + label + jQuery.i18n.prop("checkuserjpn.lbl_00021") );
			}
			if( focus ){
				//field.focus();
				setItemFocus(field);
				$field.addClass("ErrStyle");
				if (isStaticTableItem) {
					parentObj.css("background-color", "red");
				}
				SF.setServerExecute(true);
				return false;
			}
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isNumericType( field, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 数字と.のみの入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isNumericType( field, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	s = s.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	while(s.indexOf(",") > 0) {
		s = s.replace(",", "");
	}
	if(s == null || s == "") {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}

	// 文字種チェック
	var numericChars = "-.0123456789";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( numericChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00022") + label + jQuery.i18n.prop("checkuserjpn.lbl_00023") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	var firPoint = s.indexOf(".");
	if(firPoint >= 0) {
		if(firPoint == 0 || s.indexOf(".", firPoint + 1) >= 0) {
			alert("「" + label + jQuery.i18n.prop("checkuserjpn.lbl_00024"));
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
checkObjNullAndNumber( field, label, focus, flg )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 有効な郵便番号かどうかチェックします。
-----------------------------------------------------------------------------*/
function checkNumber( field, label, focus ,strMsg2,strMsg3, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var ss = field.value.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	var postalCodeChars = "-0123456789";
	var i;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	for ( i = 0; i<ss.length; i++ ) {
		if ( postalCodeChars.indexOf( ss.charAt( i ), 0 ) == -1 ) {
			//alert( "項目 '" + label + "' は数値ではありません。数値を入力して下さい。" );
			strMsg2 =strMsg2.replace("@@",label);
			if (!hideMessage) {
				alert(strMsg2);
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
				$field.addClass("ErrStyle");
				if (isStaticTableItem) {
					parentObj.css("background-color", "red");
				}
				SF.setServerExecute(true);
				return false;
			}
		}
	}

	if(parseInt(ss,10)==0){
		strMsg3 =strMsg3.replace("@@",label);
		if (!hideMessage) {
			alert(strMsg3);
		}
		//	  alert("項目「"+label+"」は0以上に設定してください。");
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isNumeric( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 数字と[-][.]のみの入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isNumeric( field, required, length, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;
	s = s.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	while(s.indexOf(",") > 0) {
		s = s.replace(",", "");
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, s, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, s, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var numericChars = "-.0123456789";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( numericChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00022") + label + jQuery.i18n.prop("checkuserjpn.lbl_00023") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	var firPoint = s.indexOf(".");
	if(firPoint >= 0) {
		if(firPoint == 0 || s.indexOf(".", firPoint + 1) >= 0) {
			alert("「" + label + jQuery.i18n.prop("checkuserjpn.lbl_00024"));
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}

/*-----------------------------------------------------------------------------
============================================================
isUnsignedNumeric( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 数字と.のみの入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isUnsignedNumeric( field, required, length, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;
	s = s.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	while(s.indexOf(",") > 0) {
		s = s.replace(",", "");
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, s, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, s, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var numericChars = ".0123456789";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( numericChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00022") + label + jQuery.i18n.prop("checkuserjpn.lbl_00023") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}

			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	var firPoint = s.indexOf(".");
	if(firPoint >= 0) {
		if(firPoint == 0 || s.indexOf(".", firPoint + 1) >= 0) {
			alert("「" + label + jQuery.i18n.prop("checkuserjpn.lbl_00024"));
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isInteger( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 整数かどうかチェックします。
-----------------------------------------------------------------------------*/
function isInteger( field, required, label, length, focus, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;
	s = s.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	while(s.indexOf(",") > 0) {
		s = s.replace(",", "");
	}

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, s, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, s, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var digits = "0123456789";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( digits.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00011") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00022") + label + jQuery.i18n.prop("checkuserjpn.lbl_00025") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isFixedPointDecimal( field, required, integerDigits, decimalDigits, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: integerDigits 整数部桁数
			: decimalDigits 小数部桁数
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 数値かどうか調べ桁数のチェックを行います
-----------------------------------------------------------------------------*/
function isFixedPointDecimal( field, required, integerDigits, decimalDigits, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// 文字種チェック
	if ( isNumeric( field, required, 1 + integerDigits + decimalDigits, label, focus, hideMessage ) ) {
		var point = s.indexOf( "." , 0 );
		if ( point == -1 ) {
			if ( !( s.length <= integerDigits ) ) {
				if (!hideMessage) {
					alert("["+ label + jQuery.i18n.prop("checkuserjpn.lbl_00026") + integerDigits + jQuery.i18n.prop("checkuserjpn.lbl_00027")+ decimalDigits + jQuery.i18n.prop("checkuserjpn.lbl_00028") );
				}
				if( focus != false ){
					//field.focus();
					setItemFocus(field);
				}
				$field.addClass("ErrStyle");
				if (isStaticTableItem) {
					parentObj.css("background-color", "red");
				}
				SF.setServerExecute(true);
				return false;
			}
		} else if ( !( ( point <= integerDigits ) && ( ( s.length - 1 ) - point ) <= decimalDigits ) ) {
			if (!hideMessage) {
				alert("["+ label + jQuery.i18n.prop("checkuserjpn.lbl_00026") + integerDigits + jQuery.i18n.prop("checkuserjpn.lbl_00027")+ decimalDigits + jQuery.i18n.prop("checkuserjpn.lbl_00028") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	} else {
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isDate( field, required, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 有効な日付かどうかチェックします。
-----------------------------------------------------------------------------*/
function isDate( field, required, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}
	// 文字種チェック
	var dateChars = "-/0123456789";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( dateChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert("[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00029") + jQuery.i18n.prop("checkuserjpn.lbl_00030") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00031") + label + jQuery.i18n.prop("checkuserjpn.lbl_00032") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	// 区切り文字を特定
	var delim;
	var hyphenPos = s.indexOf( "-" );
	var slashPos = s.indexOf( "/" );
	if ( hyphenPos >= 0 && slashPos < 0 ) {
		delim = "-";
	} else if ( slashPos >= 0 && hyphenPos < 0 ) {
		delim = "/";
	} else {
		if (!hideMessage) {
			alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00033") );
		}
		if( focus != false ){
			setItemFocus(field);
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 区切り文字で分割した結果が3つの数字列になっているかどうか
	var digits = s.split( delim );
	if ( digits.length != 3 || digits[ 0 ].length == 0 || digits[ 1 ].length == 0 || digits[ 2 ].length == 0
			|| digits[ 0 ].length > 5 || digits[ 1 ].length > 2 || digits[ 2 ].length > 2 ) {
		if (!hideMessage) {
			alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00033") );
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 整数化
	var year = eval( digits[ 0 ] );
	var month = eval( digits[ 1 ] );
	var day = eval( digits[ 2 ] );
	daysOfMonthInNormalYear = new Array( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 );
	daysOfMonthInLeapYear = new Array( 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 );
	// 月の範囲をチェック
	if ( month <= 0 || month > daysOfMonthInNormalYear.length ) {
		if (!hideMessage) {
			alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00034") );
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 日の範囲をチェック
	if ( ( year % 4 ) == 0 && ( year % 100 ) != 0 || ( year % 400 ) == 0 ) {
		if ( day <= 0 || day > daysOfMonthInLeapYear[ month - 1 ] ) {
			if (!hideMessage) {
				alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00035") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	} else {
		if ( day <= 0 || day > daysOfMonthInNormalYear[ month - 1 ] ) {
			if (!hideMessage) {
				alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00035") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	if( month < 10){
		month = "0" + month;
	}
	if( day < 10){
		day = "0" + day;
	}
	field.value = year + delim + month + delim + day;
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isYearMonth(field,required,label)
============================================================
引数	: field - チェックするフィールド
		: required 必須or任意(true or false)
		: label メッセージ用文字列
戻り値	: true : 文字列は有効な年と月である。
		: false : 文字列は有効な年と月ではない。
機能	: 引数で渡された文字列が有効な年月(YYYYMM)かどうかを判断する。
		  承認する文字
		  半角数字
-----------------------------------------------------------------------------*/
function isYearMonth( field, required, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列、バイト数チェック
	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if (s == ""){
		return true;
	}

	if( s.length!=0 && s.length!=5 && s.length!=6  && s.length!=7  ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		if (!hideMessage) {
			alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00036") );
		}
		setItemFocus(field);
		SF.setServerExecute(true);
		return false;
	}

	if (!s.match(/^[0-9]{4}(\/|-)?[0-9]{2}$/)) {
		if (!hideMessage) {
			alert( jQuery.i18n.prop("checkuserjpn.lbl_00037") + s + jQuery.i18n.prop("checkuserjpn.lbl_00038") + label + jQuery.i18n.prop("checkuserjpn.lbl_00039") );
		}
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
//	var dateChars = "-/0123456789";
//	var i;
//	for ( i = 0; i < s.length; i++ ) {
//		if ( dateChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
//			alert( "文字 '" + s.charAt( i ) + "' は" + label + "に使えません。数値を入力し直して下さい。" );
//			setItemFocus(field);
//			$(field).addClass("ErrStyle");
//			return false;
//		}
//	}

	// 区切り文字を特定
	var delim;
	var hyphenPos = s.indexOf( "-" );
	var slashPos = s.indexOf( "/" );
	if ( hyphenPos >= 0 && slashPos < 0 ) {
		delim = "-";
	} else if ( slashPos >= 0 && hyphenPos < 0 ) {
		delim = "/";
	} else if ( slashPos >= 0 && hyphenPos >= 0 ){
		if (!hideMessage) {
			alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00040") );
		}
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else {
		delim = "";
	}

	var year;
	var month;
	if (delim == "") {
		// 整数化
		if (s.length==6) {
			year = s.substr( 0, 4 );
			month = s.substr( 4, 2 );
		} else if (s.length==5) {
			year = s.substr( 0, 4 );
			month = s.substr( 4, 1 );
		}
	} else {
		// 区切り文字で分割した結果が3つの数字列になっているかどうか
		var digits = s.split( delim );
		if ( digits.length != 2 || digits[ 0 ].length == 0 || digits[ 1 ].length == 0
				|| digits[ 0 ].length > 5 || digits[ 1 ].length > 2 ) {
			if (!hideMessage) {
				alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00040") );
			}
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
		year = eval( digits[ 0 ] );
		month = eval( digits[ 1 ] );
	}

	daysOfMonthInNormalYear = new Array( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 );
	daysOfMonthInLeapYear = new Array( 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 );
	// 年の範囲をチェック
	if ( year < 1900 || year > 2079 ) {
		if (!hideMessage) {
			alert( "" + label + jQuery.i18n.prop("checkuserjpn.lbl_00041") );
		}
		//field.focus();
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 月の範囲をチェック
	if ( month <= 0 || month > daysOfMonthInNormalYear.length ) {
		if (!hideMessage) {
			alert( "" + label + jQuery.i18n.prop("checkuserjpn.lbl_00042") );
		}
		//field.focus();
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	if(year == 2079){
		if(month > 6){
			if (!hideMessage) {
				alert( "" + label + jQuery.i18n.prop("checkuserjpn.lbl_00043") );
			}
			//field.focus();
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	if (s.length==6 && delim == "") {
	} else if (s.length==6 && delim != "") {
		if( month < 10){
			month = "0" + month;
		}
		field.value = year + "/" + month;
	} else if (s.length==5) {
		field.value = year + "/" + "0" + month;
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
function isMonthDate(field, required, label, focus, hideMessage, year) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列、バイト数チェック
	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if (s == "") {
		return true;
	}

	if( s.length!=3 && s.length!=4  && s.length!=5 ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		if (!hideMessage) {
			alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00044") );
		}
		setItemFocus(field);
		SF.setServerExecute(true);
		return false;
	}

	if (!s.match(/^[0-9]{2}(\/|-)?[0-9]{2}$/)) {
		if (!hideMessage) {
			alert( jQuery.i18n.prop("checkuserjpn.lbl_00045") + s + jQuery.i18n.prop("checkuserjpn.lbl_00046") + label + jQuery.i18n.prop("checkuserjpn.lbl_00047") );
		}
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}

	// 区切り文字を特定
	var delim;
	var hyphenPos = s.indexOf( "-" );
	var slashPos = s.indexOf( "/" );
	if ( hyphenPos >= 0 && slashPos < 0 ) {
		delim = "-";
	} else if ( slashPos >= 0 && hyphenPos < 0 ) {
		delim = "/";
	} else if ( slashPos >= 0 && hyphenPos >= 0 ){
		if (!hideMessage) {
			alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00048") );
		}
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else {
		delim = "";
	}

	var month, day;
	if (delim == "") {
		// 整数化 4桁のみ
		if (s.length==4) {
			month = s.substr( 0, 2 );
			day = s.substr( 2, 2 );
		} else {
			if (!hideMessage) {
				alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00048") );
			}
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	} else {
		// 区切り文字で分割した結果が3つの数字列になっているかどうか
		var digits = s.split( delim );
		if ( digits.length != 2 || digits[ 0 ].length == 0 || digits[ 1 ].length == 0
		|| digits[ 0 ].length > 2 || digits[ 1 ].length > 2 ) {
			if (!hideMessage) {
				alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00048") );
			}
			setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
		month = eval( digits[ 0 ] );
		day = eval( digits[ 1 ] );
	}

  if (year == undefined || year == "") {
    year = new Date().getFullYear();
  }
	daysOfMonthInNormalYear = new Array( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 );
	daysOfMonthInLeapYear = new Array( 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 );
	// 月の範囲をチェック
	if ( month <= 0 || month > daysOfMonthInNormalYear.length ) {
		if (!hideMessage) {
			alert( "" + label + jQuery.i18n.prop("checkuserjpn.lbl_00049") );
		}
		//field.focus();
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 日の範囲をチェック
	if ( ( year % 4 ) == 0 && ( year % 100 ) != 0 || ( year % 400 ) == 0 ) {
		if ( day <= 0 || day > daysOfMonthInLeapYear[ month - 1 ] ) {
			if (!hideMessage) {
				alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00050") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	} else {
		if ( day <= 0 || day > daysOfMonthInNormalYear[ month - 1 ] ) {
			if (!hideMessage) {
				alert( "[" + label + jQuery.i18n.prop("checkuserjpn.lbl_00050") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	if (s.length==4 && delim == "") {
	} else if (s.length==4 && delim != "") {
		if( month < 10){
			month = "0" + month;
		} else if (day < 10) {
			day = "0" + day;
    }
		field.value = month + "/" + day;
	} else if (s.length==3) {
		field.value = month + "/" + "0" + days;
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isDateTime(field, required, label, focus)
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: 時刻付け日付をチェックする関数。
-----------------------------------------------------------------------------*/
function isDateTime(field, required, label, focus, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var val = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( val == "" ) {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}

	var msg = "「" + label + jQuery.i18n.prop("checkuserjpn.lbl_00051");
	var time = val.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去

	time = time.split(" ");
	var day = time[0];
	var date = time[1];

	if (time.length!=2) {
		if (!hideMessage) {
			alert(msg);
		}
		setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}

	field.value = day;
	if(!isDate(field, false, label, focus)) {
		field.value = val;
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	day = field.value;

	field.value = date;
	if(!isTime(field, false, label, focus)) {
		field.value = val;
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	date = field.value;

	// msg = "「" + label + "」に正しいタイムではありません。入力し直して下さい。";
	field.value = day + " " + date;
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}

/*-----------------------------------------------------------------------------
============================================================
isTime(field, required, label, focus)
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: 時刻チェック用関数。
-----------------------------------------------------------------------------*/
function isTime(field, required, label, focus, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var val = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( val == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}

	val = val.replace(/(^\s*)|(\s*$)/g,"");//両方の空白を除去
	var time = val.split(":");
	if(time.length != 3&&time.length != 2) {
		if (!hideMessage) {
			alert("「" + label + jQuery.i18n.prop("checkuserjpn.lbl_00052"));
		}
		if(focus)
			setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}

	var hour = time[0];
	var minute = time[1];
	var second;
	if (time.length==2) {
		second = "00";
	} else {
		second = time[2];
	}

	// 文字種チェック
	var msg = "「" + label + jQuery.i18n.prop("checkuserjpn.lbl_00052");
	var all = hour + minute + second;
	var numericChars = "0123456789";
	var i;
	for ( i = 0; i < all.length; i++ ) {
		if ( numericChars.indexOf( all.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert(msg);
			}
			if(focus)
				//field.focus();
				setItemFocus(field);
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}

	hour = Number(hour);
	minute = Number(minute);
	second = Number(second);

	if(hour < 0 || hour > 23 || minute < 0 || minute > 59 || second < 0 || second > 59) {
		if (!hideMessage) {
			alert(msg);
		}
		if(focus)
			//field.focus();
			setItemFocus(field);
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}

	if(hour < 10)
		hour = "0" + hour;
	if(minute < 10)
		minute = "0" + minute;
	if(second < 10)
		second = "0" + second;
	if (time.length==2) {
		field.value = hour + ":" + minute;
	} else {
		field.value = hour + ":" + minute + ":" + second;
	}

	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
DateBeforeCompare( date1, date2)
============================================================
引数	: date1 比較日付１
		: date2 比較日付２
戻り値	: false : date1 > date2
		: true : date1 <= date2
機能	: 日付比較を行う
-----------------------------------------------------------------------------*/
function DateCompare(date1, date2) {
	var dt1 = new Date();
	dt1.setTime(Date.parse(date1));
	var dt2 = new Date();
	dt2.setTime(Date.parse(date2));
	if (dt1 > dt2) {
		return false;
	} else {
		return true;
	}
}
/*-----------------------------------------------------------------------------
============================================================
isValidPhoneNumber( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 有効な電話番号かどうかチェックします。
-----------------------------------------------------------------------------*/
function isValidPhoneNumber( field, required, length, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var phoneNumberChars = "0123456789+-()";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( phoneNumberChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00045") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00046") + label + jQuery.i18n.prop("checkuserjpn.lbl_00053") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isValidPostalCode( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 有効な郵便番号かどうかチェックします。
-----------------------------------------------------------------------------*/
function isValidPostalCode( field, required,  label, length, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		$field.removeClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "");
		}
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var postalCodeChars = "0123456789-";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( postalCodeChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00045") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00046") + label + jQuery.i18n.prop("checkuserjpn.lbl_00054") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
checkMailRequired( field, label, focus )
============================================================
引数	: field - チェックするフィールド
	: focus (true or false)
	: label メッセージ用文字列
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: //メールアドレスの型のﾁｪｯｸ。
-----------------------------------------------------------------------------*/
function checkMailRequired( field, label, focus ,strMsg, hideMessage) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var tvalue;

	tvalue = field.value.replace(/^\s+/,"");
	if (tvalue.match(/^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)+$/)) {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}else {
		//alert("メールアドレスを「xxxxx@xxxxx.xxx」の格式で入力してください");
		if (!hideMessage) {
			alert(strMsg);
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		$(field).addClass("ErrStyle");
		SF.setServerExecute(true);
		return false;
	}
}
/*-----------------------------------------------------------------------------
============================================================
isValidEmailAddress( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // 有効なe-mailアドレスかどうかチェックします。
-----------------------------------------------------------------------------*/
function isValidEmailAddress( field, required,label, length, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;

	var $field = $(field);
	var parentObj = $field.parent(".WF_STABLE_CLASS_TH, .WF_STABLE_CLASS_TD");
	var isStaticTableItem = (parentObj.length > 0);

	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	} else if ( s == "" ) {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return true;
	}
	//正規表現によるチェック
	if (required) {
		if ( s.match( /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/ ) == null ){
			if (!hideMessage) {
				alert( "" + label + jQuery.i18n.prop("checkuserjpn.lbl_00055") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		}
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, null, hideMessage ) ) {
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var emailAddressChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.@";
	var atMarkOccurrence;
	atMarkOccurrence = 0;
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( emailAddressChars.indexOf( s.charAt( i ), 0 ) == -1 ) {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00056") + s.charAt( i ) + jQuery.i18n.prop("checkuserjpn.lbl_00057") + label + jQuery.i18n.prop("checkuserjpn.lbl_00058") );
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$field.addClass("ErrStyle");
			if (isStaticTableItem) {
				parentObj.css("background-color", "red");
			}
			SF.setServerExecute(true);
			return false;
		} else {
			if ( s.charAt( i ) == '@' ) {
				if ( atMarkOccurrence > 0 ) {
					if (!hideMessage) {
						alert( "" + label + jQuery.i18n.prop("checkuserjpn.lbl_00059") );
					}
					if( focus != false ){
						//field.focus();
						setItemFocus(field);
					}
					$field.addClass("ErrStyle");
					if (isStaticTableItem) {
						parentObj.css("background-color", "red");
					}
					SF.setServerExecute(true);
					return false;
				} else {
					atMarkOccurrence = 1;
				}
			}
		}
	}
	if ( s.match( /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/ ) == null ){
		if (!hideMessage) {
			alert( "" + label + jQuery.i18n.prop("checkuserjpn.lbl_00059") );
		}
		if( focus != false ){
			//field.focus();
			setItemFocus(field);
		}
		$field.addClass("ErrStyle");
		if (isStaticTableItem) {
			parentObj.css("background-color", "red");
		}
		SF.setServerExecute(true);
		return false;
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isHtmlTagElementLess( field, required, length, label, focus )
============================================================
引数	: field - チェックするフィールド
			: required 必須or任意(true or false)
			: length 最大長
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // htmlのtagが含まれているかどうかチェックする
// <>が使用されていなければtrueを返す
// 使用されていればfalseをかえす
-----------------------------------------------------------------------------*/
function isHtmlTagElementLess( field, required, length, label, focus, hideMessage ) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.value;
	// 空文字列チェック
	if ( !acceptEmptyString( field, required, label, focus, null, hideMessage ) ) {
		//if ($(field).hasClass("ErrStyle"))
		//	$(field).removeClass("ErrStyle");
		return false;
	} else if ( s == "" ) {
		$(field).removeClass("ErrStyle");
		return true;
	}
	// バイト数チェック
	if ( !isProperByteSize( field, length, label, focus, null, hideMessage ) ) {
		$(field).addClass("ErrStyle");
		SF.setServerExecute(true);
		return false;
	}
	// 文字種チェック
	var htmlTagElement = "<>";
	var i;
	for ( i = 0; i < s.length; i++ ) {
		if ( htmlTagElement.indexOf( s.charAt( i ), 0 ) != -1 ) {
			if( label == "" ){
				if (!hideMessage) {
					alert( jQuery.i18n.prop("checkuserjpn.lbl_00060") );
				}
			}else{
				if (!hideMessage) {
					alert( jQuery.i18n.prop("checkuserjpn.lbl_00061") + label + jQuery.i18n.prop("checkuserjpn.lbl_00062") );
				}
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$(field).addClass("ErrStyle");
			SF.setServerExecute(true);
			return false;
		}
	}
	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
function checkSpecialInput(){
	return true;
	$selected = $("input:text:password,textarea");
	var t;
	var id ;
	for (var i = 0; i < $selected.length; i++) {
		t = $selected[i];
		if (!checkSpecialQuery($(t),true)) {
			SF.setServerExecute(true);
			return false;
		}
	}
	return true;
}
function checkSpecialQuery( obj, focus, hideMessage) {
	var s = obj.val();
	var regex = /'|--/;
	if (s.search(regex)>-1){
		if (!hideMessage) {
			alert(jQuery.i18n.prop("checkuserjpn.lbl_00063"));
		}
		if( focus != false ){
			obj.focus();
		}
		$(obj).addClass("ErrStyle");
		SF.setServerExecute(true);
		return false;
	} else {
		//if ($(obj).hasClass("ErrStyle"))
		//	$(obj).removeClass("ErrStyle");
		return true;
	}
}

/*-----------------------------------------------------------------------------
============================================================
rangeCheck( from, to,focus)
============================================================
引数	: from - チェックするフィールド
		: to 必須or任意(true or false)
		: focus 必須or任意(true or false)
戻り値	: true : 範囲正常
		: false : 不正
機能	:
-----------------------------------------------------------------------------*/
function rangeCheck(field,fromValue, toValue,label,focus, hideMessage){

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var fv = $(field).val();
	if (!isNaN(parseFloat(fromValue)) && !isNaN(parseFloat(toValue))) {
		var fromV = parseFloat(fromValue);
		var toV = parseFloat(toValue);
		if (fromV > toV) {
			if (!hideMessage) {
				alert(label+ jQuery.i18n.prop("checkuserjpn.lbl_00064")+fromValue+"-"+toValue+"]");
			}
			if( focus != false ){
				//field.focus();
				setItemFocus(field);
			}
			$(field).addClass("ErrStyle");
			SF.setServerExecute(true);
			return false;
		} else {
			if (isNumeric(field,false,20,label,focus, hideMessage)) {

				if (parseFloat(fv)< fromV
						|| parseFloat(fv)> toV) {
					if (!hideMessage) {
						alert(label+ jQuery.i18n.prop("checkuserjpn.lbl_00065")+fromValue+"-"+toValue+"]");
					}
					if( focus != false ){
						setItemFocus(field);
					}
					$(field).addClass("ErrStyle");
					SF.setServerExecute(true);
					return false;
				}
			} else {
				SF.setServerExecute(true);
				return false;
			}
		}
	}  else {
		if (fromValue > toValue) {
			if (!hideMessage) {
				alert(label+ jQuery.i18n.prop("checkuserjpn.lbl_00064")+fromValue+"-"+toValue+"]");
			}
			if( focus != false ){
				setItemFocus(field);
			}
			$(field).addClass("ErrStyle");
			SF.setServerExecute(true);
			return false;
		} else {
			if (fv != "") {
				if (fv <fromValue || fv> toValue) {
					if (!hideMessage) {
						alert(label+ jQuery.i18n.prop("checkuserjpn.lbl_00065")+fromValue+"-"+toValue+"]");
					}
					if( focus != false ){
						setItemFocus(field);
					}
					$(field).addClass("ErrStyle");
					SF.setServerExecute(true);
					return false;
				}
			}
		}
	}

	//if ($(field).hasClass("ErrStyle"))
	//	$(field).removeClass("ErrStyle");
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
isInputRegexCheck( field, inputRegexCheck, label, focus )
============================================================
引数	: field - チェックするフィールド
			: inputRegexCheck 正規表現式
			: label メッセージ用文字列
			: focus 必須or任意(true or false)
戻り値	: true : 正規表現に従った内容
		: false : 正しくない内容
機能	: // 正規表現で入力チェックに使用します。
-----------------------------------------------------------------------------*/
function isRegexCheck(field,inputRegexCheck) {

	if (skipCheck(field)) {
		return true;
	}
	if (field==undefined || field==null) {
		return true;
	}
	var s = field.val().replace(/(^\s*)|(\s*$)/g,"");
	var re = new RegExp("^" + inputRegexCheck + "$");
	if (s.match(re)){
		returnVal = true;
	}else{
		SF.setServerExecute(true);
		returnVal = false;
	}
	return returnVal;
}
function replaceAll(v,s,t) {
	if (jQuery.trim(v)==""){
		return v;
	} else {
		return v.split(s).join(t);
	}
}
/*-----------------------------------------------------------------------------
============================================================
dateFormatChang( from, to,focus)
============================================================
引数	: obj - 対象
戻り値	: true : 範囲正常
		: false : 不正
機能	:
-----------------------------------------------------------------------------*/
function dateFormatChange(obj,label){
	var s = obj.val().replace(/(^\s*)|(\s*$)/g,"");
	s = replaceAll(obj.val(),"/","");
	s = replaceAll(s,"-","")
	var inputRegexCheck = "(?!([02468][1235679]|[13579][01345789])000229)(([0-9]{4}(01|03|05|07|08|10|12)(0[1-9]|[12][0-9]|3[01]))|([0-9]{4}(04|06|09|11)(0[1-9]|[12][0-9]|30))|([0-9]{4}02(0[1-9]|1[0-9]|2[0-8]))|([0-9]{2}(([02468])[048]|[13579][26])0229))";
	if (isRegexCheck(obj,inputRegexCheck)) {
		s =s.substring(0,4) + "/" + s.substring(4,6)+ "/" + s.substring(6,8);
		obj.val(s);
	}
}
//パスワードチェック
function pwdCheck(msg1,msg2,msg3) {
	var  userID = document.getElementById("UserID");
	var  pwd =document.getElementById("password")
	if (document.getElementById("actflg").value=="1")
		if( !checkRequired(pwd,jQuery.i18n.prop("checkuserjpn.lbl_00066"),true,msg1)) {
			return false;
		}

	if (userID.value == pwd.value){
		alert(msg2);
		SF.setServerExecute(true);
		return false;
	}
	if (pwd.value.length <6){
		alert(msg3);
		SF.setServerExecute(true);
		return false;
	}
	return true;
}
/*-----------------------------------------------------------------------------
============================================================
checkPasswords( passwordNew, passwordConfirm, focus )
============================================================
引数	: passwordNew - 入力したパスワード
	: passwordConfirm - もう一回入力したパスワード
	: focus 必須or任意(true or false)
戻り値	: true : 文字列は半角英字である。
		: false : 文字列は半角英字ではない。
機能	: // パスワード変更時にその確認入力と照合します。
----------------------------------------------------------------------------*/
function checkPasswords( passwordNew, passwordConfirm, focus, hideMessage ) {
	if ( isAlphanumeric( passwordNew, true, 256, jQuery.i18n.prop("checkuserjpn.lbl_00066"), focus )
	&& isAlphanumeric( passwordConfirm, true, 256, jQuery.i18n.prop("checkuserjpn.lbl_00067"), focus ) ) {
		if ( passwordNew.value == passwordConfirm.value ) {
			SF.setServerExecute(true);
			return false;
		} else {
			if (!hideMessage) {
				alert( jQuery.i18n.prop("checkuserjpn.lbl_00068") );
			}
			passwordNew.value = "";
			passwordConfirm.value = "";
			if( focus != false ){
				passwordNew.focus();
			}
		}
	}
	SF.setServerExecute(true);
	return false;
}

//指定された行を削除
function   DeleteSelectedRow(rowid,frame,flg){
  	var proFrame =  document.getElementById(frame);
	var proItem=proFrame.rows[rowid];
	proItem.style.display='none';
	document.getElementById(flg+rowid).value="0";

}

/* 日付、時刻、数字をフォーマットする
 * 画面から取得したデータをDB保存用データにフォーマット
 * @param type 入力形式
 * @param input 入力
 * @param outType 出力タイプ
 *        6:日付(時刻付き) 2:日付(時刻付けない) 3:時刻(日付付き) 4:時刻(日付付けない) 5:数字
 * 作成者：セン
 * 作成日：2010/01/06
 * 更新者：
 * 更新日：
 */
function changeToDBTimeNum(type, input, outType) {
	//if(input == null ||
	//		input == "" || outType == null || outType == "")
	//	return null;

	if(input == "" || outType == "")
		return "";

	/* 日付と時刻の時、入力データと入力形式の一致性チェック */
	//if(outType != 5 && outType.length != input.length)
	//	return "";

	/* 日付(6:時刻付き, 3:時刻付けない)変換
	 * 出力形式:1900-10-01 13:22:00 OR 1900-10-01
	 * 入力形式:yyyy/mm/dd、yyyy年mm月dd日、mm月dd日
	 */
	if(outType == 6 || outType == 3) {
		var year, month, day;

		var yearInd = type.indexOf("yyyy");
		if(yearInd >= 0)
			year = input.substring(yearInd, yearInd + 4);

		var monthInd = type.indexOf("mm");
		if(monthInd >= 0)
			month = input.substring(monthInd, monthInd + 2);

		var dayInd = type.indexOf("dd");
		if(dayInd >= 0)
			day = input.substring(dayInd, dayInd + 2);

		var now = new Date();
		if(year == "")
			year = now.getFullYear();

		if(month == "") {
			month = now.getMonth() + 1;
			if(month < 10)
				month = "0" + month;
		}

		if(day == "") {
			day = now.getDate();
			if(day < 10)
				day = "0" + day;
		}

		if(outType == 6)
			return year + "-" + month + "-" + day + " 00:00:00";
		else
			return year + "-" + month + "-" + day;
	}

	/* 時刻変換(7:日付付き, 4:日付付けない)
	 * 出力形式:1900-01-01 13:22:00 OR 13:22:00
	 * 入力形式:hh:mm、hh:mm:ss
	 */
	else if(outType == 7 || outType == 4) {
		var hour, minute, sencond;

		var hourInd = type.indexOf("hh");
		if(hourInd >= 0)
			hour = input.substring(hourInd, hourInd + 2);
		else
			hour = "00";

		var minuteInd = type.indexOf("mm");
		if(minuteInd >= 0)
			minute = input.substring(minuteInd, minuteInd + 2);
		else
			minute = "00";

		var secondInd = type.indexOf("ss");
		if(secondInd >= 0)
			second = input.substring(secondInd, secondInd + 2);
		else
			second = "00";

		//if(outType == 7)
		//	return "1900-01-01 " + hour + ":" + minute + ":" + second;
		//else
			return hour + ":" + minute + ":" + second;
	}

	/* 数字変換
	 * 出力形式:12345.1
	 */
	else if(outType == 2 || outType == 5) {
		return input.split(",").join("");
	}

	return "";
}


/* 日付、時刻、数字をフォーマットする
 * サーバーからロードしたデータを画面表示データにフォーマット
 * @param type 入力タイプ
 *        DATE:3;DATETIME:6;TIME:7;INT:2;DOUBLE:5;
 * @param input 入力
 * @param outParam 出力形式
 * 作成者：セン
 * 作成日：2010/01/05
 * 更新者：セン
 * 更新日：2010/01/06
 */
function setFormatedValue(type, input, outParam) {
	if(input == null || input == "" || outParam == null || outParam == "")
		return "";

	/* 日付変換
	 * 入力形式:1900-10-01 13:22:00 OR 1900-01-01
	 * 出力形式とoutParamの対応関係
	 *     yyyy/mm/dd     → 1900/10/01
	 *     yyyy年mm月dd日 → 1900年10月01日
	 *     mm月dd日       → 10月01日
	 */
	var hour,minute,second;
	if(type =="6"
		|| type =="3") {
		if(input.length != 10 && input.length != 19)
			return "";

		if (outParam.indexOf("hh")>-1
				&& outParam.indexOf("d")==-1){
			/* 時刻変換(日付付き)
			 * 入力形式:1900-10-01 13:22:00
			 * 出力形式とoutParamの対応関係
			 *     hh:mm     → 13:22
			 *     hh:mm:ss  → 13:22:00
			 */
			hour = input.substring(11, 13);
			minute = input.substring(14, 16);
			second = input.substring(17);

			return outParam.replace("hh", hour).replace("mm", minute).replace("ss", second);
		} else if (outParam.indexOf(jQuery.i18n.prop("checkuserjpn.lbl_00074"))>-1){
			/* 曜日変換
			 * 入力形式:2010-01-06 13:22:00 OR 2010-01-06
			 * 出力形式とoutParamの対応関係
			 *     金                       → 水
			 *     金曜日                   → 水曜日
			 *     yyyy/mm/dd(金)           → 2010/01/06(水)
			 *     yyyy年mm月dd日 金曜日    → 2010年01月06日 水曜日
			 */
			var year2 = input.substring(0, 4);
			var month2 = input.substring(5, 7);
			var day2 = input.substring(8, 10);

			var date = new Date(year2, month2 - 1, day2);
			var week = date.getDay();
			var weekArr = new Array(jQuery.i18n.prop("checkuserjpn.lbl_00069"), jQuery.i18n.prop("checkuserjpn.lbl_00070"), jQuery.i18n.prop("checkuserjpn.lbl_00071"), jQuery.i18n.prop("checkuserjpn.lbl_00072"), jQuery.i18n.prop("checkuserjpn.lbl_00073"), jQuery.i18n.prop("checkuserjpn.lbl_00074"), jQuery.i18n.prop("checkuserjpn.lbl_00075"));

			return outParam.replace("yyyy", year2).replace("mm", month2).replace("dd", day2).replace(jQuery.i18n.prop("checkuserjpn.lbl_00074"), weekArr[week]);
		} else if (outParam.indexOf("yyyy")>-1
				&& outParam.indexOf("hh")==-1){

			var year = input.substring(0, 4);
			var month = input.substring(5, 7);
			var day = input.substring(8, 10);

			return outParam.replace("yyyy", year).replace("mm", month).replace("dd", day);
		} else {
			return input;
		}
	}
	else if(type == "7") {
		/* 時刻変換(日付付けない)
		 * 入力形式:13:22:00
		 * 出力形式とoutParamの対応関係
		 *     hh:mm     → 13:22
		 *     hh:mm:ss  → 13:22:00
		 */
		if(input.length != 8)
			return "";

		var hour2 = input.substring(0, 2);
		var minute2 = input.substring(3, 5);
		var second2 = input.substring(6);

		return outParam.replace("hh", hour2).replace("mm", minute2).replace("ss", second2);

	}
	/* 数字変換
	 * 入力形式:12345.1
	 * 出力形式とoutParamの対応関係
	 *     000,000     → 012,345
	 *     000,000.00  → 012,345.10
	 */
	else if(type == "2"
		|| type == "5") {
		// マイナスかどうかの確認、マイナスの場合、"-"を取出す
		var minus = (input.substring(0, 1) == "-");
		if(minus) {
			input = input.substring(1);
		}

		// 対象がFloat型の場合、Int部分とFloat部分を分けて処理する
		var int, lim;
		var arr = input.split(".");
		if(arr.length == 1) {
			int = input;
			lim = "0";
		} else if(arr.length == 2) {
			int = arr[0];
			lim = arr[1];
		} else {
			return "";
		}

		// 出力形式がFloat型かどうかを判断して、分けて処理する
		var format = outParam.replace(",", "");
		var point = format.indexOf(".");
		if(point == -1) { // Float型ではない場合

			// Float部分をInt部分に四捨五入
			if(parseInt(lim.substring(0, 1)) > 4) {
   				int = int.substring(0, int.length - 1) + (parseInt(int.substring(int.length - 1)) + 1).toString();
   			}

   			if(int.length > format.length) { // 出力形式の桁数が対象の桁数より少ない場合
   				if(outParam.length > 3) {
	   				var outEnd = outParam.substring(outParam.length - 4);
	   				if(outEnd == ",999" || outEnd == ",000") { // フォーマット必要の場合
	   					var str = "";
	   					for(var i = int.length - 1; i >= 0;) {
	   						if(i > 2)
	   							str = "," + int.substring(i - 2, i + 1) + str;
	   						else
	   							str = int.substring(0, i + 1) + str;
	   						i = i - 3;
	   					}

	   					if(minus)
	   						return "-" + str;
	   					else
	   						return str;
	   				}
   				}

   				// フォーマット不要の場合
				if(minus)
					return "-" + input;
				else
					return input;
   			}

			// 出力形式の桁数で対象の前に"0"を追加
			for(var i1 = int.length; i1 < format.length; i1++) {
				int = "0" + int;
			}

			// 出力形式で分割する
			var con = outParam.indexOf(",");
			while( con >= 0) {
				int = int.substring(0, con) + "," + int.substring(con);
				con = outParam.indexOf(",", con + 1);
			}

			// "999,999"の形式で前の"0"を削除
			if(outParam.substring(0, 1) != "0") {
				var intSta = int.substring(0, 1);
				while((intSta == "0" || intSta == ",") && int.length > 1) {
					int = int.substring(1);
					intSta = int.substring(0, 1);
				}
			}

			if(minus)
				return "-" + int;
			else
				return int;
		} else { // Float型の場合

			// 出力形式がFloat型の場合、Int部分とFloat部分を分ける
			var point2 = outParam.indexOf(".");
			var int2 = outParam.substring(0, point2);
			var lim2 = outParam.substring(point2 + 1);

			// Float部分の処理
			if(lim.length > lim2.length) { // 出力形式のFloat部分の桁数が対象のFloat部分の桁数より少ない場合
				if(parseInt(lim.substring(lim2.length, lim2.length + 1)) > 4) {
					lim = lim.substring(0, lim2.length - 1) + (parseInt(lim.substring(lim2.length - 1, lim2.length)) + 1);
				} else
					lim = lim.substring(0, lim2.length);
			} else if(lim2.substring(lim2.length - 1) == "0"){ //Float部分部分に"0"を追加
				for(var k = lim.length; k < lim2.length; k++) {
					lim += "0";
				}
			}

			 // 出力形式のInt部分の桁数が対象のInt部分の桁数より少ない場合、フォーマットする
			if(int.length > point) {
				if(int2.length > 3) {
					var int2End = int2.substring(int2.length - 4);
					if(int2End == ",999" || int2End == ",000") {
						var str2 = "";
						for(var i2 = int.length - 1; i2 >= 0;) {
	   						if(i2 > 2)
	   							str2 = "," + int.substring(i2 - 2, i2 + 1) + str2;
	   						else
	   							str2 = int.substring(0, i2 + 1) + str2;
	   						i2 = i2 - 3;
	   					}

	   					if(minus)
	   						return "-" + str2 + "." + lim;
	   					else
	   						str2 + "." + lim;
					}
				}
				 // フォーマット不要
				var retVal = int + "." + lim;
				if(minus)
					return "-" + retVal;
				else
					return retVal;
			}

			// 出力形式の桁数で対象の前に"0"を追加
			for(var j = int.length; j < point; j++) {
				int = "0" + int;
			}

			// 出力形式で分割する
			var con2 = int2.indexOf(",");
			while( con2 >= 0) {
				int = int.substring(0, con2) + "," + int.substring(con2);
				con2 = int2.indexOf(",", con2 + 1);
			}

			// "999,999"の形式で前の"0"を削除
			if(outParam.substring(0, 1) != "0") {
				var intStart = int.substring(0, 1);
				while((intStart == "0" || intStart == ",") && int.length > 1) {
					int = int.substring(1);
					intStart = int.substring(0, 1);
				}
			}

			return int + "." + lim;
		}
	}
	return "";
}

/**
 *　機能： コントロールのIDによって、コントロールを得る
 *　パラメータ：	コントロールID
 */
function getObj(id) {
	var element = document.getElementById(id)
	if (!element || element.type === 'radio' || (element.tagName.toLowerCase() === 'div' && element.classList.contains('radios'))) {
      element = document.querySelector('input[name=\"' + id + '\"]');
    }
    return element;
}

function setGridCheckBoxVal(Obj){
	var check = Obj.is(':checked');
	if (check==true) {
		Obj.val("1");
	} else {
		Obj.val("0");
	}
}
function setCheckBoxVal(checkObj,valueObj){
	if (document.getElementById(checkObj).checked==true)
		document.getElementById(valueObj).value = "1";
	else
		document.getElementById(valueObj).value = "0";
}
function setCheckBoxValWithCntx(checkObj,valueObj,context){
	if ($('#'+checkObj,context).attr('checked')) {
		$('#'+checkObj,context).val("1");
	} else {
		$('#'+checkObj,context).val("0");
	}
}
function setCheckBoxCheck(checkObj,valueObj,checkVal){
	if (document.getElementById(valueObj).value == checkVal)
		document.getElementById(checkObj).checked = true;
	else
		document.getElementById(checkObj).checked = false;
}
/**
 *　機能： Radioを指定値に移動する
 *　パラメータ：	val			指定値
 *					objId		ドロップダウンのID
 */
function setRadioValue(val, objId) {
	var on = document.getElementsByName(objId);

	for (var m=0;m<on.length;m++) {
		if (on[m].value == val) {
			on[m].checked = true;
		} else {
			on[m].checked = false;
		}
	}
}
/**
 *　機能： ドロップダウンを指定値に移動する
 *　パラメータ：	val			指定値
 *					objId		ドロップダウンのID
 */
function setSelectValue(val, objId) {
	$('#'+objId).val(val);
//	var obj = getObj(objId);
//	if (obj) {
//		var opts = obj.options;
//		var noSelected = -1;
//
//		for (var i = 0; i < opts.length; i++) {
//			if (val == opts[i].value) {
//				noSelected = i;
//				obj.selectedIndex = i;
//				opts[i].setAttribute("selected", true);
//				break;
//			}
//		}
//
//		if (noSelected == -1) {
//			obj.selectedIndex = -1;
//		}
//	}
}
function getSelectValue(objId) {
	var obj = getObj(objId);
	if (obj.tagName.toLocaleLowerCase() == "select") {
		var opts = obj.options;

		for (var i = 0; i < opts.length; i++) {
			if (opts[i].selected) {
				return opts[i].value;
			}
		}
		return "";
	} else {
		return obj.value;
	}
}
function getSelectText(objId) {
	var obj = getObj(objId);
	if (obj.tagName.toLocaleLowerCase() == "select") {
		var opts = obj.options;

		for (var i = 0; i < opts.length; i++) {
			if (opts[i].selected) {
				return opts[i].text;
			}
		}
		return "";
	} else {
		return obj.value;
	}
}
function dataTransfer(direct,srecognid,sinitSearch){
	var url = '/user/inc/dataTransferU.jsp?dir=' +direct+'&srecognID='+srecognid+'&sinitSearch='+sinitSearch+getRandParam();
	location.href = url;
}
function changeSearchTextValue(v1,v2) {
	getObj(v2).value = getObj(v1).value;
}
function grep(obj,v1) {
	refObj = obj + "selectDiv";
	sourceObj = obj;
	if (!getObj(refObj)) {
		var html = $("#"+obj).parent().html();
		var  list =v1.split(",");
		html += "<ul id ='"+ refObj+  "' style='border:1 solid #grey:padding:0.3em 1em'>";
		 for( var i= 0 ;i<=list.length;i++){
			 html += "<span style='border:1 solid #grey:padding:0.3em 1em'>a</span>";
		 }
		 html += "</ul>";
		 $("#"+obj).parent().html(html);
	} else {
		$("#"+refObj).html("");
	}
	getObj("searchTextObjID").value = obj;
	getObj("searchFieldID").value = v1;
	sendcode = "5";
	ajaxSend(urlRunSearch,"POST",document.form1);
}
//特殊変更
function changeSpecHtml(obj){
	var $obj = $(obj);
	var _ire = $obj.attr("_ire");
	var mailRegStr = /^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)+$/;
	var htmlRegStr = /^(http:|https:)/i;
	if (_ire == undefined
			|| !_ire.match(mailRegStr)
			|| !_ire.match(htmlRegStr)) {
		return;
	}
	var id = $obj.attr("id");
	var textVal = $obj.val();
	var pObj = $obj.parent() ;
	var html= pObj.html();
	var flg = "0";
	var editStr = jQuery.i18n.prop("uprop001.alt_00001");
	if (textVal.match(mailRegStr)) {
		if (undefined == getObj(id+ "_-http")){
			pObj.append("<span id ='"+ id+"_-http' style='vertical-align: middle; width: " + pObj.width() + "px; height: " + pObj.height() + "px;'><a class='default' href='mailto:"+textVal+"'>"+textVal+"</a><img src='/images/icon/write.gif' style='float: right;' alt='" + editStr + "' onclick=\"showTextEdit('"+id+"')\"/></span>");
		} else {
			$("#"+id + "_-http").html("<a class='default' href='mailto:"+textVal+"'>"+textVal+"</a><img src='/images/icon/write.gif' style='float: right;' alt='" + editStr + "' onclick=\"showTextEdit('"+id+"')\"/></span>");
		}
		flg = "1";
	} else if (textVal.match(htmlRegStr)) {
		if (undefined == getObj(id+ "_-http")){
			pObj.append("<span id ='"+ id+"_-http' style='vertical-align: middle; width: " + pObj.width() + "px; height: " + pObj.height() + "px;'><a class='default' href='"+textVal+"' target=_blank>"+textVal+"</a><img src='/images/icon/write.gif' style='float: right;' alt='" + editStr + "' onclick=\"showTextEdit('"+id+"')\"/></span>");

		} else {
			$("#"+id + "_-http").html("<a class='default' href='"+textVal+"' target=_blank>"+textVal+"</a><img src='/images/icon/write.gif' style='float: right;' alt='" + editStr + "' onclick=\"showTextEdit('"+id+"')\"/></span>");
		}
		flg = "1";
	}

	if (flg =="1"){
		getObj(id+ "_-http").style.display= "table-cell";
		getObj(id).style.display= "none";
	}
}
function refSpecHtmlLoad() {
	var $selected = $('input:text,textarea');
	if ($selected.length>0) {
		for (var i = 0; i < $selected.length; i++) {
			SF.changeRefSpecHtml($selected[i]);
		}
	}
}
function showTextEdit(v) {
	getObj(v).style.display= "";
	getObj(v+ "_-http").style.display= "none";
	getObj(v).focus();
}
//エクセル出力
function ajaxDoExcelPrint(subID) {
	$(".ErrStyle").removeClass("ErrStyle");
	getObj("pringFlg").value = "1";
	$("#triggerID").val($("input[_subid="+subID+"]").attr("name"));
	getObj("SubID").value = subID;
	getQAjaxRunJson("rstfld",false,1,"",urlUserSearch,true,setSendData(document.form1),"printAjax();");
}
function printAjax(url) {
	var url= getObj("WF_PRINTFILEID").value;
	try {
		var top=50;
		var left=100;
		var width=800;
		var height=width/1.6;
		var arrUrl = url.split(",");
		var p ="";
		for (i = 0; i < arrUrl.length; i++) {
			p = arrUrl[i];
//			var nst= "/s/ExcelFile?f="+ encodeURIComponent(p);
//			var OpenWindow=window.open(nst,"_blank","height="+height+",width="+width+",top="+top+",left="+left+",toolbar=no,menubar=no,scrollbars=yes, resizable=no,location=no,status=no");
			SF.setWindowOpen("f="+ p, width, height, "/s/ExcelFile");
		}
	} catch (e) {
		alert('JS Error:'+e.message);
	}
}
function exportDBdataAjax() {
	var url= getObj("WF_PRINTFILEID").value;
	try {
		var top=50;
		var left=100;
		var width=800;
		var height=width/1.6;
		var arrUrl = url.split(",");
		var p ="";
		for (i = 0; i < arrUrl.length; i++) {
			p = arrUrl[i];
//			var nst= "/s/exportdbdata?exportdbdata="+ encodeURIComponent(p);
//			var OpenWindow=window.open(nst,"_blank","height="+height+",width="+width+",top="+top+",left="+left+",toolbar=no,menubar=no,scrollbars=yes, resizable=no,location=no,status=no");
			SF.setWindowOpen("exportdbdata="+ p, width, height, "/s/exportdbdata");
		}
	} catch (e) {
		alert('JS Error:'+e.message);
	}
}
function outExcelajax(v1,v2,v3) {
	var repId =v1;
	var inteId =v2;
	var top=50;
	var left=100;
	var width=800;
	var height=width/1.6;

	var nst="/s/outToExcelServlet?R_ID="+v1+"&INTELLISEARCH_ID="+v2+"&confVar="+v3;
	var OpenWindow=window.open(nst,"pretarget","height="+height+",width="+width+",top="+top+",left="+left+",toolbar=no,menubar=no,scrollbars=yes, resizable=no,location=no,status=no");
}
function ajaxDoImport(title,pageid,subID) {
	openFuncDiag(title,"/user/action/inout/uinout001.jsp?pageID="+pageid +"&subid="+subID,"uinout001_initFuncDialog();",700,550,'5','FuncDiv');
}
function ajaxDoExport(pageid,subID) {
	$(".ErrStyle").removeClass("ErrStyle");
	getObj("pringFlg").value = "5";
	$("#triggerID").val($("input[_subid="+subID+"]").attr("name"));
	getObj("SubID").value = subID;
	getQAjaxRunJson("rstfld",false,1,"",urlUserSearch,true,setSendData(document.form1),"exportAjax('"+pageid+"',"+subID+");");
}
function exportAjax(pageid,subID) {
//	var url="/s/Export?pageID="+pageid +"&exportID="+subID+"&"+setSendData(document.form1);
//	window.open(url, '_blank');

	var url= $("#WF_PRINTFILEID").val();
  var encode= $("#WF_PRINTFILEENCODE").val();
	var top=50;
	var left=100;
	var width=800;
	var height=width/1.6;
	var arrUrl = url.split(",");
	var p ="";
	for (i = 0; i < arrUrl.length; i++) {
		p = arrUrl[i];
//		var nst= "/s/Export?e="+ encodeURIComponent(p) + "&d=" +encode;
//		var OpenWindow=window.open(nst,"_self","height="+height+",width="+width+",top="+top+",left="+left+",toolbar=no,menubar=no,scrollbars=yes, resizable=no,location=no,status=no");
		SF.setWindowOpen("e="+ p + ",d=" +encode, width, height, "/s/Export");
	}

}
function ajaxDoClearSession(nextFunc) {
	var url = urlUserEdit+"?actid=100080&recognID="+getObj("recognID").value;
	getQAjaxRunJson("rstfld",false,1,"",url,true,"",nextFunc);
}
//指定された行を更新(changeSelectedRow(flg,row))
function csr(f,r,b){
	var i = parseInt(r)+parseInt(b);
	if (getObj(f+i).value!=2) {
		getObj(f+i).value="1";
	}
}
function cs(o,rowId,f,b){
	var s = getObjectParentByTagname(o,"tr").attr("id");
	s = s.substring(rowId.length);
	if (s != "") {
		var i = parseInt(s)+parseInt(b);
		if (getObj(f+i).value!=2) {
			getObj(f+i).value="1";
		}
	}
}
//Gridの行番号を取得
function getGridRowIndex(o,rid) {
	if (!o) {
		return;
	}
	var ro = o.get(0);
	while (ro.tagName.toLowerCase() != 'tr') {
		ro = ro.parentNode;
	}
	return ro.id.substring(rid.length);
}
//Gridの列番号を取得
function getCommonGridColIndex(o) {
	while (o.get(0).tagName.toLowerCase() != 'td') {
		o = o.parent();
	}
	return o.get(0).cellIndex;
}
//Gridの行番号を取得
function getCommonGridRowIndex(o) {
	while (o.get(0).tagName.toLowerCase() != 'tr') {
		o = o.parent();
	}
	return o.get(0).rowIndex;
}
function getObjectParentByTagname(o,s) {
	while (o.get(0).tagName.toLowerCase() != s) {
		if (o.parent() == undefined) {
			return o;
		}
		o = o.parent();
	}
	return o;
}
function pageLinkTranferBK2(toUrl,flg,o,mixpParam,mixValue,target,gMix,modalFlg,mbWidth,mbHeight){
	var afterParam = "";
	if (mixpParam.length >0) {
		var rowid = "1";
		if (flg == "1") {
			rowid = getGridRowIndex(o,"rowseq");
		}
		var arrParam = mixpParam.split(",");
		var arrValue = mixValue.split(",");
		var arrGrid = "";
		var m,g,f,l,p,v,gp,fg;
		for (var i = 0; i < arrParam.length-1; i++) {
			if (flg == "0") {
				if (getObj(arrValue[i])) {
					afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]).value);
				}
			} else {
				if (getObj(arrValue[i]+rowid)) {
					afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]+rowid).value);
				} else {
					if (getObj(arrValue[i])) {
						afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]).value);
					}
				}
			}
		}
		if (gMix != undefined) {
			arrGrid = gMix.split(",");
		}
		if (flg == "0") {
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							if (getObj("RowGrid"+g)) {
								for (var n=1;n<=getObj("RowGrid"+g).value; n++) {
									f = getObj("Grid"+g+ "flg" + n).value;
									if (f != "0") {
										l++;
										p = m[1] + l;
										v =  m[4]+ "_" + l;
										if (getObj(v)){
											afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
										}
									}
								}
								if (afterParam.indexOf("RowGrid_"+g+"_")==-1) {
									gp = "RowGrid_"+g+"_";
									afterParam += "&" +gp +"=" +l;
								}
							}
						} else {
							p = m[1];
							v = m[4];
							if (getObj(v)){
								afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
							}
						}
					}
				}
			}
		} else if (flg == "1"){
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						p = m[1];
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							v = m[4]+ "_" + rowid;
						} else {
							v = m[4];
						}
						if (getObj(v)) {
							afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
						}
					}
				}
			}
		}
	}
	if (target == "_self") {
		afterParam += "&popFlg=0&placeFlg="+flg;
	} else {
		afterParam += "&popFlg=1&placeFlg="+flg;
	}
	//alert(afterParam);

	//getDetailInfo
	var url = toUrl+afterParam;
	var ipos = url.indexOf("?");
	url = urlUserEdit + url.substr(ipos)+ "&actid=100055";
	//getQAjaxRunJson(oneFieldId,messageFlg,msgCntlFlg,popflg,lasturl,async,paramdata,nextFunc)
	getQAjaxRunJson("rstfld",false,1,"",url,false,'',"doTransferAfterCheck('"+toUrl+afterParam.replaceAll("\'", "\\'")+"','"+target+"','"+modalFlg+"','"+mbWidth+"','"+mbHeight+"');");
	//window.open(toUrl+afterParam, target);
}

function getValueByDataRegex(id) {
	var reg = "";
	var paramVal = "";
	var obj = $("#" + id);
	if (obj) {
		reg = obj.attr("_rge");
		paramVal = obj.val();
		if (paramVal != null && reg == "1") {
			paramVal = paramVal.replaceAll(",","");
		}
	}
	return paramVal;
}

function pageLinkTranfer(toUrl,flg,o,mixpParam,mixValue,target,gMix,modalFlg,mbWidth,mbHeight,partsflg){
	eval(toUrl.slice(0, -4)+ "()")
	return
	var afterParam = "";
	var wfpostParams = new Array();
	var paramVal = "";
	if (mixpParam.length >0) {
		var rowid = "1";
		if (flg == "1") {
			rowid = getGridRowIndex(o,"rowseq");
		}
		var arrParam = mixpParam.split(",");
		var arrValue = mixValue.split(",");
		var arrGrid = "";
		var m,g,f,l,p,v,gp,fg;
		var isHasVal = false;
		for (var i = 0; i < arrParam.length-1; i++) {
			isHasVal = false;
			if (flg == "0") {
				if ($('input[name='+arrValue[i]+']').attr("type") == 'radio') {
					paramVal = $('input[name='+arrValue[i]+']:checked').val();
					isHasVal = true;
				} else {
					if (getObj(arrValue[i])) {
						paramVal = getValueByDataRegex(arrValue[i]);
						isHasVal = true;
					}
				}
			} else {
				if ($('input[name='+arrValue[i]+']').attr("type") == 'radio') {
					if (getObj(arrValue[i]+rowid)) {
						paramVal = $('input[name='+arrValue[i]+rowid+']:checked').val();
						isHasVal = true;
					} else {
						if (getObj(arrValue[i])) {
							paramVal = $('input[name='+arrValue[i]+']:checked').val();
							isHasVal = true;
						}
					}
				} else {
					if (getObj(arrValue[i]+rowid)) {
						paramVal = getValueByDataRegex(arrValue[i]+rowid);
						isHasVal = true;
					} else {
						if (getObj(arrValue[i])) {
							paramVal = getValueByDataRegex(arrValue[i]);
							isHasVal = true;
						}
					}
				}
			}
			if (isHasVal) {
				afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(paramVal);
				var postParam = new Array();
				postParam.push(arrParam[i]);
				postParam.push(paramVal);
				wfpostParams.push(postParam);
			}
		}
		if (gMix != undefined) {
			arrGrid = gMix.split(",");
		}
		if (flg == "0") {
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							if (getObj("RowGrid"+g)) {
								for (var n=1;n<=getObj("RowGrid"+g).value; n++) {
									isHasVal = false;
									f = getObj("Grid"+g+ "flg" + n).value;
									if (f != "0") {
										l++;
										p = m[1] + l;
										v =  m[4]+ "_" + l;
										if ($('input[name='+v+']').attr("type") == 'radio') {
											paramVal = $('input[name='+v+']:checked').val();
											isHasVal = true;
										} else {
											if (getObj(v)){
												paramVal = getValueByDataRegex(v);
												isHasVal = true;
											}
										}
										afterParam += "&"+ p + "=" + encodeURIComponent(paramVal);
										var postParam = new Array();
										postParam.push(p);
										postParam.push(paramVal);
										wfpostParams.push(postParam);
									}
								}
								if (afterParam.indexOf("RowGrid_"+g+"_")==-1) {
									gp = "RowGrid_"+g+"_";
									afterParam += "&" +gp +"=" +l;
									var postParam = new Array();
									postParam.push(gp);
									postParam.push(l);
									wfpostParams.push(postParam);
								}
							}
						} else {
							p = m[1];
							v = m[4];
							if ($('input[name='+v+']').attr("type") == 'radio') {
								paramVal = $('input[name='+v+']:checked').val();
								isHasVal = true;
							} else {
								if (getObj(v)){
									paramVal = getValueByDataRegex(v);
									isHasVal = true;
								}
							}
							afterParam += "&"+ p + "=" + encodeURIComponent(paramVal);
							var postParam = new Array();
							postParam.push(p);
							postParam.push(paramVal);
							wfpostParams.push(postParam);

						}
					}
				}
			}
		} else if (flg == "1"){
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						p = m[1];
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							v = m[4]+ "_" + rowid;
						} else {
							v = m[4];
						}
						if ($('input[name='+v+']').attr("type") == 'radio') {
							paramVal = $('input[name='+v+']:checked').val();
							isHasVal = true;
						} else {
							if (getObj(v)) {
								paramVal = getValueByDataRegex(v);
								isHasVal = true;
							}
						}
						afterParam += "&"+ p + "=" + encodeURIComponent(paramVal);
						var postParam = new Array();
						postParam.push(p);
						postParam.push(paramVal);
						wfpostParams.push(postParam);
					}
				}
			}
		}
	}

	if (target == "_self") {
		//toUrl += "&popFlg=0&placeFlg="+flg+"&prevLoc=" + encodeURIComponent(window.location.href);
		toUrl += "&popFlg=0&placeFlg="+flg;
		var postParam = new Array();
		postParam.push(wfpostParams);
		postParam.push(encodeURIComponent(toUrl));
		//postParam.push(encodeURIComponent(window.location.href));
		//postParam.push(encodeURIComponent(getObj("prevLoc").value));
		SF.setPrevloc(postParam);
	} else {
		toUrl += "&popFlg=1&placeFlg="+flg;
	}

	//getDetailInfo
	var checkData = false;
	if (checkData) {
		var url = toUrl+afterParam;
		var ipos = url.indexOf("?");
		urlparam = url.substr(ipos+1)+ "&actid=100055";
		//getQAjaxRunJson(oneFieldId,messageFlg,msgCntlFlg,popflg,lasturl,async,paramdata,nextFunc)
		getQAjaxRunJson("rstfld",false,1,"",urlUserEdit,false,urlparam,"SF.postAfterLinkCheck(wftranferurl, wfpostParams,'"+target+"','"+modalFlg+"','"+mbWidth+"','"+mbHeight+"','"+partsflg+"');")
	} else {
		SF.postAfterLinkCheck(toUrl, wfpostParams, target, modalFlg, mbWidth, mbHeight, partsflg);

	}
}
function pageLinkTranferBK(toUrl,flg,o,mixpParam,mixValue,target,gMix,modalFlg,mbWidth,mbHeight){
	var afterParam = "";
	if (mixpParam.length >0) {
		var rowid = "1";
		if (flg == "1") {
			rowid = getGridRowIndex(o,"rowseq");
		}
		var arrParam = mixpParam.split(",");
		var arrValue = mixValue.split(",");
		var arrGrid = "";
		var m,g,f,l,p,v,gp,fg;
		for (var i = 0; i < arrParam.length-1; i++) {
			if (flg == "0") {
				if (getObj(arrValue[i])) {
					afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]).value);
				}
			} else {
				if (getObj(arrValue[i]+rowid)) {
					afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]+rowid).value);
				} else {
					if (getObj(arrValue[i])) {
						afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]).value);
					}
				}
			}
		}
		if (gMix != undefined) {
			arrGrid = gMix.split(",");
		}
		if (flg == "0") {
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							if (getObj("RowGrid"+g)) {
								for (var n=1;n<=getObj("RowGrid"+g).value; n++) {
									f = getObj("Grid"+g+ "flg" + n).value;
									if (f != "0") {
										l++;
										p = m[1] + l;
										v =  m[4]+ "_" + l;
										if (getObj(v)){
											afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
										}
									}
								}
								if (afterParam.indexOf("RowGrid_"+g+"_")==-1) {
									gp = "RowGrid_"+g+"_";
									afterParam += "&" +gp +"=" +l;
								}
							}
						} else {
							p = m[1];
							v = m[4];
							if (getObj(v)){
								afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
							}
						}
					}
				}
			}
		} else if (flg == "1"){
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						p = m[1];
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							v = m[4]+ "_" + rowid;
						} else {
							v = m[4];
						}
						if (getObj(v)) {
							afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
						}
					}
				}
			}
		}
	}
	getQAjaxRunJson("rstfld",false,1,"",toUrl,false,'',"doTransferAfterCheck('"+toUrl+afterParam+"','"+target+"','"+modalFlg+"','"+mbWidth+"','"+mbHeight+"');");
}

function pageLinkTranferGant(toUrl,o,mixpParam,mixValue,target,gMix,modalFlg,mbWidth,mbHeight){
	var afterParam = "";
	if (mixpParam.length >0) {
		var rowid = "1";
		var arrParam = mixpParam.split(",");
		var arrValue = mixValue.split(",");
		for (var i = 0; i < arrParam.length-1; i++) {
			afterParam += "&"+ arrParam[i] + "=" + encodeURIComponent(arrValue[i]);
		}
	}
	if (target == "_self") {
		afterParam += "&popFlg=0";
	} else {
		afterParam += "&popFlg=1";
	}
	//alert(afterParam);

	//getDetailInfo
	var url = toUrl+afterParam;
	var ipos = url.indexOf("?");
	url = urlUserEdit + url.substr(ipos)+ "&actid=100055";
	getQAjaxRunJson("rstfld",false,1,"",url,false,'',"doTransferAfterCheck('"+toUrl+afterParam+"','"+target+"','"+modalFlg+"','"+mbWidth+"','"+mbHeight+"');");

}

function doTransferAfterCheck(url, target, modalFlg,mbWidth,mbHeight ) {
  if (modalFlg==undefined || modalFlg == '' || modalFlg=='0') {
    SF.setServerExecute(true);
  	window.open(url, target);
  } else {
    SF.setServerExecute(true);
    if (mbWidth==undefined || mbWidth=='0') {
      mbWidth = "400px";
      mbHeight = "300px";
    } else {
      mbWidth = mbWidth + "px";
      mbHeight = mbHeight + "px";
    }
    var options = "dialogWidth=" + mbWidth + ";dialogHeight=" + mbHeight + ";toolbar=0;center=1;status=1;scroll=1;resizable=0;minimize=0;maximize=0;";
    window.open(url+"&modalFlg=1", target, options);
  }
}
function pageLinkTranferURL(toUrl,flg,o,mixpParam,mixValue,target,gMix,modalFlg){
	var afterParam = "";
	if (toUrl.indexOf("?") == -1) {
		afterParam = "?";
	} else {
		afterParam = "&";
	}
	if (mixpParam.length >0) {
		var rowid = "1";
		if (flg == "1") {
			rowid = getGridRowIndex(o,"rowseq");
		}
		var arrParam = mixpParam.split(",");
		var arrValue = mixValue.split(",");
		var arrGrid = "";
		var m,g,f,l,p,v,gp,fg,a;
		for (var i = 0; i < arrParam.length-1; i++) {
			if (i==0) {
				a="";
			} else {
				a="&";
			}
			if (flg == "0") {
				if (getObj(arrValue[i])) {
					afterParam += a+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]).value);
				}
			} else {
				if (getObj(arrValue[i]+rowid)) {
					afterParam += a+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]+rowid).value);
				} else {
					if (getObj(arrValue[i])) {
						afterParam += a+ arrParam[i] + "=" + encodeURIComponent(getObj(arrValue[i]).value);
					}
				}
			}
		}
		if (gMix != undefined) {
			arrGrid = gMix.split(",");
		}
		if (flg == "0") {
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							if (getObj("RowGrid"+g)) {
								for (var n=1;n<=getObj("RowGrid"+g).value; n++) {
									f = getObj("Grid"+g+ "flg" + n).value;
									if (f != "0") {
										l++;
										p = m[1] + l;
										v =  m[4]+ "_" + l;
										if (getObj(v)){
											afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
										}
									}
								}
								if (afterParam.indexOf("RowGrid_"+g+"_")==-1) {
									gp = "RowGrid_"+g+"_";
									afterParam += "&" +gp +"=" +l;
								}
							}
						} else {
							p = m[1];
							v = m[4];
							if (getObj(v)){
								afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
							}
						}
					}
				}
			}
		} else if (flg == "1"){
			if (arrGrid.length >0 && gMix!="") {
				for (var j = 0; j < arrGrid.length-1; j++ ){
					m = arrGrid[j].split("#");
					if (m[0]=="1"){
						p = m[1];
						g = m[2];
						l = 0;
						fg = m[3];
						if (m[3]=="1"){
							v = m[4]+ "_" + rowid;
						} else {
							v = m[4];
						}
						if (getObj(v)) {
							afterParam += "&"+ p + "=" + encodeURIComponent(getObj(v).value);
						}
					}
				}
			}
		}
	}

	doTransferAfterCheck(toUrl+afterParam, target, modalFlg);
}
function popSrchWinAjax(v1,v2,v3,v4,v5,v6,v7,v8,v9){
	var top=50;//(document.body.scrollTop + window.event.y)/2;
	var left=100;//document.body.scrollLeft + window.event.x;
	var width=760;
	var height=width/1.6;
	var params;
	var attparam = "";
	var row;
	var pageID = getObj("PageID").value;
	var flg = "1";
	if (v6 != "") {
		var condMixID,condIDs;
		var condValue;
		condMixID = v6.split(",");
		for (i = 0; i < condMixID.length-1; i++) {
			condIDs = condMixID[i].split(":");
			if (v4 =="0") {
				if (getObj(condIDs[0])) {
					condValue = getObj(condIDs[0]).value;
					if (condValue == "") {
						alert(condIDs[1]+ jQuery.i18n.prop("checkuserjpn.lbl_00076"));
						flg = "0";
					}
				} else {
					alert(condIDs[1]+ jQuery.i18n.prop("checkuserjpn.lbl_00077"));
					flg = "0";
				}
			} else if (v4 =="1") {
				row = getGridRowIndex(v3,"rowseq");
				if (getObj(condIDs[0]+ "_" + row)) {
					condValue = getObj(condIDs[0]+ "_" + row).value;
					if (condValue == "") {
						alert(condIDs[1]+ jQuery.i18n.prop("checkuserjpn.lbl_00076"));
						flg = "0";
					}
				} else {
					if (getObj(condIDs[0])) {
						condValue = getObj(condIDs[0]).value;
						if (condValue == "") {
							alert(condIDs[1]+ jQuery.i18n.prop("checkuserjpn.lbl_00076"));
							flg = "0";
						}
					} else {
						alert(condIDs[1]+ jQuery.i18n.prop("checkuserjpn.lbl_00077"));
						flg = "0";
					}
				}
			}
		}
	}

	if (flg == "1") {
		var itemname = "";
		if (v4 =="1") {
			row = getGridRowIndex(v3,"rowseq");
			itemname = $("#"+v3+"_"+row).attr("_itemname");
		} else {
			itemname = $("#"+v3).attr("_itemname");
		}

		if (v2 != null && v2 != "") {

			params = v2.split(",");

			if (v4 =="0") {
				for (i = 0; i < params.length-1; i++) {
					attparam += "&" +params[i]+ "="+ encodeURIComponent(getObj(params[i]).value);
				}
			} else {
				for (i = 0; i < params.length-1; i++) {
					if (getObj(params[i])) {
						attparam += "&" +params[i]+ "="+ encodeURIComponent(getObj(params[i]).value);
					} else {
						attparam += "&" +params[i]+ "="+ encodeURIComponent(getObj(params[i]+ "_" + row).value);
					}
				}
			}
		}

		var paramString = "";
		if (v4 =="0") {
			paramString = 'PageID='+pageID+'&SubID='+v1+'&dataControlFlg='+v7+attparam;
			openFuncDiag(itemname,"/user/uinu001.jsp?"+paramString,"uinu001_showSeniorOption();uinu001_ajaxQuery(1,'0');",v8,v9,'6','PopDiv');
		} else {
			paramString = 'PageID='+pageID+'&SubID='+v1+ '&SelGirdRow='+row+'&GridID='+v5+'&dataControlFlg='+v7+attparam;
			openFuncDiag(itemname,"/user/uinu001.jsp?"+paramString,"uinu001_showSeniorOption();uinu001_ajaxQuery(1,'0');",v8,v9,'6','PopDiv');
		}

		return;
		var url ="";
		url ='/user/uinu001.jsp';
		sendcode ="10";
		httpObj = createXMLHttpRequest(initdisplayData);
		if (httpObj) {
			httpObj.open("POST", url, false);
			httpObj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
			if (v4 =="0") {
				httpObj.send('PageID='+pageID+'&SubID='+v1+'&dataControlFlg='+v7+attparam);
			} else {
				httpObj.send('PageID='+pageID+'&SubID='+v1+ '&SelGirdRow='+row+'&GridID='+v5+'&dataControlFlg='+v7+attparam);
			}
		}
	}
}
function cntlValueClearGrid(v,o){
	var row = getGridRowIndex(o,"rowseq");
	var objMixID = v.split(",");
	var objID = "";
	for (i = 0; i < objMixID.length-1; i++) {
		objID = objMixID[i];
		if (getObj(objID+ "_" + row)) {
			getObj(objID+ "_" + row).value = "";
			if (getObj("O-" + objID+ "_" + row)) {
				getObj("O-" + objID+ "_" + row).value = "";
			}
		}
	}
}
function cntlValueClear(v){
	var objMixID = v.split(",");
	var objIDs;
	var objID = "";
	var gobjID = "";
	var line = 0;
	for (i = 0; i < objMixID.length-1; i++) {
		objIDs = objMixID[i].split(":");
		objID = objIDs[0];
		if (objIDs[1] == "0") {
			if (getObj(objID)) {
				getObj(objID).value = "";
				if (getObj("O-" + objID)) {
					getObj("O-" + objID).value = "";
				}
			}
		} else {
			gobjID = "RowGrid" + objIDs[2];
			line = getObj(gobjID).value;
			for (j = 1; j <= line; j++) {
				if (getObj(objID+ "_" + j)) {
					getObj(objID+ "_" + j).value = "";
					if (getObj("O-" + objID+ "_" + j)) {
						getObj("O-" + objID+ "_" + j).value = "";
					}
				}
			}
		}
	}
}
function doSmartPopChange(v2,v4,v6){
	$("#pringFlg").val("4");
	var pageID = $("#PageID").val();
	var subid = v4.attr("_subid");
	var gid = v4.attr("_gid");
	var itemname = v4.attr("_itemname");
	var isGrid = false;
	var paramMix = v2.split(",");//item id
	var att = "";
	var id = "";
	var row = "";
	var msgFlg = "0";
	if (gid != undefined && gid != "") {
		isGrid = true;
	}
	if (isGrid) {//level
		 row = getGridRowIndex(v4,"rowseq");
	}
	for (var i = 0; i < paramMix.length; i++) {
		id = paramMix[i];
		if (!isGrid) {
			if (getObj(id)){
				att += "&" + id + "=" + encodeURIComponent(getObj(id).value);
			}
		} else if (isGrid) {
			if (getObj(id)){
				att += "&" + id + "=" + encodeURIComponent(getObj(id).value);
			} else {
				if (getObj(id+ "_"+ row)){
					att += "&" + id+ "_"+ row + "=" + encodeURIComponent(getObj(id+ "_"+ row).value);
				}
			}
		}
	}
	var thisID = v4.attr("id");
	var thisVar = v4.val();
	if (thisVar == "") {
		return false;
	}
	att += "&"+thisID + "=" + encodeURIComponent(thisVar);
	if (isGrid) {
		att += "&Row=" + row;
	}
	var dataControlFlg = getObj("dataControlFlg").value;
	var lasturl = "/user/ajaxUser/XRRunSearch.jsp";
	var errObj = getObj("filterError").value;

	$.ajax({
		type: "POST",
		url: lasturl,
		async: false,
		data: "actid=100017&dataControlFlg="+dataControlFlg+"&pageID="+pageID+"&subID="+subid+att,
		success: function(data){
			data=jQuery.trim(data);
			if (data.length >4 ) {
				data = data.substring(2,data.length-3);
				var items = data.split(",");
				var vObjIDs;
				for (var idx=0 ; idx<items.length;idx++) {
					vObjIDs =items[idx].split(":");
					vObjIDs[0] = vObjIDs[0].split("\"").join("");
					vObjIDs[1] = vObjIDs[1].split("\"").join("");
					vObjIDs[0] = vObjIDs[0].substring(1);
					if (isGrid) {
						vObjIDs[0] += "_" + row;
					}
					if (getObj(vObjIDs[0])) {
						SF.setItemValue(vObjIDs[0], vObjIDs[1]);
						//getObj(vObjIDs[0]).value = vObjIDs[1];
					}
				}
				//if (v4.hasClass("ErrStyle"))
				//	v4.removeClass("ErrStyle");
				if (errObj.indexOf(thisID)>-1)  {
					errObj = errObj.split(thisID + ":" + itemname + ",").join("");
					getObj("filterError").value = errObj;
				}
			} else {
				v4.addClass("ErrStyle");
				if (msgFlg == "0") {
					var codeObjID = thisID.substring(2,thisID.length);
					getObj(codeObjID).value = "";
					alert(jQuery.i18n.prop("checkuserjpn.lbl_00078"));
					if (errObj.indexOf(thisID)==-1)  {
						getObj("filterError").value = errObj + thisID + ":" + itemname + ",";
					}
				}
			}
		},
		error: function(){
			alert('Error loading XML document');
		}

	 });
}
function setCalendar() {
	$('input.calendar',$('#target')).datepicker({
		showButtonPanel: true,
		changeMonth: true,
		changeYear: true
	});
}
function doStaticTableSearch(v1,v2) {
	getObj("SubID").value = v1;
	$("#triggerID").val($("input[_subid="+v1+"]").attr("name"));
    var url = "/user/ajaxUser/XRRunSearch.jsp?actid=900007&targetID="+v2+"&smartID="+v1;
    var array = null;
    getQAjaxRunJson("rstfld",true,1,"",url, true,setSendData(document.form1),"afterSearch(array,'"+v2+"');", true);
}

var self = null;

function afterSearch(array,v2) {
	if (self == null) {
		ko.applyBindings(new newsViewModel(array),document.getElementById("dragB"+v2));
	}
	if (array != null) {
		self.resultData({array:array});
	} else {
		self.resultData(undefined);
	}
}

function newsViewModel(array) {
	self = this;
	// Editable data
    self.resultData = ko.observable(array);
}

function doSmartSearch(v1,v2,v3,afterFunc) {
	$(".ErrStyle").removeClass("ErrStyle");
	getObj("pringFlg").value = "2";
	$("#triggerID").val($("input[_subid="+v1+"]").attr("name"));
	getObj("SubID").value = v1;
	var url,data;
	if (v2!="") {
		var count = v2.split(",");
		for (var i = 0; i < count.length; i++) {
			sendcode = "7";
			//displayObj = "_ingrid_Grid" +count[i]+"_0";
			displayObj = "dragB" +count[i];
			url = "/user/ajaxUser/XRRunSearch.jsp";
			data = "toSubID="+count[i]+"&actflg="+v3+"&targetID="+displayObj+"&"+setSearchSendData(document.form1);
			//refresh page layout
			if (afterFunc != undefined && afterFunc != null) {
				getQAjaxRunJson("rstfld",false,1,"",url, false,data,"_afterDoSmartSearch("+count[i]+");" + afterFunc, true);
			} else {
				getQAjaxRunJson("rstfld",false,1,"",url, false,data,"_afterDoSmartSearch("+count[i]+");", true);
			}

		}
	}
}
function _afterDoSmartSearch(i) {
	eval("setGrid"+i+"()");
	//SF.initPageStyle();
}

function doGetMapData(v2) {
	if (v2!="") {
		var count = v2.split(",");
		for (var i = 0; i < count.length; i++) {
      eval('doGetMapData'+count[i]+'();');
		}
	}
}
function doChartRefresh(v2,v1) {
	if (v2!="") {
		var count = v2.split(",");
		for (var i = 0; i < count.length; i++) {
			//$('#'+count[i],$('#target')).get(0).style.height = 'auto';
			//$('#'+count[i],$('#target')).get(0).style.width = 'auto';
			$('#'+count[i],$('#target')).attr('src','/images/loadingAnimation.gif');
			v3 = $('#'+count[i],$('#target')).parent().attr('oricond');
			if (v3 != undefined && v3 !="") {
				var conds = v3.split(",");
				v3 = "";
				for (var j = 0; j < conds.length; j++) {
					v3  += "&"+ conds[j] + "=" + getObjValueWithDiv(conds[j], 'target');
				}
			}
			if ($('#'+count[i],$('#target')).parent().attr('fileFlg')=="0") {//image FreeChart

				$('#'+count[i],$('#target')).attr('src',$('#'+count[i],$('#target')).parent().attr('orisrc')+getRandParam() + v3);

			} else if ($('#'+count[i],$('#target')).parent().attr('fileFlg')=="1") {//image ChartDirector

				var url = $('#'+count[i],$('#target')).parent().attr('orisrc')+getRandParam() + v3;
				getQAjaxRunJson('rstfld',false,1,'',url,false,'','');

			} else if ($('#'+count[i],$('#target')).parent().attr('fileFlg')=="2") {//jsChart

				if (v1) {
					var url = $('#'+count[i],$('#target')).parent().attr('orisrc')+getRandParam() + v3 + "&chartType=" + v1 + "&initChart=0";
					getQAjaxRunJson("rstfld",false,1,'',url,false,'','addBIChartHead()');

				} else {
					var url = $('#'+count[i],$('#target')).parent().attr('orisrc')+getRandParam() + v3 + "&initChart=0";
					getQAjaxRunJson("rstfld",false,1,'',url,false,'','addBIChartHead()');
				}
			}
		}
		SF.setServerExecute(true);
	}
}
function chartDirectorControl(o,v) {
	if (v == 0) {
		//no data
		if (o.is(':visible')) {
			o.hide();
			o.parent().css('border','#ccc 1px solid')
					.css('text-align','center')
					.css('vertical-align','middle')
					.append('<span>no result</span>');
		}
	} else {
		//has data
		if (o.is(':hidden')) {
			o.show();
			o.parent().css('border','');
			$("span", o.parent()).remove();
		}
	}

}
function doGetChartCustomize(isPreview) {
	var chartid = $('#WF_CUSTOMIZE-CHARTID').val();
  if ($('#'+chartid,$('#target'))) {
  	$('#'+chartid,$('#target')).get(0).style.height = 'auto';
  	$('#'+chartid,$('#target')).get(0).style.width = 'auto';
  	$('#'+chartid,$('#target')).attr('src','/images/loadingAnimation.gif');
  	v3 = $('#'+chartid,$('#target')).parent().attr('oricond');
  	if (v3 !="") {
  		var conds = v3.split(",");
  		v3 = "";
  		for (var j = 0; j < conds.length; j++) {
  			v3  += "&"+ conds[j] + "=" + encodeURIComponent($("#"+conds[j],$('#target')).val());
  		}
  	}

  	if (!isPreview) {
  		if ($('#'+chartid,$('#target')).parent().attr('fileFlg')=="0") {//image

  			$('#'+chartid,$('#target')).attr('src',$('#'+chartid,$('#target')).parent().attr('orisrc')+getRandParam() + v3);

  		} else if ($('#'+chartid,$('#target')).parent().attr('fileFlg')=="2") {//jsChart

  			var url = $('#'+chartid,$('#target')).parent().attr('orisrc')+getRandParam() + v3 + "&chartType=" + $('#bichart_chartType').val() + "&initChart=1";
  			getQAjaxRunJson("rstfld",false,1,'',url,false,'','addBIChartHead()');
  		}
  	} else {
  		var url = '/s/Chart?initChart=1'+getRandParam() + v3;
  		getQAjaxRunJson("rstfld",false,1,'',url,false,resetSendData(document.chartFrm),'addBIChartHead()');
  	}
  }
}

function splitStr(s,f) {
	var arr;
	if (s.indexof(f)==s.length-1) {
		return s.split(f);
	} else {
		arr[0]=s;
		return arr;
	}
}
String.prototype.trim = function() {
	return this.replace(/^\s+|\s+$/g, "");
}
function resetEnterKey() {
	$('input:text',$("#SearchFrm")).keypress(function(ev) {
		if ((ev.which && ev.which === 13) || (ev.keyCode && ev.keyCode === 13)) {
			if (getObj("searchbtn")) {
				ajaxQuery(1,'0');
				return false;
			} else {
				return false;
			}
		} else {
			return true;
		}
	});
}
function resetEnterKeyWithItems(i,s) {//i:'#zz,#xx';s:'zz'
	$(i).keypress(function(ev) {
		if ((ev.which && ev.which === 13) || (ev.keyCode && ev.keyCode === 13)) {
			if (getObj(s)) {
				$('#'+s).click();
				return false;
			} else {
				return false;
			}
		} else {
			return true;
		}
	});
}
function getRadioValue(objId) {
	return $("input:radio[name="+objId+"]:checked").val();
}
function getRadioValueWithDiv(objId,div) {
	return $("input:radio[id='"+objId+"']:checked",div).val();
}
function getCheckboxValueWithDiv(objId,div) {
	if ($("input:checkbox[id='"+objId+"']",div).attr("checked") == "checked") {
		return "1";
	} else {
		return "0";
	}
}

function setUserSideDate() {
	var holidays = {
		     "20110101":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00080")},
		     "20110110":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00081")},
		     "20110211":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00082")},
		     "20110321":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00083")},
		     "20110429":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00084")},
		     "20110503":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00085")},
		     "20110504":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00086")},
		     "20110505":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00087")},
		     "20110718":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00088")},
		     "20110919":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00089")},
		     "20110923":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00090")},
		     "20111010":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00091")},
		     "20111031":{type:1, title:jQuery.i18n.prop("checkuserjpn.lbl_00092")},
		     "20111103":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00093")},
		     "20111123":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00094")},
		     "20111223":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00095")},
		     "20120101":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00080")},
		     "20120102":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00096")},
		     "20120109":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00081")},
		     "20120211":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00082")},
		     "20120320":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00083")},
		     "20120429":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00084")},
		     "20120430":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00096")},
		     "20120503":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00085")},
		     "20120504":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00086")},
		     "20120505":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00087")},
		     "20120716":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00088")},
		     "20120917":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00089")},
		     "20120922":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00090")},
		     "20121008":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00091")},
		     "20121031":{type:1, title:jQuery.i18n.prop("checkuserjpn.lbl_00092")},
		     "20121103":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00093")},
		     "20121123":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00094")},
		     "20121223":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00095")},
		     "20121224":{type:0, title:jQuery.i18n.prop("checkuserjpn.lbl_00096")}
		};
		$( "#usersidedate" ).datepicker({
		  dateFormat: "yy/mm/dd",
			gotoCurrent: true,
			showButtonPanel: true,
			showMonthAfterYear: true,
		  beforeShowDay: function(day) {
			  var result;
			  var holiday = holidays[$.format.date(day, "yyyyMMdd")]
			  // 祝日・非営業日定義に存在するか？
			  if (holiday) {
				  result =  [true, "date-holiday"+holiday.type, holiday.title];
				} else {
					if (day == new Date()) {
						result = [true, ""];
					} else {
						switch (day.getDay()) {
							case 0: // 日曜日か？
								result = [true, "date-sunday"];
								break;
							case 6: // 土曜日か？
								result = [true, "date-saturday"];
								break;
							default:
								result = [true, ""];
								break;
						}
					}
				}
				return result;
			},
			onSelect: function(dateText, inst) {
				alert(dateText);
			}

		});
}
function setMenuControl() {
	var cntl = $('#controlpanel'),
	coffset = cntl.offset();
	$(window).scroll(function () {
	  if($(window).scrollTop() > coffset.top) {
	  	cntl.css('top', $(window).scrollTop()-coffset.top);
	  } else {
		  cntl.css('top',"");
	  }
	});
}
function LeftMenu(v, change) {
	var a = $('#leftmenuflg').val();
	if (change) {
		if (a=='1' || a=='3') {
			if (getObj('target')) {
				$('#leftmenu').hide(600);
				$("div[id^='dragB']",$('#target')).delay(300).animate({
					left: '-='+v
				},800,function() {
					$('#leftmenuflg').val("0");
					$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 38px 56px 23px);left:-22px" src="/images/main/leftmenu.png"><br>'+
			   			'<img style="position:absolute;clip:rect(0px 47px 56px 40px);top:56px;left:-31px" src="/images/main/leftmenu.png"><br>'+
			   			'<img style="position:absolute;clip:rect(0px 55px 56px 48px);top:112px;left:-39px" src="/images/main/leftmenu.png">');
					var url = urlUserDelete+"?actid=400011&leftmenuflg="+getObj("leftmenuflg").value;
					getQAjaxRunJson("rstfld",false,1,"",url,false,"","");

				});
			} else {
				$('#leftmenu').fadeOut(1000,function() {
					$('#leftmenuflg').val("0");
					$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 38px 56px 23px);left:-22px" src="/images/main/leftmenu.png"><br>'+
		   			'<img style="position:absolute;clip:rect(0px 47px 56px 40px);top:56px;left:-31px" src="/images/main/leftmenu.png"><br>'+
		   			'<img style="position:absolute;clip:rect(0px 55px 56px 48px);top:112px;left:-39px" src="/images/main/leftmenu.png">');
					var url = urlUserDelete+"?actid=400011&leftmenuflg="+getObj("leftmenuflg").value;
					getQAjaxRunJson("rstfld",false,1,"",url,false,"","");
				});
			}
		} else if ((a=='2')||(a=='0')) {
			$('#leftmenu').show(2000);
			if (getObj('target')) {
				$("div[id^='dragB']",$('#target')).each(function() {
					l=$(this).position().left+v;
					$(this)
						.css({
							left: l+"px"
						});
				});
			}
			$('#leftmenuflg').val("1");
			$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 11px 56px 0);" src="/images/main/leftmenu.png"><br>'+
	   			'<img style="position:absolute;clip:rect(0px 17px 56px 12px);top:56px;left:-6px" src="/images/main/leftmenu.png"><br>'+
	   			'<img style="position:absolute;clip:rect(0px 23px 56px 18px);top:112px;left:-12px" src="/images/main/leftmenu.png">');
			var url = urlUserDelete+"?actid=400011&leftmenuflg="+getObj("leftmenuflg").value;
			getQAjaxRunJson("rstfld",false,1,"",url,false,"","");
		}
	} else {
		//init
		if (a=='0') {
			if (getObj('target')) {
				$('#leftmenu').hide(600);
				$("div[id^='dragB']",$('#target')).delay(300).animate({
					left: '-='+v
				},800,function() {
					$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 38px 56px 23px);left:-22px" src="/images/main/leftmenu.png"><br>'+
			   			'<img style="position:absolute;clip:rect(0px 47px 56px 40px);top:56px;left:-31px" src="/images/main/leftmenu.png"><br>'+
			   			'<img style="position:absolute;clip:rect(0px 55px 56px 48px);top:112px;left:-39px" src="/images/main/leftmenu.png">');

				});
			} else {
				$('#leftmenu').fadeOut(1000,function() {
					$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 38px 56px 23px);left:-22px" src="/images/main/leftmenu.png"><br>'+
		   			'<img style="position:absolute;clip:rect(0px 47px 56px 40px);top:56px;left:-31px" src="/images/main/leftmenu.png"><br>'+
		   			'<img style="position:absolute;clip:rect(0px 55px 56px 48px);top:112px;left:-39px" src="/images/main/leftmenu.png">');
				});
			}
		} else if (a=='1') {
			$('#leftmenu').show(2000);
			if (getObj('target')) {
				$("div[id^='dragB']",$('#target')).each(function() {
					l=$(this).position().left+v;
					$(this)
						.css({
							left: l+"px"
						});
				});
			}
			$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 11px 56px 0);" src="/images/main/leftmenu.png"><br>'+
	   			'<img style="position:absolute;clip:rect(0px 17px 56px 12px);top:56px;left:-6px" src="/images/main/leftmenu.png"><br>'+
	   			'<img style="position:absolute;clip:rect(0px 23px 56px 18px);top:112px;left:-12px" src="/images/main/leftmenu.png">');
		} else if (a=='2') {
			if (getObj('target')) {
				$("div[id^='dragB']",$('#target')).hide();
				$('#leftmenu').hide();
				$("div[id^='dragB']",$('#target')).fadeIn(1000,function() {
					$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 38px 56px 23px);left:-22px" src="/images/main/leftmenu.png"><br>'+
			   			'<img style="position:absolute;clip:rect(0px 47px 56px 40px);top:56px;left:-31px" src="/images/main/leftmenu.png"><br>'+
			   			'<img style="position:absolute;clip:rect(0px 55px 56px 48px);top:112px;left:-39px" src="/images/main/leftmenu.png">');
				});
			} else {
				$('#leftmenu').fadeOut(600,function() {
					$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 38px 56px 23px);left:-22px" src="/images/main/leftmenu.png"><br>'+
		   			'<img style="position:absolute;clip:rect(0px 47px 56px 40px);top:56px;left:-31px" src="/images/main/leftmenu.png"><br>'+
		   			'<img style="position:absolute;clip:rect(0px 55px 56px 48px);top:112px;left:-39px" src="/images/main/leftmenu.png">');
				});
			}
		} else {
			$('#leftmenu').show();
			$('#leftmenuhandler').html('<img style="position:absolute;clip:rect(0px 11px 56px 0);" src="/images/main/leftmenu.png"><br>'+
	   			'<img style="position:absolute;clip:rect(0px 17px 56px 12px);top:56px;left:-6px" src="/images/main/leftmenu.png"><br>'+
	   			'<img style="position:absolute;clip:rect(0px 23px 56px 18px);top:112px;left:-12px" src="/images/main/leftmenu.png">');
		}

	}
}
//info-message
function openInfoList() {
	if (!$('#InfoList' ).dialog("isOpen")) {
		$('#InfoList' )
			.dialog( 'option','height',400)
			.dialog( 'option','width',480)
			.dialog( 'option','position',["right","top"]);
		$('#InfoList' ).dialog('open' );
	} else {
		getInfoListPage();
	}
}
function getInfoListPage(){
	//getDetailInfo
	var url = urlUserSearch+"?actid=100018";

	//getQAjaxRunJson(oneFieldId,messageFlg,msgCntlFlg,popflg,lasturl,async,paramdata,nextFunc)
	getQAjaxRunJson("rstfld",true,1,"",url,false,"","");
}
function openMsg(mi) {
	openFuncDiag(jQuery.i18n.prop("msg.ttl_0000002"),"/user/msg/umsg007.jsp?msgId="+mi,"$('#MsgDetailDialog').dialog('moveToTop');umsg007_initAddrDialog();",700,500,'5','MsgDetailDialog');
}
function getNewMsgPage(mi) {
	//getDetailInfo for reply
	openFuncDiag("","/user/msg/umsg004.jsp?msgId="+mi,"umsg004_initMsgDialog();$('#MsgDialog' ).dialog('moveToTop' );",700,530,'5','MsgDialog');
}
function openNewMsg() {
	openFuncDiag(jQuery.i18n.prop("msg.ttl_0000001"),"/user/msg/umsg004.jsp?msgId=-1","umsg004_initMsgDialog();",650,550,'5','MsgDialog');
}
function repalceAll(ex, org, dest) {
	return ex.split(org).join(dest);
}
String.prototype.replaceAll = function (org, dest) {
	return this.split(org).join(dest);
}
function replaceFullWidthNum(s) {
	var i;
    for(i=0;i<10;i++) s=s.replace(new RegExp(new Array('０','１','２','３','４','５','６','７','８','９')[i],'g'),i);
    return s;
}
function isMac() {
	var ua = navigator.userAgent.toUpperCase();
	if (ua.indexOf('MAC')>=0) {
		return true;
	} else {
		return false;
	}
}
function openMailer(m,s,b,c) {
	if (isMac()) {
		b = b.replaceAll("\n","%0d%0a");
		b = b.replaceAll(" ","%20");
		b = b.replaceAll("?","%3f");
		location.href = "mailto:"+m+"?subject="+s+"&body="+b;
	} else {
		var url = '';
		if (c) {
			url = urlUserSearch+"?actid=100059&m="+encodeURIComponent(m)+"&s="+encodeURIComponent(s)+"&b="+encodeURIComponent(b)+"&c="+c;
		} else {
			url = urlUserSearch+"?actid=100059&m="+encodeURIComponent(m)+"&s="+encodeURIComponent(s)+"&b="+encodeURIComponent(b);
		}
		//getQAjaxRunJson(oneFieldId,messageFlg,msgCntlFlg,popflg,lasturl,async,paramdata,nextFunc)
		getQAjaxRunJson("rstfld",false,1,"",url,false,"","");
	}
}
function ialert(m) {
	alert(m);
}
function iconfirm(m, fun) {
	var flg = confirm(m);
	if (flg) {
		ajaxDoAddExeJs(fun, "saasForceConfirm=1");
	}
	return flg;
}
function mouseCoords(ev){
    if(ev.pageX || ev.pageY){
        return {x:ev.pageX, y:ev.pageY};
    }
    return {
        x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,
        y:ev.clientY + document.body.scrollTop  - document.body.clientTop
    };
}
function addBIChartHead() {
	$("div.GChart, div.gvChart").each(function() {
		$('<p class="ui-widget-header">Menu</p>')
			.css({
				top: "-10px", left: "0px",
				position: "absolute", opacity: "0.5", zIndex: 800
			})
			.appendTo($(this));
    	$('p.ui-widget-header', $(this)).click(function(e) {
    		$('#WF_CUSTOMIZE-CHARTID').val($(this).parent().attr('id'));
    		$('#bichart_chartType',$('#target')).val('');
    		$('#bichart_chartKind',$('#target')).val('');
    		var mousePos  = mouseCoords(e);
			$(".bichart-menu").
				css({"left": mousePos.x-20 + "px",
					 "top": mousePos.y + "px" });
			$(".bichart-menu").show();
			$(".bichart-menu-item").show();
		});
	});
	$("p.ui-widget-header")
		.mouseover(function(){
			$(this).css({
					position: "absolute", opacity: "1", zIndex: 800
				})
				;
			});
	$("p.ui-widget-header")
		.mouseout(function(){
			$(this).css({
					position: "absolute", opacity: "0.5", zIndex: 800
				})
				;
		});
}
function openDetailChartDefn(i) {
	var pageid = $('#PageID').val();
	var subid = $('#'+$('#WF_CUSTOMIZE-CHARTID').val()).attr('_subid');
	var assurl;
	if (!$('#PropertyDiv' ).dialog("isOpen")) {
		$('#PropertyDiv').html('');
		$('#PropertyDiv').unbind( "dialogopen");
		$('#PropertyDiv').bind( "dialogopen", function(event, ui) {
			$('#PropertyDiv' ).dialog( 'option','title','Chart Customize');
			assurl = "/user/action/chart/ucht001.jsp?pageID="+pageid+"&subid="+subid+"&numID="+getObj('bichart_chartnumID').value;
			getQAjaxRun("rstfld1",true,assurl,true,"","ucht001_initProDialog()","5","PropertyDiv","div");
		});
		width = 600;
		height = 440;
		$('#PropertyDiv' )
			.dialog( 'option','width',width)
			.dialog( 'option','height',height);
		$('#PropertyDiv' ).dialog('open' );
		$('.bichart-menu-item').fadeOut(500);
	}
}
function delDetailChartDefn() {
	var pageid = $('#PageID').val();
	var subid = $('#'+$('#WF_CUSTOMIZE-CHARTID').val()).attr('_subid');
	var url;
	url = urlUserDelete;
	getQAjaxRunJson("rstfld",true,1,"",url,false,"actid=190003&opflg1=7&pageID="+pageid+"&chartID="+subid+"&numID="+getObj('bichart_chartnumID').value,"doGetChartCustomize();");
	$('.bichart-menu-item').fadeOut(500);
}
function setOption(oid,optionstr,isMust) {//dropdownlist選択値設定
	if (document.getElementById(oid)){
		var opName = new Array();
		opName = optionstr.split(",");
		document.getElementById(oid).innerHTML ="";
		if (isMust==undefined || !isMust) {
			document.getElementById(oid).options.add(new Option("", ""));
		}
		for (i = 0; i < opName.length-1; i++) {
			var op =  opName[i].split("#");
			document.getElementById(oid).options.add(new Option(op[1], op[0]));
		}
	}
}
function doGantData(i,j) {//ganttchart menu
	$('#ganttchart_moveflg_prev').val($('#ganttchart_moveflg').val());
	$('#ganttchart_sortitem_prev').val($('#ganttchart_sortitem').val());
	$('#ganttchart_finish_prev').val($('#ganttchart_finish').val());
	$('#ganttchart_period_prev').val($('#ganttchart_period').val());
	$('#ganttchart_basedate_prev').val($('#ganttchart_basedate').val());
	if (i=='0') {
		if (j=='0') {
			$('#ganttchart_moveflg').val('1');
		} else if (j=='1') {
			$('#ganttchart_moveflg').val('2');
		} else if (j=='2') {
			$('#ganttchart_moveflg').val('3');
		} else if (j=='3') {
			$('#ganttchart_moveflg').val('');
		}
	} else if (i=='1') {
		if (j=='0') {
			$('#ganttchart_sortitem').val('1');$('#ganttchart_moveflg').val('0');
		} else if (j=='1') {
			$('#ganttchart_sortitem').val('2');$('#ganttchart_moveflg').val('0');
		} else if (j=='2') {
			$('#ganttchart_sortitem').val('3');$('#ganttchart_moveflg').val('0');
		}
	} else if (i=='2') {
		if (j=='0') {
			$('#ganttchart_finish').val('1');$('#ganttchart_moveflg').val('0');
		} else if (j=='1') {
			$('#ganttchart_finish').val('2');$('#ganttchart_moveflg').val('0');
		} else if (j=='2') {
			$('#ganttchart_finish').val('');$('#ganttchart_moveflg').val('0');
		}
	} else if (i=='3') {
		if (j=='0') {
			$('#ganttchart_period').val('1');
		} else if (j=='1') {
			$('#ganttchart_period').val('2');
		} else if (j=='2') {
			$('#ganttchart_period').val('3');
		}
	}
	$("span",$("ul#ganttchart-menu-item > li:nth-child("+(parseInt(i)+1)+") > ul")).removeClass("ui-icon ui-icon-check");
	$("span",$("ul#ganttchart-menu-item > li:nth-child("+(parseInt(i)+1)+") > ul > li:nth-child("+(parseInt(j)+1)+")")).addClass("ui-icon ui-icon-check");
	doGetGantData();
	$(".ganttchart-menu").hide();
}
function setPrevGantCond() {
	$('#ganttchart_moveflg').val($('#ganttchart_moveflg_prev').val());
	$('#ganttchart_sortitem').val($('#ganttchart_sortitem_prev').val());
	$('#ganttchart_finish').val($('#ganttchart_finish_prev').val());
	$('#ganttchart_period').val($('#ganttchart_period_prev').val());
	$('#ganttchart_basedate').val($('#ganttchart_basedate_prev').val());
	doGetGantData();
}
function doChartCustomize(i,j) {
	if (i=='0') {
		if (j=='0') {
			$('#bichart_chartType').val('0');
		} else if (j=='1') {
			$('#bichart_chartType').val('2');
		} else if (j=='2') {
			$('#bichart_chartType').val('7');
		} else if (j=='3') {
			$('#bichart_chartType').val('3');
		} else if (j=='4') {
			$('#bichart_chartType').val('6');
		} else if (j=='5') {
			$('#bichart_chartType').val('5');
		}
	} else if (i=='1') {
		if (j=='0') {
			$('#bichart_chartKind').val('1');$('#ganttchart_moveflg').val('0');
		} else if (j=='1') {
			$('#bichart_chartKind').val('2');$('#ganttchart_moveflg').val('0');
		}
	}
	doGetChartCustomize();
	$('.bichart-menu-item').fadeOut(1000);
}
function closePopWindow() {
//	window.opener = window;
//	var win = window.open("","_self");
	window.close();
}
function getTrueFlg(v) {
	if (undefined==v) {
		return true;
	}
	return v;
}
function addComma(str) {
	var num = new String(str).replace(/,/g, "");
	while(num != (num = num.replace(/^(-?\d+)(\d{3})/, "$1,$2")));
	return num;
}
function clearComma(str) {
	return new String(str).replace(/,/g, "");
}
//日付計算関数
function dateAdd(cat,add,ymd,format){
	var result_ymd;
	ymd = new Date(ymd);
	if(cat=="d"){
		result_ymd = new Date(ymd.getFullYear(), ymd.getMonth(), ymd.getDate() + (add * 1));
	}else if(cat=="m"){
		result_ymd = new Date(ymd.getFullYear(), ymd.getMonth() + (add * 1), ymd.getDate());
	}else if(cat=="y"){
		result_ymd = new Date(ymd.getFullYear() + (add * 1), ymd.getMonth(), ymd.getDate());
	}
	if (format == undefined || format == '') {
		return $.format.date(result_ymd,'yyyy/MM/dd');
	} else {
		return $.format.date(result_ymd,format);
	}
}
function ChangeTime(tmpTime) {
	 var dblTime = -1;
	 var bTimes,bHour,bMin,bSec,bAllSec;

	 if (tmpTime != null && tmpTime != "") {
	   bTimes = tmpTime.split(":");
	   if (parseInt(bTimes.length,10)>=2) {
	     bHour = bTimes[0];
	     bMin = bTimes[1];

	     bAllSec=parseInt(bMin,10)+(parseInt(bHour,10)*60)

	     dblTime = Math.round((bAllSec/60)*100)/100;
	   }
	 }
	 return dblTime;
}
//Popwin------start--------
var po = $("#PopDiv");
var to = $("#target");
var f;

function clearParam(){
	$selected = $("input:text[class!='readonly'],input:checkbox,select",$("#PopDiv"));
	var t;
	for (var i = 0; i < $selected.length; i++) {
		t = $selected[i];
		$(t).val("");
	}
	$("#result",$("#PopDiv")).html("")
	$("#infomsg",$("#PopDiv")).html("")
}

function returnParam(v){
	var objArrID = $("#returnID",$('#PopDiv')).val();
	var selfID = "O-" +$("#selfID",$('#PopDiv')).val();
	var values,objs,tob;
	var objID ,row;
	var clearFlg = "0";
	objs = objArrID.split(',');
	values = v.split('%WF,WF%');
	if ($("#ugridID",$('#PopDiv')).val()!="") {
		row = $("#SelGirdRow").val();
		if (row != "") {
			var c,oldValue,flg;
			c = $("#ugridID",$('#PopDiv')).val() + "flg" + row;
			flg = $("#"+c,$("#target")).val();
			selfID += "_"+ row;
			for( i=0; i <objs.length; i ++ ) {
				objID = objs[i] + "_"+ row;
				if (getObj(objID)) {
					tob = $("#"+objID,$("#target"));
					if (tob.length) {
						if (selfID == objID ) {
							//if (tob.hasClass("ErrStyle"))
							//	tob.removeClass("ErrStyle");
							oldValue = tob.val();
							if (oldValue != values[i]) {
								clearFlg = "1";
							}
							if (flg!="2") {
								if (oldValue != values[i]) {
									$("#"+c,$("#target")).val("1");
								}
							}
						}
						tob.val(values[i]);
						if (selfID == "O-"+objID) {
							$("#"+selfID,$("#target")).val(values[i]);
						}
					}
				}
			}
		}
	} else {
		for( i=0; i <objs.length; i ++ ) {
			objID = objs[i];
			if (getObj(objID)) {
				tob = $("#"+objID,$("#target"));
				if (tob.length) {
					if( clearFlg == "0"
						&& tob.val() != values[i]) {
						clearFlg = "1";
					}
					if (selfID == objID ) {
						//if (tob.hasClass("ErrStyle"))
						//	tob.removeClass("ErrStyle");
					}
					tob.val(values[i]);
					if (selfID == "O-"+objID) {
						$("#"+selfID,$("#target")).val(values[i]);
					}
				}
			}
		}
	}

	if (clearFlg == "1") {
		var clParam = $('#clearID',$('#PopDiv')).val();
		if (clParam != "") {
			mainCntlValueClear(clParam);
		}
	}
	$("#PopDiv").dialog('close');
	$("#PopDiv").html("");
	$("#pop").remove();
}
function ClearValue(){
	$("#PopDiv").dialog('close');
	$("#PopDiv").html("");
	$("#pop").remove();
}
function mainCntlValueClear(v){
	var objMixID = v.split(",");
	var objIDs;
	var objID = "";
	var gobjID = "";
	var line = 0;
	var v1 = "0";
	if ($("#ugridID",$('#PopDiv')).val()!="") {
		v1 = "1";
	}
	for (i = 0; i < objMixID.length-1; i++) {
		objIDs = objMixID[i].split(":");
		objID = objIDs[0];
		tob = $("#"+objID,$("#target"));
		if(v1 == "0") {
			if (objIDs[1] == "0") {
				if (tob.length) {
					tob.val("");
					if ($("#O-" + objID,$("#target"))) {
						$("#O-" + objID,$("#target")).val("");
					}
				}
			} else {
				gobjID = "RowGrid" + objIDs[2];
				line = $("#"+gobjID,$("#target")).val();
				for (j = 1; j <= line; j++) {
					if ($("#"+objID+ "_" + j,$("#target"))) {
						$("#"+objID+ "_" + j,$("#target")).value = "";
						if ($("#O-" + objID+ "_" + j,$("#target"))) {
							$("#O-" + objID+ "_" + j,$("#target")).val("");
						}
					}
				}
			}
		} else {
			line = $("#SelGirdRow",$('#PopDiv')).val();
			if ($("#"+objID + "_" +line,$("#target"))) {
				$("#"+objID+ "_" +line,$("#target")).val("");
				if ($("#O-" + objID+ "_" +line,$("#target"))) {
					$("#O-" + objID+ "_" +line,$("#target")).val("");
				}
			}
		}
	}
}
//Popwin-----end--------
//MultiSearch start
function addMultiSearchHandler() {
	$("li.wf_user_search_patterns").each(function() {
		$('<p class="wf_user_search_edit"><img style=\'width:10px;height:10px\' src=\'/images/icon/pen.gif\'></p>')
			.css({
				top: "-10px", left: "0px", width:"10px", height:"10px",
				position: "absolute", opacity: "0.5", zIndex: 1,
        display: "none"
			})
			.appendTo($(this));
		$('<p class="wf_user_search_del"><img style=\'width:10px;height:10px\' src=\'/images/icon/delete.gif\'></p>')
		.css({
			top: "-10px", left: $(this).width(), width:"10px", height:"10px",
			position: "absolute", opacity: "0.5", zIndex: 1,
      display: "none"
		})
		.appendTo($(this));
	})
  .mouseout(function() {
      $("p",$(this)).hide();
      $(this).addClass("ui-state-default");
      $(this).removeClass("ui-state-highlight");
    })
  .mouseover(function() {
      $("p",$(this)).show();
      $(this).addClass("ui-state-highlight");
      $(this).removeClass("ui-state-default");
    })
  .click(function() {
    ajaxDoGetSearch($(this).get(0).id);
  });

	$("p.wf_user_search_edit")
		.click(function() {
			openSearchPattern($(this).parent().get(0).id, $(this).parent().text());
			return false;
		})
		.mouseover(function(){
			$(this).css({
					opacity: "1", zIndex: 800
				})
				;
			})
		.mouseout(function(){
			$(this).css({
					opacity: "0.5"
				})
				;
		});
	$("p.wf_user_search_del")
		.click(function() {
			delSearchPattern($(this).parent().get(0).id);
			return false;
		})
		.mouseover(function(){
			$(this).css({
					opacity: "1", zIndex: 800
				})
				;
			})
		.mouseout(function(){
			$(this).css({
					opacity: "0.5", zIndex: 1
				})
				;
		});
}
function ajaxDoGetSearch(p){
	$("#errmsg").html("");
  if ($('#ErrDialog' ).dialog("isOpen")) {
		$( '#ErrDialog' ).dialog( 'close' );
	}
	var url = urlUserSearch+"?actid=100057&PageID="+getObj("PageID").value+"&patternID="+p;
  getQAjaxRunJson("rstfld",false,1,"",url,true,"","ajaxQuery(1,'0');");
  $('.multisearch_menu_item').fadeOut(500);

}
function ajaxDoAddSearch(){
	var oriActid = $("#actid",$("#SearchDiv")).val();
  if ($("#rename_searchpatternid",$('#SearchPatternDialog' )).val()=='') {
  	$("#actid",$("#SearchDiv")).val("100056");
  } else {
   	$("#actid",$("#SearchDiv")).val("100057");
  }
  if ($('#rename_searchpatternname',$('#SearchPatternDialog' )).val()=='') {
    alert($.i18n.prop("inup013.msg0001"));
    $('#rename_searchpatternname',$('#SearchPatternDialog' )).focus();
    return false;
  }
	var url = urlUserEdit;
	getQAjaxRunJson("rstfld",false,1,"",url,true,setSendData(document.SearchFrm)+"&"+setSendDivData('SearchPatternDialog'),"$('#actid',$('#SearchDiv')).val('"+oriActid+"');$( '#SearchPatternDialog' ).dialog( 'close' );");
}
function delSearchPattern(p) {
	$("#errmsg").html("");
  if ($('#ErrDialog' ).dialog("isOpen")) {
		$( '#ErrDialog' ).dialog( 'close' );
	}
	var url = urlUserDelete+"?actid=100057&PageID="+getObj("PageID").value+"&patternID="+p;
  getQAjaxRunJson("rstfld",false,1,"",url,true,"","");
}
function renameSearchPattern() {
	$("#errmsg").html("");
  if ($('#ErrDialog' ).dialog("isOpen")) {
		$( '#ErrDialog' ).dialog( 'close' );
	}
	var url = urlUserEdit+"?actid=100057&PageID="+getObj("PageID").value;
  getQAjaxRunJson("rstfld",false,1,"",url,true, setSendDivData('SearchPatternDialog'), "$( '#SearchPatternDialog' ).dialog( 'close' );");
}
function openSearchPattern(p, n) {
	$("#errmsg").html("");
  if ($('#ErrDialog' ).dialog("isOpen")) {
		$( '#ErrDialog' ).dialog( 'close' );
	}
  $("#rename_searchpatternid").val(p);
  $("#rename_searchpatternname").val(n);
  if (!$('#SearchPatternDialog' ).dialog("isOpen")) {
		$( '#SearchPatternDialog' ).dialog( 'open' );
	}
}
//MultiSearch end
//-------sys start---
function chgsys() {
	getObj("systoid").value = getObj("systo").value;
	document.hf.submit();
}
//-------sys end---
function ajaxDoAddExeJs(v, param, showLoading, triggerObj, afterFun ){
	$(".ErrStyle").removeClass("ErrStyle");
	if ($("#ServerScriptFlg").length > 0) {
		$("#ServerScriptFlg").val("1");
		$("#ServerScriptID").val(v);
	}
	if (triggerObj) {
		$("#triggerID").val(triggerObj.attr("id"));
	}

	var url = urlUserScript;
	if (param && param !="") {
		url += "?" + param;
	}
	if (afterFun==undefined) {
		afterFun = "";
	}
	getQAjaxRunJson("rstfld",false,1,"",url, true,setSendData(document.form1),afterFun, showLoading);
}
function ajaxDoAddExeJsWithSelectedGridRow(v, param, showLoading, triggerObj, afterFun ){
	$(".ErrStyle").removeClass("ErrStyle");
	if ($("#ServerScriptFlg").length > 0) {
		$("#ServerScriptFlg").val("1");
		$("#ServerScriptID").val(v);
	}
	if (triggerObj) {
		$("#triggerID").val(triggerObj.attr("id"));
	}

	var url = urlUserScript;
	if (param && param !="") {
		url += "?" + param;
	}
	if (afterFun==undefined) {
		afterFun = "";
	}
	getQAjaxRunJson("rstfld",false,1,"",url, true,setSendDataWithSelectedGridRow(document.form1),afterFun, showLoading);
}
function logout(u){
	sessionStorage.clear();
  if (u == undefined || u == ''|| u == ' ') {
  	window.top.location.href="/WFLogout.jsp";
  } else {
  	window.top.location.href=u;
  }
}
function rejectHankaku(o) {
	$(o).keydown(function(ev) {
		if ((ev.which && ev.which === 229) || (ev.keyCode && ev.keyCode === 229)) {
			event.returnValue = false;
		}
	});
}
function enter2tab() {
	$("input:text,input:password,input:radio,input:checkbox,textarea", $("#target")).keydown(function(ev) {
		if ((ev.which && ev.which === 13) || (ev.keyCode && ev.keyCode === 13)) {

			if (window.event) {
				event.keyCode = 9;
			} else {
				ev.preventDefault();
				ev.which.keyCode = 9;
			}
		}
	});
}
/*-----------------------------------------------------------------------------
============================================================
openSubWin( field, label, focus )
============================================================
引数: url - url名
	: paramString  パラメータ文字
	: height width　top　left
	: formart
機能: サーブウィンドウを開く。
-----------------------------------------------------------------------------*/
function openSubWin(url,paramString,height,width,top,left,formart,winID){
	if (formart ==undefined|| formart =="") {
		formart ="toolbar=no,menubar=no,scrollbars=yes, resizable=yes,location=no,status=yes";
	}
	if (top ==undefined) {
		top =1;
	}
	if (left ==undefined) {
		left =1;
	}
	if (height ==undefined || height==0) {
		height =window.screen.height;
	}
	if (width ==undefined || width==0) {
		width =window.screen.width;
	}
	formart = "height="+height+",width="+width+",top="+top+",left="+left+","+ formart;
	var nst=  url + "?" + paramString;

	if (winID ==undefined || winID =="")  winID = "showtarget";
	var OpenWindow=window.open(nst,winID,formart);
	return OpenWindow;
}

function getTableRowCnt(tdObj) {
	var rowcnt;
	rowcnt = (tdObj.parent().prevAll().length + 1) /2 - 1;
	if($.browser.msie){
		 if($.browser.version == "8.0" || $.browser.version == "9.0"){
			 rowcnt = (tdObj.parent().prevAll().length + 1) /2;
		 } else if($.browser.version == "10.0"){
			 rowcnt = (tdObj.parent().prevAll().length + 1) /2 - 1;
		 }
	}
	return rowcnt;
}

function subSpaceAndChangeFullNumberToSingle(value) {
	var bigSpace = "　";
	var newValue = "";
	var bigNumber = "０１２３４５６７８９";
	if (value != "") {
		for (var i = 0; i < value.length; i++) {
			var varChar = $.trim(value.charAt(i));
			if (varChar == bigSpace || varChar == "") {
				newValue += "";
			} else {
				var index = bigNumber.indexOf(varChar);
				if (index > -1) {
					newValue += index;
				} else {
					newValue += varChar;
				}
			}
		}
	}
	return newValue;
}

function getAttr(attr, inputID) {
	if ("" != attr) {
		var attrArray = attr.split("|");
		for (var i = 0; i < attrArray.length; i++) {
			var key = attrArray[i].split("&")[0];
			var value = attrArray[i].split("&")[1];
			if (key == inputID) {
				return value;
			}
		}
	}
	return "";
}

function setNewAttr(attr, inputID, elementID, propertyKey, newValue) {
	var newAttr = "";
	if ("" != attr) {
		var attrArray = attr.split("|");
		for (var i = 0; i < attrArray.length; i++) {
			var key = attrArray[i].split("&")[0];
			var value = attrArray[i].split("&")[1];
			if (key == inputID) {
				newAttr += key + "&" + newValue + "|";
			} else {
				newAttr += key + "&" + value + "|";
			}
		}
	}
	if (newAttr != "") {
		newAttr = newAttr.substring(0, newAttr.length - 1);
	}
	SF.setItemAttributes(elementID, propertyKey, newAttr);
}

function setChangedValueTdBgColor(oldAttr, newAttr, inputID, value, backgroundColor) {
	if (typeof (oldAttr) != 'undefined' && oldAttr != '') {
		var oldAttrArray = oldAttr.split("|");
		var newAttrArray = newAttr.split("|");
		for (var i = 0; i < oldAttrArray.length; i++) {
			var oldValues = oldAttrArray[i].split("&");
			var oldValuesKey = oldValues[0];
			var keyArray = oldValuesKey.split("@");
			var key = keyArray[keyArray.length - 1];
			var oldValuesValue = oldValues[1];
			var addFlg;

			if (oldValuesKey == inputID) {
				if (parseInt(oldValuesValue, 10) != value) {
					$("#" + key).parent().css("background-color", backgroundColor);
					addFlg = true;
				} else {
					$("#" + key).parent().css("background-color", 'transparent');
					addFlg = false;
				}
				setChangedValue(inputID, addFlg);
			}

		}
	}
}

function setChangedValue(changedValueInputID, addFlg) {
	var changedValue = $.trim($("#changedTextItem").val());
	if (addFlg && changedValue == "") {
		changedValue = changedValueInputID;
	} else {
		if (changedValue != "") {
			if (addFlg) {
				if (!isExists(changedValue, changedValueInputID)) {
					changedValue += "|" + changedValueInputID;
				}
			} else {
				changedValue = getNewValue(changedValue, changedValueInputID);
			}
		}
	}

	$("#changedTextItem").val(changedValue);
}

function isExists(value1, value2) {
	if (value1 != "") {
		var valueArray = value1.split("|");
		for (var i = 0; i < valueArray.length; i++) {
			if (valueArray[i] == value2) {
				return true;
			}
		}
	}
	return false;
}

function getNewValue(value1, value2) {
	var newValue = "";
	if (value1 != "") {
		var valueArray = value1.split("|");
		for (var i = 0; i < valueArray.length; i++) {
			if (valueArray[i] != value2) {
				newValue += valueArray[i] + "|";
			}
		}
		newValue = newValue.substring(0, newValue.length - 1);
	}
	return newValue;
}

function addFormLoadEvent(id, eventName) {
	$("#" + id).on(eventName, function() {
	    var value = $(this).val();
	    $(this).val(value.replaceAll("'", ""));
	});
}
/*-----------------------------------------------------------------------------
============================================================
checkPwdType()
引数	: field
		: msg
戻り値	: true : ある
		: false : なし
機能	: 引数で大文字、小文字、数字、特別文字列であるかどうかを判断する。
-----------------------------------------------------------------------------*/
function checkPwdType(field, msg) {
	// 文字種チェック
	var postalCodeChars1 = "0123456789";
	var postalCodeChars2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	var postalCodeChars3 = "abcdefghijklmnopqrstuvwxyz";
	// 2014/12/22 ei 特別文字列を対応
	var postalCodeChars4 = "\"#$%&'()*+,-./:;<=>?@\_!";
	var i;
	var len1 = 0;
	var len2 = 0;
	var len3 = 0;
	// 2014/12/22 ei 特別文字列を対応
	var len4 = 0;
	for (i=0; i<field.value.length; i++) {
		if (postalCodeChars1.indexOf(field.value.charAt(i),0)!=-1) {
			len1++;
		}
		if (postalCodeChars2.indexOf(field.value.charAt(i),0)!=-1) {
			len2++;
		}
		if (postalCodeChars3.indexOf(field.value.charAt(i),0)!=-1) {
			len3++;
		}
		// 2014/12/22 ei 特別文字列を対応
		if (postalCodeChars4.indexOf(field.value.charAt(i),0)!=-1) {
			len4++;
		}

	}
	// 2014/12/22 ei 特別文字列を対応
	if (len1==0||len2==0||len3==0||len4==0) {
		alert(msg);
		return false;
	}

	return true;
}

/*-----------------------------------------------------------------------------
============================================================
checkPwdMoji()
引数	: field
		: msg
戻り値	: true : ある
		: false : なし
機能	: パスワードに無効な文字が入力された
変更履歴： 2014/12/22 永
-----------------------------------------------------------------------------*/
function checkPwdMoji(field, msg) {
	// 文字種チェック
	var postalCodeChars1 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\"#$%&'()*+,-./:;<=>?@\_!";
	var i;
	var len1 = 0;
	for (i=0; i<field.value.length; i++) {
		if (postalCodeChars1.indexOf(field.value.charAt(i),0)==-1) {
			len1++;
		}
	}
	if (len1!=0) {
		alert(msg);
		return false;
	}

	return true;
}

function isContain(str1, str2) {
	if (str1.indexOf(str2) != -1) {
		return true;
	} else {
		return false;
	}
}

function pageOutExcel(i, data){
	var top=50;//(document.body.scrollTop + window.event.y)/2;
	var left=100;//document.body.scrollLeft + window.event.x;
	var width=500;
	var height=width/1.6;

	if (i==7) {
		var nst="/s/AuthWatch?f=A&"+data;
		var OpenWindow=window.open(nst,"pretarget","height="+height+",width="+width+",top="+top+",left="+left+",toolbar=no,menubar=no,scrollbars=yes, resizable=yes,location=no,status=no");
	}
}
//get refer data value
function ajaxQueryGridVal(reqName,tagetSubID,tagetObj,o,v){
  var row = getGridRowIndex(o,"rowseq");
  tagetObj = tagetObj +"_" +row;
  ajaxQueryVal(reqName,tagetSubID,tagetObj,v);
}
function ajaxQueryVal(reqName,tagetSubID,tagetObj,v){
  $(".ErrStyle").removeClass("ErrStyle");
  getObj("TargetObj").value = tagetObj;
  if (getObj(tagetObj)){
    getObj(tagetObj).value = "";
  }
  refObj = tagetObj;
  var conf = "";
  if (v == "1") {
    conf =  getRadioValue(reqName);
  } else {
    conf = getObj(reqName).value;
  }
  if (conf =="") {
    return false;
  }
  var pageid = getObj("PageID").value;
  var url = urlUserSearch + "?actid=100015&PageID="+ pageid+"&targetSubID="+tagetSubID+"&pringFlg=4"+"&targetObj="+tagetObj+"&conf="+conf;
  getQAjaxRunJson("rstfld",false,1,"",url,false,"","changeRefSpecHtml($('#"+refObj+"'));");

}
//dosave
function doSave(){
  if (inputDataCheck()) {ajaxDoSave()}
  else {SF.setServerExecute(true)}
}

function ajaxDoSave() {
  if (!checkSpecialInput()) {
    return false;
  }
  getObj('WF_RUNRESULT') =='0';
  getQAjaxRunJson("rstfld",true,1,"",urlUserEdit,true,setSendData(document.form1),"");
}
function inputDataCheck(){
  $(".ErrStyle").each(function () {
    var _this = $(this);
    var parentObj = _this.parent(".WF_STABLE_CLASS_TH , .WF_STABLE_CLASS_TD");
    var isStaticTableItem = (parentObj.length > 0);
    _this.removeClass("ErrStyle");
    if (isStaticTableItem) {
      parentObj.css("background-color", "");
    }
  });
   if (popErrCheck()) {
     if(DoMustCheckPcs())
       if (DoDataCheckPcs())
         return DoBeforeSave();
       else
         return false;
     else
       return false;
   } else {
     return false;
   }
  return true
}
function DoMustCheckPcs(){
  SF.setCheckSuccess(true);
  var doMustFlg = true;
  doMustFlg = DoMustCheck();
  if(doMustFlg == null || doMustFlg || doMustFlg == undefined || doMustFlg == "undefined") {
    eval(SF.getMustCheckData());
    if (!SF.isCheckSuccess()) {
      alert(jQuery.i18n.prop("com.msg_1000803"));
      SF.setServerExecute(true);
      return false;
    }
    return true;
  } else {
    return false;
  }
}
function DoDataCheckPcs() {
  DoDataCheck();
  eval(SF.getItemCheckData());
  if (!SF.isCheckSuccess()) {
  	alertMsg = alertMsg.replace(/#n#/g, '\n')
    alert(alertMsg);
    alertMsg = "";
    SF.setCheckSuccess(true);
    return false;
  }
  return true;
}
function popErrCheck(){
  var errObj = $("#filterError").val();
  if (errObj == "") {
    return true;
  } else {
    var errObjs = errObj.split(",");
    var msgMix,codeObjID;
    var val1,val2;
    for (var i=0;i<errObjs.length;i++) {
      msgMix = errObjs[i].split(":");
      if (getObj(msgMix[0])) {
        codeObjID = msgMix[0].substring(2,msgMix[0].length);
        val1 = getObj(msgMix[0]).value;
        if (getObj(codeObjID)) {
          val2 = getObj(codeObjID).value;
        }
        if (val1 !="" && val2 =="") {
          alert(msgMix[1]+jQuery.i18n.prop("checkuserjpn.lbl_00079"));
          return false;
        }
      }
    }
    return true;
  }
}
//filter
function ajaxDoGridFilterList(tagetSubID,tagetObj,o, nextFunc){
  var row = getGridRowIndex(o,"rowseq");
  tagetObj = tagetObj +"_" +row;
  $("#filterRow").val(row);
  ajaxDoFilterList(tagetSubID,tagetObj,nextFunc,row);
}
function ajaxDoFilterList(tagetSubID,tagetObj,nextFunc,row,async){
  $("#filterID").val(tagetSubID);
  $("#pringFlg").val("3");
  if (getObj(tagetObj)){
    $("#"+tagetObj).html("");
    $option = $('<option>')
      .val("")
      .text("");
    $("#"+tagetObj).append($option);
    //document.getElementById(tagetObj).options.add(new Option('', ''));
    SF.setComboboxIndex(tagetObj, 0);
  }
  refObj= "&WF_FILTER_TARGET="+tagetObj;
  var url = urlUserSearch;
  var showLoading = true;
  if (nextFunc == undefined || nextFunc == "") {
    afterFun = "SF.resetDropdownListOptionStyle('" + tagetObj + "');";
  } else {
    afterFun = "SF.resetDropdownListOptionStyle('" + tagetObj + "');"+nextFunc;
  }
  if (async == undefined) {
	  async = true;
  }
  if (row != undefined && row != "") {
	  getQAjaxRunJson("rstfld1",false,1,"",url,async,setSendDataForFilter("form div[depth=0],div[id^='_ingrid_Grid'][id$='_b'] tr[id=rowseq"+row+"]")+refObj,afterFun,showLoading);
  } else {
	  getQAjaxRunJson("rstfld1",false,1,"",url,async,setSendDataForFilter("form div[depth=0],body div:not(:hidden) div[depth=0]")+refObj,afterFun,showLoading);
  }
}
//do server script with transfer parameters by div
function ajaxDoServerJs(v, param, div, showLoading, afterFun){
  $(".ErrStyle").removeClass("ErrStyle");
  getObj("ServerScriptFlg").value= "1";
  getObj("ServerScriptID").value= v;
  var url = urlUserScript;
  var divs = "";
  if (div != undefined) {
    divs = setSendDivDataForSearch(div);
  }
  if (afterFun==undefined) {
    afterFun = "";
  }
  getQAjaxRunJson("rstfld",false,1,"",url, true,setSpecData(param)+divs,afterFun,showLoading);
}
//do smart search for vue
function doSmartSearchJson(v1,v2,v3,afterFunc) {
	$(".ErrStyle").removeClass("ErrStyle");
	getObj("pringFlg").value = "2";
	$("#triggerID").val($("input[_subid="+v1+"]").attr("name"));
	getObj("SubID").value = v1;
	var url,data;
	if (v2!="") {
		var count = v2.split(",");
		for (var i = 0; i < count.length; i++) {
			sendcode = "7";
			//displayObj = "_ingrid_Grid" +count[i]+"_0";
			displayObj = "dragB" +count[i];
			url = "/user/ajaxUser/XRRunSmartSearch.jsp";
			data = "toSubID="+count[i]+"&actflg="+v3+"&targetID="+displayObj+"&"+setSearchSendData(document.form1);
			//refresh page layout
			if (afterFunc != undefined && afterFunc != null) {
				getQAjaxRunJson("rstfld",false,1,"",url, false,data,afterFunc, true);
			} else {
				getQAjaxRunJson("rstfld",false,1,"",url, false,data,"", true);
			}

		}
	}
}
