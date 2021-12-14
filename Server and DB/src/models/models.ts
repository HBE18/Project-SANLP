export interface UserInsert {
    email: string;
    password: string;
    firstName?: string;
    lastName?: string;
    secLevel: number;
}

export interface UserUpdate {
    email: string;
    password?: string;
    firstName?: string;
    lastName?: string;
    secLevel: number;
}

export interface CRUD {
    list: (limit: number, page: number) => Promise<any>;
    create: (resource: any) => Promise<any>;
    putById: (id: string, resource: any) => Promise<string>;
    readById: (id: string) => Promise<any>;
    deleteById: (id: string) => Promise<string>;
    patchById: (id: string, resource: any) => Promise<string>;
}

export type User = UserUpdate;

export interface Patch extends Partial<UserUpdate>{}

export interface emailReq {
    email: string;
}

export interface UserResponse {
    id: string;
    email: string;
}
