/**
 * A small, build-time syntax highlighter.
 *
 * The documentation sites load no external resources, so highlighting happens
 * when the site is generated rather than in the browser. The output is plain
 * `<span>` elements with a handful of `tok-*` classes.
 *
 * It is deliberately small: enough to make the examples readable, not a
 * full parser.
 */

const GRAMMAR = {
  python: {
    lineComment: "#",
    blockComment: null,
    strings: ['"""', "'''", '"', "'"],
    charLiteral: false,
    keywords: [
      "False", "None", "True", "and", "as", "assert", "async", "await", "break",
      "class", "continue", "def", "del", "elif", "else", "except", "finally",
      "for", "from", "global", "if", "import", "in", "is", "lambda", "match",
      "nonlocal", "not", "or", "pass", "raise", "return", "try", "while",
      "with", "yield",
    ],
    builtins: [
      "print", "len", "range", "str", "int", "float", "bool", "dict", "list",
      "set", "tuple", "open", "isinstance", "super", "self", "cls", "enumerate",
      "zip", "sorted", "sum", "min", "max", "abs", "any", "all", "getattr",
    ],
    types: [],
  },
  typescript: {
    lineComment: "//",
    blockComment: "/*",
    blockClose: "*/",
    strings: ['"', "'", "`"],
    charLiteral: false,
    keywords: [
      "as", "async", "await", "break", "case", "catch", "class", "const",
      "continue", "debugger", "declare", "default", "delete", "do", "else",
      "enum", "export", "extends", "false", "finally", "for", "from", "function",
      "if", "implements", "import", "in", "instanceof", "interface", "is",
      "keyof", "let", "new", "null", "of", "package", "private", "protected",
      "public", "readonly", "return", "satisfies", "static", "super", "switch",
      "this", "throw", "true", "try", "type", "typeof", "undefined", "var",
      "void", "while", "yield",
    ],
    builtins: ["Promise", "console", "JSON", "Object", "Array", "String", "Number", "Boolean", "Math", "Date", "Error", "Record", "Partial"],
    types: [],
  },
  rust: {
    lineComment: "//",
    blockComment: "/*",
    blockClose: "*/",
    strings: ['"'],
    charLiteral: true,
    keywords: [
      "as", "async", "await", "break", "const", "continue", "crate", "dyn",
      "else", "enum", "extern", "false", "fn", "for", "if", "impl", "in",
      "let", "loop", "match", "mod", "move", "mut", "pub", "ref", "return",
      "self", "Self", "static", "struct", "super", "trait", "true", "type",
      "unsafe", "use", "where", "while",
    ],
    builtins: ["String", "Vec", "Option", "Result", "Box", "Some", "Ok", "Err", "None", "bool", "str", "i64", "u64", "f64"],
    types: [],
  },
};

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function isWordStart(char) {
  return /[A-Za-z_]/.test(char);
}

function isWord(char) {
  return /[A-Za-z0-9_]/.test(char);
}

/**
 * Highlight a code sample.
 *
 * @param {string} code the sample
 * @param {string} language one of python, typescript, rust
 * @returns {string} HTML with `tok-*` spans
 */
export function highlight(code, language) {
  const grammar = GRAMMAR[language];
  if (!grammar) return escapeHtml(code);

  let out = "";
  let index = 0;
  const length = code.length;

  while (index < length) {
    const rest = code.slice(index);

    // Line comment
    if (grammar.lineComment && rest.startsWith(grammar.lineComment)) {
      const newline = code.indexOf("\n", index);
      const stop = newline === -1 ? length : newline;
      out += `<span class="tok-com">${escapeHtml(code.slice(index, stop))}</span>`;
      index = stop;
      continue;
    }

    // Block comment (nestable in Rust)
    if (grammar.blockComment && rest.startsWith(grammar.blockComment)) {
      let depth = 0;
      let cursor = index;
      while (cursor < length) {
        if (code.startsWith(grammar.blockComment, cursor)) {
          depth += 1;
          cursor += grammar.blockComment.length;
          continue;
        }
        if (code.startsWith(grammar.blockClose, cursor)) {
          depth -= 1;
          cursor += grammar.blockClose.length;
          if (depth === 0) break;
          continue;
        }
        cursor += 1;
      }
      out += `<span class="tok-com">${escapeHtml(code.slice(index, cursor))}</span>`;
      index = cursor;
      continue;
    }

    // Rust character literal: 'a' or '\n'. A lone quote is a lifetime.
    if (grammar.charLiteral && code[index] === "'") {
      const literal = /^'(\\.|[^\\'])'/.exec(rest);
      if (literal) {
        out += `<span class="tok-str">${escapeHtml(literal[0])}</span>`;
        index += literal[0].length;
        continue;
      }
      out += escapeHtml("'");
      index += 1;
      continue;
    }

    // Strings
    let delimiter = null;
    for (const candidate of grammar.strings) {
      if (rest.startsWith(candidate)) {
        delimiter = candidate;
        break;
      }
    }
    if (delimiter) {
      let cursor = index + delimiter.length;
      while (cursor < length) {
        if (code[cursor] === "\\") {
          cursor += 2;
          continue;
        }
        if (code.startsWith(delimiter, cursor)) {
          cursor += delimiter.length;
          break;
        }
        cursor += 1;
      }
      out += `<span class="tok-str">${escapeHtml(code.slice(index, cursor))}</span>`;
      index = cursor;
      continue;
    }

    // Numbers
    if (/[0-9]/.test(code[index])) {
      let cursor = index;
      while (cursor < length && /[0-9a-fA-FxXbBoO._]/.test(code[cursor])) cursor += 1;
      out += `<span class="tok-num">${escapeHtml(code.slice(index, cursor))}</span>`;
      index = cursor;
      continue;
    }

    // Words
    if (isWordStart(code[index])) {
      let cursor = index;
      while (cursor < length && isWord(code[cursor])) cursor += 1;
      const word = code.slice(index, cursor);

      let className = null;
      if (grammar.keywords.includes(word)) className = "tok-kw";
      else if (grammar.builtins.includes(word)) className = "tok-bi";
      else if (code[cursor] === "(") className = "tok-fn";
      else if (/^[A-Z]/.test(word)) className = "tok-ty";

      out += className
        ? `<span class="${className}">${escapeHtml(word)}</span>`
        : escapeHtml(word);
      index = cursor;
      continue;
    }

    // Punctuation and everything else
    out += escapeHtml(code[index]);
    index += 1;
  }

  return out;
}
