var express = require('express');
const fs = require('fs');
var router = express.Router();
const path = require('path')

let student=""




router.route('/getstoreregister')

     	 .get(function (req, res) {
	 	
			fs.readFile('../data.json', (err, data) => {
    if (err) throw err;
     student= JSON.parse(data);
     
     res.send(student);	
    
});      
});	

router.route('/getserverapi')

     	 .get(function (req, res) {

			fs.readFile('../serverapi.json', (err, data) => {
    if (err) throw err;
     student= JSON.parse(data);

     res.send(student);

});
});




module.exports = router;
