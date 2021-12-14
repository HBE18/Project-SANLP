import express, { query, response} from "express";
import * as mods from "../models/models";
import shortid from "shortid"

export function addUser(user:mods.UserInsert): string {
    const userid = shortid.generate();
    try {
        //Querying with DB #Add user with models.UserInsert
    } catch (error) {
        console.error(error);
    }
    return userid;
}

export /*async*/ function getUsers() /*:Promise<QueryResult<any>>*/ {
    try {
        return /*await*/ "users"; //query Select * FROM Users like
        //return await query;
    } catch (error) {
        console.error(error);
        throw(error);
    }
}

export /* async*/ function getUserById(userId:string)/*: Promise<model>*/{
    try {
        // const {rows, rowCount} = await query
    } catch (error) {
        console.error(error);
        throw(error);
    }
}

export /*async*/ function putUserById(userId:string, user:mods.Patch)/*: Promise<string>*/{
    try {
        const resp = "a";//await query
    } catch (error) {
        console.error(error);
        throw(error);
    }

}

export async function patchUserById(userId:string,user:mods.Patch)/*Promise<string>*/{
    const resp = await getUserById(userId);
    // const updatedUser = {
    //     email: user.email ?? resp.email,
    //     password : user.password ?? resp.password,
    //     firstName : user.firstName ?? resp.firstName,
    //     lastName : user.lastName ?? resp.lastName,
    //     secLevel : user.secLevel ?? resp.secLevel
    // } as mods.UserUpdate;
    //await putUserById(userId/,updatedUser);
    return userId;
}

export async function removeUserById(userId: string):Promise<void> {
    return await new Promise((resolve,reject) => {
        //query
            //release();
            //resolve();
    })
}

export async function getUserByEmail(email: string): Promise<boolean> {
    try {
        //query
        return true;
    } catch (error) {
        console.error(error);
        throw(error);
    }
}

module.exports;