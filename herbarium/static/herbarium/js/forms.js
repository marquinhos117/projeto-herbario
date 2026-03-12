/* ==========================================================================
   forms.js — Validações de segurança com Regex para formulários do Herbário
   ========================================================================== */

/* --------------------------------------------------------------------------
   HAMBURGER MENU — Toggle do menu em mobile
   -------------------------------------------------------------------------- */
const navToggle = document.getElementById('navToggle');
const mainNav   = document.getElementById('mainNav');

if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
        mainNav.classList.toggle('open');
        navToggle.classList.toggle('active');
    });

    // Fecha o menu ao clicar em qualquer link dentro dele
    mainNav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
            mainNav.classList.remove('open');
            navToggle.classList.remove('active');
        });
    });
}


/**
 * Validação do formulário de LOGIN
 * Bloqueia caracteres clássicos de SQL Injection no campo de usuário.
 */
const formLogin = document.querySelector('.curador-form');
if (formLogin) {
    formLogin.addEventListener('submit', function (e) {
        const username = document.getElementById('username').value;

        // Bloqueia: aspas simples/duplas, ponto e vírgula e traços (-- comentário SQL)
        const sqlInjectionRegex = /['";-]/;
        if (sqlInjectionRegex.test(username)) {
            e.preventDefault();
            alert(
                'Caracteres especiais inválidos no nome de usuário!\n' +
                'Aspas (\' "), ponto e vírgula (;) e traços (-) não são permitidos por segurança.'
            );
        }
    });
}

/**
 * Validação do formulário de CADASTRO
 * - Username: apenas letras, números e underlines.
 * - Senha forte: mínimo 8 caracteres, 1 maiúscula e 1 número.
 * - Confirmação de senha deve coincidir.
 */
const formCadastro = document.querySelector('.form-cadastro');
if (formCadastro) {
    formCadastro.addEventListener('submit', function (e) {
        const username         = document.getElementById('id_username').value;
        const password         = document.getElementById('id_password').value;
        const passwordConfirm  = document.getElementById('id_password_confirm').value;

        // Permite apenas letras (com acentos), números e underlines
        const usernameRegex = /^[a-zA-Z0-9_]+$/;
        if (!usernameRegex.test(username)) {
            e.preventDefault();
            alert('O nome de usuário deve conter apenas letras, números e underlines (_).\nCaracteres especiais não são permitidos.');
            return;
        }

        // Senha forte: mínimo 8 chars, ao menos 1 maiúscula e 1 dígito
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        if (!passwordRegex.test(password)) {
            e.preventDefault();
            alert('A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.');
            return;
        }

        if (password !== passwordConfirm) {
            e.preventDefault();
            alert('As senhas não coincidem. Verifique e tente novamente.');
        }
    });
}
