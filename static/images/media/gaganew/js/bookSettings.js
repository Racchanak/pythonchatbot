flippingBook.pages = [
       "pages/small/10.jpg",
	"pages/small/1.jpg",
	"pages/small/2.jpg",
	"pages/small/3.jpg",
	"pages/small/4.jpg",
	"pages/small/5.jpg",
	"pages/small/6.jpg",
	"pages/small/7.jpg",
	"pages/small/8.jpg",
	"pages/small/9.jpg",
];


	flippingBook.contents = [
	[ "Cover", 1 ],
	[ "End", 8 ]
];


// define custom book settings here
flippingBook.settings.bookWidth = 854;
flippingBook.settings.bookHeight = 606;
flippingBook.settings.pageBackgroundColor = 0x5b7414;
flippingBook.settings.backgroundColor = 0xf7f2a7;
flippingBook.settings.zoomUIColor = 0x919d6c;
flippingBook.settings.smoothPages = false;	
flippingBook.settings.useCustomCursors = false;
flippingBook.settings.dropShadowEnabled = false,
flippingBook.settings.zoomImageWidth = 704;
flippingBook.settings.zoomImageHeight = 1000;
flippingBook.settings.downloadURL = "arcadia_e_brouchure.pdf";
flippingBook.settings.flipSound = "sounds/02.mp3";
flippingBook.settings.flipCornerStyle = "first page only";
flippingBook.settings.zoomHintEnabled = true;

// default settings can be found in the flippingbook.js file
flippingBook.create();
