import type { LoginForm, MessageForm } from '../types/auth'

export function isValidLoginForm(loginForm:LoginForm) :boolean {

    if (loginForm.email.trim()=='' || loginForm.password.trim()=='') {
        return false;
    }
    return true;
}