/**
 * Tree-sitter grammar for MiniLang (Refactored)
 */

module.exports = grammar({
  name: "minilang",

  // 1. Define the 'word' property so keywords take precedence over identifiers
  word: ($) => $.identifier,

  extras: ($) => [/\s/, $.comment],

  conflicts: ($) => [
    [$._expression, $.lvalue],
    [$._expression, $.struct_literal],
    [$.type, $.identifier],
  ],

  rules: {
    source_file: ($) => repeat($._top_level_statement),

    _top_level_statement: ($) =>
      choice(
        $.struct_definition,
        $.function_definition,
        $.const_declaration,
        $.var_declaration,
        $.array_declaration
      ),


// ── Comments ─────────────────────────────────────────────────────────────        
    // Updated comment rule
    comment: (_) => token(choice(
      seq('//', /[^\n]*/),
      seq('/*', /[^*]*\*+([^/*][^*]*\*+)*/, '/')
    )),

    // Ensure identifier doesn't conflict with simple tokens
    identifier: (_) => /[a-zA-Z_][a-zA-Z0-9_]*/,
    

    // ── Declarations ─────────────────────────────────────────────────────────
    const_declaration: ($) =>
      seq("const", $.identifier, ":", $.type, "=", $._expression, ";"),

    var_declaration: ($) =>
      seq(
        "var",
        $.identifier,
        ":",
        $.type,
        optional(seq("=", $._expression)),
        ";"
      ),

    array_declaration: ($) =>
      seq(
        "array",
        $.identifier,
        ":",
        $.type,
        "[",
        $.integer_literal,
        "]",
        optional(seq("=", $.array_literal)),
        ";"
      ),

    // ── Structs ──────────────────────────────────────────────────────────────
    struct_definition: ($) =>
      seq(
        "struct",
        $.identifier,
        "{",
        repeat($.struct_field),
        "}"
      ),

    struct_field: ($) => seq($.identifier, ":", $.type, ";"),

    // ── Functions ────────────────────────────────────────────────────────────
    function_definition: ($) =>
      seq(
        "fn",
        $.identifier,
        "(",
        optional($.parameter_list),
        ")",
        "->",
        $.type,
        $.block
      ),

    parameter_list: ($) =>
      seq($.parameter, repeat(seq(",", $.parameter))),

    parameter: ($) => seq($.identifier, ":", $.type),

    block: ($) => seq("{", repeat($._statement), "}"),

    // ── Statements ───────────────────────────────────────────────────────────
    _statement: ($) =>
      choice(
        $.var_declaration,
        $.const_declaration,
        $.array_declaration,
        $.assignment_statement,
        $.return_statement,
        $.if_statement,
        $.while_statement,
        $.expression_statement
      ),

    assignment_statement: ($) =>
      seq($.lvalue, "=", $._expression, ";"),

    lvalue: ($) =>
      choice(
        $.identifier,
        $.index_expression,
        $.field_access
      ),

    return_statement: ($) => seq("return", $._expression, ";"),

    if_statement: ($) =>
      seq(
        "if",
        "(",
        $._expression,
        ")",
        $.block,
        optional(seq("else", choice($.block, $.if_statement)))
      ),

    while_statement: ($) =>
      seq("while", "(", $._expression, ")", $.block),

    expression_statement: ($) => seq($._expression, ";"),

    // ── Expressions (Fixed Hierarchy) ────────────────────────────────────────
    _expression: ($) => choice(
      $.binary_expression,
      $.unary_expression,
      $._primary_expression
    ),

    _primary_expression: ($) => choice(
      $.call_expression,
      $.index_expression,
      $.field_access,
      $.struct_literal,
      $.array_literal,
      $.identifier,
      $.integer_literal,
      $.boolean_literal,
      seq("(", $._expression, ")")
    ),

    binary_expression: ($) => choice(
      ...[
        ['==', 1], ['!=', 1], ['<', 1], ['>', 1], ['<=', 1], ['>=', 1],
        ['|', 2],
        ['^', 3],
        ['&', 4],
        ['+', 5], ['-', 5],
        ['*', 6], ['/', 6], ['%', 6],
      ].map(([op, p]) => prec.left(p, seq(
        field("left", $._expression),
        op,
        field("right", $._expression)
      )))
    ),

    unary_expression: ($) => choice(
      prec(7, seq("-", $._expression)),
      prec(7, seq("~", $._expression))
    ),

    call_expression: ($) =>
      prec(9, seq($.identifier, "(", optional($.argument_list), ")")),

    argument_list: ($) =>
      seq($._expression, repeat(seq(",", $._expression))),

    index_expression: ($) =>
      prec(8, seq($._expression, "[", $._expression, "]")),

    field_access: ($) =>
      prec(8, seq($._expression, ".", $.identifier)),

    struct_literal: ($) =>
      prec(10, seq($.identifier, "{", optional($.field_init_list), "}")),

    field_init_list: ($) =>
      seq($.field_init, repeat(seq(",", $.field_init)), optional(",")),

    field_init: ($) => seq($.identifier, ":", $._expression),

    array_literal: ($) =>
      seq("[", optional(seq($._expression, repeat(seq(",", $._expression)))), "]"),

    // ── Terminals ─────────────────────────────────────────────────────────────
    type: ($) => choice(
      "int",
      "bool",
      "void",
      alias($.identifier, $.type_name)
    ),

    integer_literal: (_) => /[0-9]+/,

    boolean_literal: (_) => token(choice("true", "false")),

    identifier: (_) => /[a-zA-Z_][a-zA-Z0-9_]*/,
  },
});
