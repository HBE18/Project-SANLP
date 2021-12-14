import express from "express";
import * as core from "../core/core";
import { HttpCode } from "../constants";

export async function listUsers(req: express.Request, res: express.Response) {
    const users = await core.getUsers();
    if(users != undefined){
        //res.status(HttpCode.Success).json(users.rows);
    }
    else{
        res.status(HttpCode.NoContent).send("List operation failed");
    }
}

export async function getUserById(req: express.Request, res: express.Response) {
    const user = await  core.getUserById(req.params.id);
    res.status(HttpCode.Success).json(user);
}

export function createUser(req: express.Request, res: express.Response) {
    //req.body.password;
    const userId = core.addUser(req.body);
    res.status(HttpCode.Created).json({ id: userId });
}

export async function patch(req: express.Request, res: express.Response) {
    const rep = await core.patchUserById(req.body.userid, req.body)
    console.log(rep);
    res.status(HttpCode.Success).json(`User ${rep} has updated by Patch`);
}

export async function put(req: express.Request, res: express.Response) {
    const rep = await core.putUserById(req.body.userid, req.body)
    console.log(rep);
    res.status(HttpCode.Success).json(`User ${rep} has updated by PUT`);
}

export async function removeUser(req: express.Request, res: express.Response) {
    await core.removeUserById(req.params.userId);
    res.status(HttpCode.Success).send();
}

module.exports;