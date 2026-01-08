from typing import Dict, List
import spacy
from wordfreq import zipf_frequency
import language_tool_python

# ===== Inicializações =====
NLP = spacy.load("pt_core_news_lg")
LT = None


def get_language_tool():
    """Inicializa e retorna uma instância de LanguageTool ou None se falhar.

    Tenta inicializar localmente; se houver a variável de ambiente
    `LANGUAGE_TOOL_REMOTE` usa o servidor remoto. Em caso de erro, retorna
    None para não quebrar a aplicação.
    """
    global LT
    if LT is not None:
        return LT

    try:
        LT = language_tool_python.LanguageTool("pt-BR")
        return LT
    except Exception:
        # fallback para servidor remoto se fornecido via env
        try:
            import os

            remote = os.getenv("LANGUAGE_TOOL_REMOTE")
            if remote:
                LT = language_tool_python.LanguageTool("pt-BR", remote_server=remote)
                return LT
        except Exception:
            pass

    LT = None
    return None


# ===== Ortografia =====
def check_orthography(doc) -> List[str]:
    """
    Marca tokens com baixa probabilidade lexical.
    Evita falsos positivos (nomes próprios, siglas).
    """
    issues = []

    for token in doc:
        if (
            token.is_alpha
            and token.pos_ not in {"PROPN"}
            and zipf_frequency(token.text.lower(), "pt") < 1.5
        ):
            issues.append(
                f"Possível erro ortográfico ou forma incomum: '{token.text}'"
            )

    return issues


# ===== Gramática =====
def check_grammar(doc) -> List[str]:
    issues = []

    # Verbo sem sujeito explícito ou elíptico reconhecível
    for token in doc:
        if token.pos_ == "VERB":
            has_subject = any(
                child.dep_ in {"nsubj", "nsubj:pass"} for child in token.children
            )

            if not has_subject and not doc[0].pos_ == "VERB":
                issues.append(
                    f"Verbo '{token.text}' pode estar sem sujeito claro"
                )

    # Concordância básica sujeito-verbo
    for token in doc:
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            if (
                "Number=Plur" in token.morph
                and "Number=Sing" in token.head.morph
            ):
                issues.append(
                    f"Possível erro de concordância entre '{token.text}' e '{token.head.text}'"
                )

    return issues


# ===== Semântica =====
def check_semantics(doc) -> List[str]:
    issues = []

    verbs = [t for t in doc if t.pos_ == "VERB"]
    objects = [t for t in doc if t.dep_ in {"obj", "iobj"}]

    # Verbo transitivo sem objeto
    for verb in verbs:
        if verb.lemma_ in {"precisar", "gostar", "querer"} and not objects:
            issues.append(
                f"O verbo '{verb.text}' normalmente exige complemento"
            )

    # Sujeito inanimado com verbo de ação humana
    for token in doc:
        if token.dep_ == "nsubj" and token.head.lemma_ in {"decidir", "pensar"}:
            if token.pos_ not in {"PROPN", "PRON"}:
                issues.append(
                    f"Sujeito '{token.text}' pode ser semanticamente incompatível com o verbo '{token.head.text}'"
                )

    return issues


# ===== Função principal =====
def validate_sentence(sentence: str) -> Dict:
    doc = NLP(sentence)

    ortho = check_orthography(doc)
    grammar = check_grammar(doc)
    semantics = check_semantics(doc)

    # Complemento com LanguageTool
    lt = get_language_tool()
    lt_matches = []
    if lt is not None:
        try:
            lt_matches = lt.check(sentence)
        except Exception:
            lt_matches = []

    grammar.extend(
        [f"[LT] {m.message}" for m in lt_matches if getattr(m, "ruleIssueType", None) == "grammar"]
    )

    return {
        "frase_correta": not (ortho or grammar or semantics),
        "ortografia": {
            "status": "ok" if not ortho else "verificar",
            "problemas": ortho,
        },
        "gramatica": {
            "status": "ok" if not grammar else "verificar",
            "problemas": grammar,
        },
        "semantica": {
            "status": "ok" if not semantics else "verificar",
            "problemas": semantics,
        },
    }



# Verifica se o script está sendo executado como o programa principal
if __name__ == "__main__":
    print(validate_sentence("Eu gosto de  pizza."))
