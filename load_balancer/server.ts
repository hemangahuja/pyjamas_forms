import express from "express";
const httpProxy = require("http-proxy");

const [basePort, count] = process.argv.slice(2);

//creates count number of server connections for balancing the load
const apps = new Array(Number(count)).fill(null).map(($) => express());

const proxy = httpProxy.createProxyServer({});

//process request
const handler =
    (num: number) => async (req: express.Request, res: express.Response) => {
        proxy.web(req, res, { target: "http://localhost:5000" });
    };

//create handler for each connection
apps.forEach((app, idx) => {
    app.get("*", handler(idx));
});

//start listening on all the connections
apps.forEach((app, idx) => {
    app.listen(Number(basePort) + idx);
});
