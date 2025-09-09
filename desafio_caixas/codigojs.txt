'use strict'

// Reconhecendo pelo ID tudo que será necessário para executar alguma função
const botaoPesquisa = document.getElementById('botaoPesquisa')
const barraPesquisa = document.getElementById('barraPesquisa')
const galeria = document.getElementById('galeria')
const imgPrincipal = document.getElementById('imgPrincipal')
const textoInicial = document.getElementById('textoInicial')
const fundo = document.getElementById('fundo')

// Função para buscar herói na API
async function buscarHeroi(termo) {
    try {
        // Buscar por nome
        const response = await fetch(`https://www.superheroapi.com/api.php/896c3ae8a2e2d92b14388ca61a36127e/search/${termo}`) // URL da API
        const data = await response.json()
        
        // Confirmar que está retornando algum dado 
        if (data.response === "success" && data.results.length > 0) {
            return data.results //Return dos resultados da busca pelo nome
        }
        
        // Busca por ID
        if (!isNaN(termo)) {
            const responseById = await fetch(`https://www.superheroapi.com/api.php/896c3ae8a2e2d92b14388ca61a36127e/${termo}`)
            const hero = await responseById.json()
            
            // Confirmar que está retornando algum dado 
            if (hero.response === "success") {
                return [hero] //Return de array do heroi
            }
        }
        
        return []
    } catch (error) {
        console.error("Erro na API:", error)
        return [] // Retornar um Array vazio caso de um erro na API 
    }
}

// Função para criar o Card
function criarCard(heroi) {
    const card = document.createElement('div') // Cria o card
    card.className = 'character-card'
    
    // Pegar e colocar a imagem da API
    const img = document.createElement('img')
    img.src = heroi.image?.url || './img/placeholder.jpg'
    img.alt = heroi.name
    img.loading = 'lazy'
    
    // Acrescentar o apelido do personagem
    const nome = document.createElement('h2')
    nome.textContent = heroi.name
    
    // Acrescentar o ID do personagem
    const id = document.createElement('p')
    id.textContent = `ID: ${heroi.id}`

    // Acrescentar o nome do personagem
    const nomeCompleto = document.createElement('h3')
    nomeCompleto.textContent = `Nome: ${heroi.biography["full-name"]} `
    
    // Colocar tudo no Card
    card.append(img, nome, id, nomeCompleto)
    return card
}

// Função para deletar os itens da tela estática
function limparTela() {
    imgPrincipal.style.display = 'none'
    textoInicial.style.display = 'none'
    fundo.style.display = 'none'
    galeria.innerHTML = ''
    galeria.style.display = 'grid' // Define o container como grid para meljhor organizar na págima 
}

// Função para executar todas as outras (limpar tela, pesquisar e mostrar os cards)
async function exibirHerois() {
    const termo = barraPesquisa.value.trim()  // Reconhecer o valor digitado na barra de pesquisa
    
    // Mensagem de erro caso clique no botão sem digitar nenhum nome ou ID
    if (!termo) {
        alert('Por favor, digite um nome ou ID de herói')
        return
    }
    
    // Executa a função de limpar a tela
    limparTela()
    
    // Mensagem de carregamento enquanto procura na API os pesonagens 
    const loading = document.createElement('div')
    loading.textContent = 'Buscando heróis...'
    loading.className = 'mensagem-carregamento'
    galeria.appendChild(loading)
    
    // Executa a função buscar herói
    const herois = await buscarHeroi(termo)
    
    galeria.innerHTML = ''
    
    // Mensagem de erro caso digite um heroi ou ID que não existe 
    if (herois.length === 0) {
        const mensagem = document.createElement('p')
        mensagem.textContent = 'Nenhum herói encontrado. Tente outro nome ou ID.'
        mensagem.className = 'mensagem-erro'
        galeria.appendChild(mensagem)
        return
    }
    
    // Acrescenta dentro da div galeria os cards 
    herois.forEach(heroi => {
        galeria.appendChild(criarCard(heroi))
    })
}

// Clique do botão
botaoPesquisa.addEventListener('click', exibirHerois)
barraPesquisa.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') exibirHerois() // Quando pressionar a tecla enter ele pesquisa
})