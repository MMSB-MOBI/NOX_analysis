var express = require('express')
var app = express()
var fs = require('fs');

fs.readFile('./latest.json', 'utf8', function (err, data) {
    if (err) throw err; // we'll not consider error handling for now
    let fullTree = JSON.parse(data);

   /* app.get('/tree', function (req, res) {
        console.log('sending tree')
        res.send(fullTree);
    })*/
    app.get('/api/:number', function (req, res) {
        console.log("Number is " + req.params.number);
        let tree = getNode(fullTree, req.params.number);
        if (tree == null){
            res.send(`Unknown taxonID ${req.params.number}`);
            return;
        }
        console.log(tree);

        res.send(tree);
    })

    app.get('/:number', function (req, res) {
        //console.log(__dirname);
        res.sendFile(__dirname + '/index.html');
    });
    app.get('/', function (req, res) {
        //console.log(__dirname);
        res.sendFile(__dirname + '/index.html');
    });
    app.listen(9615);
});



/*
    Extract subtree
*/
function getNode(root, nodeID){
    let queryNode = isOk(root, nodeID);
    return queryNode;
}


function isOk(node, nodeID){
    //console.log(`${node.taxid} vs ${nodeID}`);
    if (node.taxid == nodeID)
        return node;
    for (let childNode of node.children) {
        let nodeState = isOk(childNode, nodeID);
        if (nodeState != null)
            return nodeState;
    }
    return null;
}
