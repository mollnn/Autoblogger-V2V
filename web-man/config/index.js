// module.exports={
//     devServer:{
//         proxy:{
//             ["/api"]:{
//             target:'http://131.mollnn.com:5000',
//               changeOrigin:true,
//                 pathRewrite: {
//                     ['^' + "/api"]: ''
//                 }
//             }
//         }

//     }
// }
module.exports = {
	dev:{
		assetSubDirectory: 'static',
		assetPublicPath:'/',
		proxyTable:{},
		host:'localhost',
		port:80,
		autoOpenBrowser:false,
		errorOverlay:true,
		notifyOnErrors:true,
		poll:false,
		devtool: 'cheap-module-eval-source-map',
		cacheBusting:true,
		cssSourceMap:true
	}
};
