import express from "express";
const httpProxy = require("http-proxy");

const [basePort, count] = process.argv.slice(2);

const apps = new Array(Number(count)).fill(null).map(($) => express());

const proxy = httpProxy.createProxyServer({});

const handler =
    (num: number) => async (req: express.Request, res: express.Response) => {
        proxy.web(req, res, { target: "http://localhost:5000" });
    };

apps.forEach((app, idx) => {
    app.get("*", handler(idx));
});

apps.forEach((app, idx) => {
    app.listen(Number(basePort) + idx);
});
