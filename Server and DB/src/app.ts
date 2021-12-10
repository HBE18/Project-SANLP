import express from 'express';
import { HttpCode } from './constants';

const app = express();
const config = require("../config.json");
const port = 3000;
app.use(express.json());

const returner = "Hello Natural Language Processers!"
const msg  = `App is running at http://localhost:${port}`;
app.get("/", async (req,res) => {
    res.status(HttpCode.Success).send(returner);
})

console.log(msg);
app.listen(port);