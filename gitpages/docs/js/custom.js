document.addEventListener('DOMContentLoaded', function() {
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
                img.src = '/assets/icons/sol.png'; // Substitua pelo caminho da imagem para "Modo Escuro"
                break;
            case 'Modo Claro':
                img.src = '/assets/icons/lua.png'; // Substitua pelo caminho da imagem para "Outro Título"
                break;
        }

        img.alt = title; // Texto alternativo para a imagem

        // Substitui o conteúdo do label pelo elemento de imagem
        label.innerHTML = '';
        label.appendChild(img);
    });
});