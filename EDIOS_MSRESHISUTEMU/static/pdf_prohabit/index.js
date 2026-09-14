// var pdf = window.opener.document.getElementById("WF_PRINTFILEID").value;

let time = getParam("time")
let pdf = sessionStorage.getItem(time)

function getParam(key) {
    var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)")
    var r = window.location.search.substr(1).match(reg)
    if (r != null) return unescape(r[2]); return null
}

const pageNum = document.querySelector('#page_num');
const pageCount = document.querySelector('#page_count');
const currentPage = document.querySelector('#current_page');
const previousPage = document.querySelector('#prev_page');
const nextPage = document.querySelector('#next_page');
const zoomIn = document.querySelector('#zoom_in');
const zoomOut = document.querySelector('#zoom_out');

const initialState = {
	pdfDoc: null,
	currentPage: 1,
	pageCount: 0,
	zoom: 4.5,
};

pdfjsLib.GlobalWorkerOptions.workerSrc = "./static/pdf_prohabit/pdf.worker.js";

// Load the document.
pdfjsLib
	.getDocument(pdf)
	.promise.then((data) => {
		initialState.pdfDoc = data;
		console.log('pdfDocument', initialState.pdfDoc);

		pageCount.textContent = initialState.pdfDoc.numPages;
		initialState.pageCount = initialState.pdfDoc.numPages

		renderPage();
	})
	.catch((err) => {
		alert(err.message);
	});
// Render the page.
const renderPage = () => {
	// Load the first page.
	let contentDiv = document.getElementById("content");
	for (let i = 0; i < initialState.pageCount; i++) {
		let canvas = document.createElement("canvas")
		initialState.pdfDoc.getPage(i+1).then((page) => {
			// const offsetX = 50;  // 设定左边距为50单位
			const offsetX = 0;
			const transform = [1, 0, 0, 1, offsetX, 0];  // 创建一个变换矩阵，仅在x轴方向偏移
			const ctx = canvas.getContext('2d');
			const viewport = page.getViewport({
				scale: initialState.zoom,
				offsetX: offsetX,
				transform: transform
			});
			canvas.height = viewport.height;
			canvas.width = viewport.width;

			const renderCtx = {
				canvasContext: ctx,
				viewport: viewport,
			};
			page.render(renderCtx);
			pageNum.textContent = initialState.currentPage;
		});
		contentDiv.appendChild(canvas)
	}

	// initialState.pdfDoc
	// 	.getPage(initialState.currentPage)
	// 	.then((page) => {
	// 		console.log('page', page);

	// 		const offsetX = 50;  // 设定左边距为50单位
	// 		const transform = [1, 0, 0, 1, offsetX, 0];  // 创建一个变换矩阵，仅在x轴方向偏移

	// 		const canvas = document.querySelector('#canvas');
	// 		const ctx = canvas.getContext('2d');
	// 		const viewport = page.getViewport({
	// 			scale: initialState.zoom,
	// 			offsetX: offsetX,
	// 			transform: transform
	// 		});

	// 		canvas.height = viewport.height;
	// 		canvas.width = viewport.width;

	// 		// Render the PDF page into the canvas context.
	// 		const renderCtx = {
	// 			canvasContext: ctx,
	// 			viewport: viewport,
	// 		};

	// 		page.render(renderCtx);

	// 		pageNum.textContent = initialState.currentPage;
	// 	});
};
const showPrevPage = () => {
	if (initialState.pdfDoc === null || initialState.currentPage <= 1)
		return;
	initialState.currentPage--;
	// Render the current page.
	currentPage.value = initialState.currentPage;
	renderPage();
};

const showNextPage = () => {
	if (
		initialState.pdfDoc === null ||
		initialState.currentPage >= initialState.pdfDoc._pdfInfo.numPages
	)
		return;

	initialState.currentPage++;
	currentPage.value = initialState.currentPage;
	renderPage();
};

// Button events.
previousPage.addEventListener('click', showPrevPage);
nextPage.addEventListener('click', showNextPage);
// Keypress event.
currentPage.addEventListener('keypress', (event) => {
	if (initialState.pdfDoc === null) return;
	// Get the key code.
	const keycode = event.keyCode ? event.keyCode : event.which;

	if (keycode === 13) {
		// Get the new page number and render it.
		let desiredPage = currentPage.valueAsNumber;
		initialState.currentPage = Math.min(
			Math.max(desiredPage, 1),
			initialState.pdfDoc._pdfInfo.numPages,
		);

		currentPage.value = initialState.currentPage;
		renderPage();
	}
});
// Zoom events.
zoomIn.addEventListener('click', () => {
	if (initialState.pdfDoc === null) return;
	// initialState.zoom *= 20 / 19;
	initialState.zoom += 0.05
	console.log(initialState.zoom)
	renderPage();
});

zoomOut.addEventListener('click', () => {
	if (initialState.pdfDoc === null) return;
	// initialState.zoom *= 19 / 20;
	initialState.zoom -= 0.05
	renderPage();
});
const printButton = document.querySelector('.print-button');

// Print PDF.
printButton.addEventListener('click', () => {

	var iframe = document.getElementById('pdfIframe');
    iframe.src = pdf;

    iframe.onload = function() {
	    //doc.head.appendChild(style);
        iframe.contentWindow.focus();
        iframe.contentWindow.print();
    };
	return

	let canvasList = document.getElementsByTagName("canvas");

	for (let i = 0; i < canvasList.length; i++) {
		canvasList[i].style.boxShadow = "0 0 0 #fff";
	}

	if (canvasList[0].width > canvasList[0].height) {
		setPrintOrientation('landscape', 1.6);
	} else {
		setPrintOrientation('portrait', 1);
	}

	window.print()

	for (let i = 0; i < canvasList.length; i++) {
		canvasList[i].style.boxShadow = "0 0 10px #535353";
	}
});

function setPrintScale(scale) {
    var printStyles = `
        @media print {
            body {
                transform: scale(${scale});
                transform-origin: top left;
            }
        }
    `;

    // 既存の印刷スタイルを削除
    // var existingStyles = document.getElementById('print-styles');
    // if (existingStyles) {
    //     // existingStyles.parentNode.removeChild(existingStyles);
    // }

    // 新しいスタイルを追加
    var styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.id = 'print-styles';
    styleSheet.innerHTML = printStyles;
    document.head.appendChild(styleSheet);
}

function setPrintStyles() {
    var printStyles = `
        @media print {
            @page {
                size: A4;
                margin: 1cm;
            }
            body {
                margin: 0;
                padding: 0;
                background-color: white;
            }
            .printable-area {
                width: 100%;
                height: auto;
                page-break-after: always;
            }
        }
    `;

    var styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = printStyles;
    document.head.appendChild(styleSheet);
}

function setPrintOrientation(orientation, scale) {
    var printStyles = `
        @media print {
            @page {
                size: ${orientation};
            }
            body {
                transform: scale(${scale});
                transform-origin: top center;
            }
        }
    `;

    // 既存の印刷スタイルを削除
    var existingStyles = document.getElementById('print-styles');
    if (existingStyles) {
        existingStyles.parentNode.removeChild(existingStyles);
    }

    // 新しいスタイルを追加
    var styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.id = 'print-styles';
    styleSheet.innerHTML = printStyles;
    document.head.appendChild(styleSheet);
}

// printButton.addEventListener('click', () => {
// 	printJS('canvas', 'html');
// });

document.getElementsByTagName('html')[0].oncontextmenu = function () {return false;}
document.body.oncontextmenu = function () {return false;}

