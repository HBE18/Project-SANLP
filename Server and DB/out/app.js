"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const constants_1 = require("./constants");
const app = express_1.default();
const config = require("../config.json");
const port = 3000;
app.use(express_1.default.json());
const returner = "Hello Natural Language Processers!";
const msg = `App is running at http://localhost:${port}`;
app.get("/", async (req, res) => {
    res.status(constants_1.HttpCode.Success).send(returner);
});
console.log(msg);
app.listen(port);
//# sourceMappingURL=app.js.map