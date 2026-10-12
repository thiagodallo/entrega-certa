const listaDeRespostas = document.querySelector("#lista-de-respostas");
const avisoDeVazio = document.querySelector("#respostas-vazio");
const botaoLimpar = document.querySelector("#limpar-respostas");
const LIMITE_DE_RESPOSTAS = 12;

function montarRequisicao(formulario) {
  let caminho = formulario.dataset.caminho;
  const corpo = {};
  for (const campo of formulario.querySelectorAll("input[name]")) {
    const texto = campo.value.trim();
    if ("noCaminho" in campo.dataset) {
      caminho = caminho.replace(`{${campo.name}}`, encodeURIComponent(texto));
      continue;
    }
    if (texto === "") continue;
    const numero = Number(texto.replace(",", "."));
    corpo[campo.name] = "numero" in campo.dataset && !Number.isNaN(numero) ? numero : texto;
  }
  return { metodo: formulario.dataset.metodo, caminho, corpo };
}

async function chamarApi(metodo, caminho, corpo) {
  const opcoes = { method: metodo, headers: { Accept: "application/json" } };
  if (metodo !== "GET") {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }
  const resposta = await fetch(caminho, opcoes);
  const texto = await resposta.text();
  return { status: resposta.status, dados: texto ? JSON.parse(texto) : null };
}

function criarElemento(nome, classe, texto) {
  const elemento = document.createElement(nome);
  if (classe) elemento.className = classe;
  if (texto !== undefined) elemento.textContent = texto;
  return elemento;
}

function mostrarResposta(metodo, caminho, status, dados) {
  const falhou = status === 0 || status >= 400;
  const item = criarElemento("li", falhou ? "resposta falhou" : "resposta");
  const topo = criarElemento("div", "resposta-topo");
  topo.append(
    criarElemento("span", "status", status === 0 ? "sem resposta" : String(status)),
    criarElemento("span", "", `${metodo} ${caminho}`),
  );
  item.append(topo);
  if (falhou && dados?.mensagem) {
    item.append(criarElemento("p", "mensagem", dados.mensagem));
  }
  if (dados !== null) {
    item.append(criarElemento("pre", "", JSON.stringify(dados, null, 2)));
  }
  listaDeRespostas.prepend(item);
  while (listaDeRespostas.children.length > LIMITE_DE_RESPOSTAS) {
    listaDeRespostas.lastElementChild.remove();
  }
  avisoDeVazio.hidden = true;
  botaoLimpar.hidden = false;
}

function preencherIdCriado(entidade, id) {
  for (const campo of document.querySelectorAll(`input[data-id-de="${entidade}"]`)) {
    campo.value = id;
  }
}

async function enviar(metodo, caminho, corpo, botao, entidade) {
  const rotulo = botao.textContent;
  botao.disabled = true;
  botao.textContent = "Enviando…";
  try {
    const { status, dados } = await chamarApi(metodo, caminho, corpo);
    mostrarResposta(metodo, caminho, status, dados);
    if (entidade && status === 201) preencherIdCriado(entidade, dados.id);
  } catch {
    mostrarResposta(metodo, caminho, 0, {
      mensagem: "A API não respondeu. Confira se ela está no ar.",
    });
  } finally {
    botao.disabled = false;
    botao.textContent = rotulo;
  }
}

function dataLocal(diasAPartirDeHoje) {
  const dia = new Date();
  dia.setDate(dia.getDate() + diasAPartirDeHoje);
  const mes = String(dia.getMonth() + 1).padStart(2, "0");
  return `${dia.getFullYear()}-${mes}-${String(dia.getDate()).padStart(2, "0")}`;
}

for (const formulario of document.querySelectorAll("form[data-caminho]")) {
  formulario.addEventListener("submit", (evento) => {
    evento.preventDefault();
    const { metodo, caminho, corpo } = montarRequisicao(formulario);
    enviar(metodo, caminho, corpo, evento.submitter, formulario.dataset.entidade);
  });
}

for (const botao of document.querySelectorAll("button[data-caminho]")) {
  botao.addEventListener("click", () => {
    enviar(botao.dataset.metodo, botao.dataset.caminho, null, botao);
  });
}

for (const botao of document.querySelectorAll("button[data-dias]")) {
  botao.addEventListener("click", () => {
    botao.form.elements.prazo.value = dataLocal(Number(botao.dataset.dias));
  });
}

botaoLimpar.addEventListener("click", () => {
  listaDeRespostas.replaceChildren();
  avisoDeVazio.hidden = false;
  botaoLimpar.hidden = true;
});

document.querySelector('input[name="prazo"]').value = dataLocal(3);
