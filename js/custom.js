document.addEventListener('DOMContentLoaded', function() {
    // Obtém a URL base do site
    var baseURL = window.location.origin + '/2024.1-Minecraft';

    // Seleciona todos os elementos com a classe especificada
    var labels = document.querySelectorAll('.md-header__button.md-icon');

    labels.forEach(function(label) {
        // Obtém o valor do atributo title
        var title = label.getAttribute('title');
        
        // Cria o novo elemento de imagem
        var img = document.createElement('img');
        img.width = 25;
        img.height = 25;
        
        // Define a fonte da imagem com base no valor do title
        switch (title) {
            case 'Modo Escuro':
                img.src = baseURL + '/assets/icons/sol.png'; // Caminho absoluto a partir da URL base
                break;
            case 'Modo Claro':
                img.src = baseURL + '/assets/icons/lua.png'; // Caminho absoluto a partir da URL base
                break;
        }

        img.alt = title; // Texto alternativo para a imagem

        // Substitui o conteúdo do label pelo elemento de imagem
        label.innerHTML = '';
        label.appendChild(img);
    });
});
