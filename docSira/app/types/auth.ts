export interface LoginForm {
    email: string;
    username?: string;
    password: string;
}

export function isValidLoginForm(loginForm:LoginForm): boolean {

    if (!loginForm.email || !loginForm.password) {
        return false;
    }
    return true;
}